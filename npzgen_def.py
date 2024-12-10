from skimage import measure
from stl import mesh
import gc
import os
import numpy as np
import nibabel as nib

pwd = os.getcwd()

def pointsgen(image_Z):
    # Use marching cubes to obtain the surface mesh
    verts, faces, normals, values = measure.marching_cubes(image_Z[0,:,:,:],0.5,step_size=1.0)
    # Create the mesh
    data = np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype)
    my_mesh = mesh.Mesh(data, remove_empty_areas=False)
    # Populate the mesh data
    my_mesh.vectors = verts[faces]
    #my_mesh.save('my_mesh.stl')
    #A = mesh.Mesh.from_file("my_mesh.stl")
    #POINTS = np.mean(A.vectors,axis=1)
    POINTS = np.mean(my_mesh.vectors,axis=1) #POINTS over the surface

    return POINTS

    gc.collect()

strut = tuple(range(0,184))  # Este numero hay que cambiarlo si se añaden estructuras al mix.

def XCAT_gen(Xbarename):  # Escoge las estructuras de TS que nos interesan, puede ser necesario tambien para eliminarlas mas adelante.
    print(Xbarename)
        
    mix_img = nib.load(pwd+'/mix/'+Xbarename+'.nii.gz')
    mix_d =mix_img.get_fdata()
    mix_affine = mix_img.affine
    
    XCAT_img_d = np.zeros((mix_img.shape[0],mix_img.shape[1],mix_img.shape[2]))
    
    for i in strut:
        if i == 0:
            XCAT_img_d = XCAT_img_d
        else:
            XCAT_img_d = XCAT_img_d + (mix_d == strut[i]) * mix_d * labels_dataset_mix_XCAT[i] / strut[i]
    print('shape for XCAT img = ',np.shape(XCAT_img_d))

        
    TS_masked_img = nib.Nifti1Image(XCAT_img_d,mix_affine)
    nib.save(TS_masked_img,pwd+'/mix/XCAT_'+Xbarename+'.nii.gz')

def crop_miximg(barename,args):
    if args.noXCAT != True:
        print('generando fichero con etiquetas XCAT')
        XCAT_gen(barename)
        miximg = nib.load(pwd+'/mix/XCAT_'+barename+'_mix_1.nii.gz')
    if args.noXCAT == True:
        print("no se creara un fichero con las etiquetas de XCAT para "+barename)
        miximg = nib.load(pwd+'/mix/'+barename+'_mix_1.nii.gz')
    img = miximg.get_fdata().astype(np.uint8)

    if args.noXCAT == True:
        heart = (img==153).astype(img.dtype)  #LV=153 en mix
    if args.noXCAT != True:
        heart = (img==5).astype(img.dtype)  #LV=1 en XCAT

    from skimage.measure import label, regionprops, regionprops_table
    props = regionprops(heart)
    heart_pos = props[0].centroid
    print("heart_coordinates (z,y,x)= ", heart_pos)

    hepo_z = int(round(heart_pos[2]))
    print('heart posic z ',hepo_z)

    miximg = miximg.slicer[:,:,hepo_z-125:hepo_z+125]

    return miximg, hepo_z

def crop_orimg(barename,hepo_z):
    orimg = nib.load(pwd+'/used/'+barename+'.nii.gz')
    img = orimg.slicer[:,:,hepo_z-125:hepo_z+125]
    
    return img

gc.collect()
