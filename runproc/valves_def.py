import argparse
import os
import nibabel as nib
import numpy as np
import gc
import cv2
from sklearn.decomposition import PCA
from skimage.measure import label, regionprops
from scipy import ndimage
from math import sqrt

gc.collect()

pwd = os.getcwd()

def get_plane_equation(P, Q, R):  # To split the valves.
    x1, y1, z1 = P
    x2, y2, z2 = Q
    x3, y3, z3 = R
    a1 = x2 - x1 
    b1 = y2 - y1 
    c1 = z2 - z1 
    a2 = x3 - x1 
    b2 = y3 - y1 
    c2 = z3 - z1 
    a = b1 * c2 - b2 * c1 
    b = a2 * c1 - a1 * c2 
    c = a1 * b2 - b1 * a2 
    d = (- a * x1 - b * y1 - c * z1) 
    return a, b, c, d
    
# To remove miocardium placed inside the spheroid volume given by the valve, in roder to give more depth, I have used the semimajor valve axis for two of the spheroid axes.
def into_spheroid(xi,yi,zi,c_coordi,ax1,ax2,ax3):   
    point = np.array([xi,yi,zi])
    r_centered = point - c_coordi
    
    mat_1 = np.column_stack([r_centered,ax2,ax3])
    mat_2 = np.column_stack([ax1,r_centered,ax3])
    mat_3 = np.column_stack([ax1,ax2,r_centered])
    mat_r = np.column_stack([ax1,ax2,ax3])
    
    left_side = (np.linalg.det(mat_1))**2 + (np.linalg.det(mat_2))**2 + (np.linalg.det(mat_3))**2
#    print('ls ',left_side)
    right_side = (np.linalg.det(mat_r))**2
#    print('rs ',right_side)
    if left_side <= right_side:
        return True
    else:
        return False
        
    gc.collect()

# Length for each of the ellipsoid axes which define the valve.
def ellipsoid_axis_lengths(inertia_tensor_eigvals):
    axis_lengths = []
    for ax in range(2, -1, -1):
        w = sum(v * -1 if i == ax else v for i, v in enumerate(inertia_tensor_eigvals))
        axis_lengths.append(sqrt(10 * w))
    return axis_lengths
    
    gc.collect()

def matrot_3d(v0,v1,v2,theta):  # Rodrigues matrix to rotate elements.
    v = np.array([v0,v1,v2])
    v_len = np.linalg.norm(v)
    if v_len==0:
        raise ValueError("length of rotation axis cannot be zero.")
    vu = v / v_len
    W = np.array([[0, -vu[2], vu[1]],
                     [vu[2], 0, -vu[0]],
                     [-vu[1], vu[0], 0]])

    rotmat_3d = np.identity(3) + W * np.sin(theta) + np.dot(W, W) * (1.0 - np.cos(theta))
    
    return rotmat_3d
    
# Calculate the new position of each voxel for the rotated valve.
def rot_elem(x_o,y_o,z_o,v_0,v_1,v_2,vec,theta):    
    p0 = np.array([x_o,y_o,z_o])
    v0 = p0 - vec #c_coord_miV
    m = matrot_3d(v_0,v_1,v_2,theta)#pcax_miV[1,0],pcax_miV[1,1],pcax_miV[1,2],angle)
    v1 = v0.dot(m)
    p1 = v1 + vec
    
    return p1

# Thins the valves before assembling them into the mixed file.
def thin_valve(mask):
    # CON cv2
    #eroded_mask = cv2.erode(mask,np.ones((3,3),np.uint8,iterations=2)

    # CON scipy
    eroded_mask = ndimage.binary_erosion(mask,structure=np.ones((3,3,3)),iterations=2).astype(mask.dtype)

    return eroded_mask

    gc.collect()

# Subroutine which will both split the valves and clean the miocardium around them.
def valve_split(barefile,valve_list):
    img = nib.load(pwd+'/mix/'+barefile+'_mix_0.nii.gz')
    img_d = img.get_fdata()
    valve_mask_d = np.zeros((img.shape[0],img.shape[1],img.shape[2]))
    
    for valve in valve_list:

        valve_d = (img_d == valve) * img_d
        vox_ind = np.argwhere(valve_d)
        pca_v = PCA(n_components=3)
        pca_v.fit(vox_ind)
        pcax_v = pca_v.components_
        valve_m =label(valve_d)
        reg_valve = regionprops(valve_m)
        for rvalve in reg_valve:
            print(f'  Bounding box: {rvalve.centroid}')
            print(f'  Major axis length: {rvalve.axis_major_length}')
            print(f'  Inert_tensors: {rvalve.inertia_tensor_eigvals}')
            
        Axlen_all = ellipsoid_axis_lengths(rvalve.inertia_tensor_eigvals)
        ax_0 = Axlen_all[0]*pcax_v[0] / 2
        ax_1 = Axlen_all[1]*pcax_v[1] / 2
        ax_2 = Axlen_all[0]*pcax_v[2] / 2
        
        c_coord = rvalve.centroid  # centroid coordinates
        c_coord_int =(int(round(c_coord[0])),int(round(c_coord[1])),int(round(c_coord[2])))
        
        maxis_l = rvalve.axis_major_length
        maxis_l_int = int(round(rvalve.axis_major_length))
        p1_v = c_coord
        p2_v = c_coord + pcax_v[1,:]
        p3_v = c_coord + pcax_v[2,:]
        p_v_a, p_v_b, p_v_c, p_v_d = get_plane_equation(p1_v,p2_v,p3_v)
        img_clone_d = np.zeros((img.shape[0],img.shape[1],img.shape[2]))

        for x in range(c_coord_int[0]-maxis_l_int,c_coord_int[0]+maxis_l_int):
            for y in range(c_coord_int[1]-maxis_l_int,c_coord_int[1]+maxis_l_int):
                for z in range(c_coord_int[2]-maxis_l_int,c_coord_int[2]+maxis_l_int):
                    if (p_v_a * x + p_v_b * y + p_v_c * z + p_v_d >= 0) and img_d[x,y,z]==valve:
                        img_clone_d[x,y,z] = valve
                    if into_spheroid(x,y,z,c_coord,ax_0,ax_1,ax_2) == True:
                        if img_d[x,y,z] == 181:
                            img_d[x,y,z] = 151
                        if img_d[x,y,z] == 182:
                            img_d[x,y,z] = 152
                        if img_d[x,y,z] == 156:
                            img_d[x,y,z] = 153
                        if img_d[x,y,z] == 184:
                            img_d[x,y,z] = 154
                    
        valve_2 = valve+10
    
        img_clone_d_2 = (valve_d - img_clone_d) * valve_2 / valve
        valve_mask_d = valve_mask_d + img_clone_d + img_clone_d_2
    
        img_d = img_d - valve_d
        
    valve_mix_1 = nib.Nifti1Image(img_d + valve_mask_d, img.affine)
    nib.save(valve_mix_1,pwd+'/mix/'+barefile+'_mix_1.nii.gz')

#    return img_d, valve_mask_d, img.affine
    gc.collect()

# Rotate the valves and put the rotated ones in a new file, this can be modified and expanded to give an output and include it into another segmented image.
def valve_rot(barefile,angle,valve_list):

    print('angle_rad',angle)
    img0 = nib.load(pwd+'/mix/'+barefile+'_mix_0.nii.gz')
    img1 = nib.load(pwd+'/mix/'+barefile+'_mix_1.nii.gz')
    img0_d = img0.get_fdata()
    img1_d = img1.get_fdata()

    valve_rot_d = np.zeros((img0.shape[0],img0.shape[1],img0.shape[2]))
    
    for valve in valve_list:

        valve_d = (img0_d == valve) * img0_d
        vox_ind = np.argwhere(valve_d)
        pca_v = PCA(n_components=3)
        pca_v.fit(vox_ind)
        pcax_v = pca_v.components_
        valve_m =label(valve_d)
        reg_valve = regionprops(valve_m)
        for rvalve in reg_valve:
            print(f'  Centroid_r: {rvalve.centroid}')
            print(f'  Major axis length_r: {rvalve.axis_major_length}')

        c_coord = rvalve.centroid  # centroid coordinates
        c_coord_int =(int(round(c_coord[0])),int(round(c_coord[1])),int(round(c_coord[2])))
        
        maxis_l = rvalve.axis_major_length
        maxis_l_int = int(round(rvalve.axis_major_length))
        v0_valve = pcax_v[0,:] * maxis_l / 2
        p_valve_plus = c_coord + v0_valve
        p_valve_minus = c_coord - v0_valve
        valve_2 = valve +10
        valve_rot_d_a = np.zeros((img0.shape[0],img0.shape[1],img0.shape[2]))
        valve_rot_d_b = np.zeros((img0.shape[0],img0.shape[1],img0.shape[2]))
        for x in range(c_coord_int[0]-maxis_l_int,c_coord_int[0]+maxis_l_int):
            for y in range(c_coord_int[1]-maxis_l_int,c_coord_int[1]+maxis_l_int):
                for z in range(c_coord_int[2]-maxis_l_int,c_coord_int[2]+maxis_l_int):
                    if img1_d[x,y,z]==valve:
                        p1 = rot_elem(x,y,z,pcax_v[1,0],pcax_v[1,1],pcax_v[1,2],p_valve_minus,-angle)
                        valve_rot_d_a[int(round(p1[0])),int(round(p1[1])),int(round(p1[2]))] = 1.0
                    if img1_d[x,y,z]==valve_2:
                        p1 = rot_elem(x,y,z,pcax_v[1,0],pcax_v[1,1],pcax_v[1,2],p_valve_plus,angle)
                        valve_rot_d_b[int(round(p1[0])),int(round(p1[1])),int(round(p1[2]))] = 1.0
        # Closiong with cv2
        #kernel = np.ones((3,3),np.uint8)
        #valve_rot_d_a = cv2.morphologyEx(valve_rot_d_a, cv2.MORPH_CLOSE, kernel)
        
        # Closiong with scipy
        valve_rot_d_a = ndimage.binary_closing(valve_rot_d_a, structure=np.ones((3,3,3))).astype(valve_rot_d_a.dtype) * valve
        valve_rot_d_b = ndimage.binary_closing(valve_rot_d_b, structure=np.ones((3,3,3))).astype(valve_rot_d_a.dtype) * valve_2
    
        valve_rot_d = valve_rot_d + valve_rot_d_a + valve_rot_d_b
    
    return valve_rot_d, img0.affine
    

gc.collect()
