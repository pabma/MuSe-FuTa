import argparse
import os
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cv2
import gc
from class_map_mix import class_map, labels_dataset_mix, labels_dataset_XCAT, labels_dataset_mix_XCAT, class_map_XCAT
from npzgen_def import pointsgen, XCAT_gen, crop_miximg, crop_orimg


gc.collect()

parser = argparse.ArgumentParser(description="option to run with or without XCAT labels, default uses XCAT labels")
parser.add_argument("--noXCAT",default="none", action='store_true', help ='do not run the XCAT transformation and use the bare mixed file to create the npz file')
parser.add_argument("-o", "--Output", help = "Esto solo deberia aparecer si el directorio mix no existe")
args=parser.parse_args()

pwd = os.getcwd()

file = args.Output
barename = file.replace("used/","")
print(barename)


miximg, hepo_z = crop_miximg(barename,args)
img = np.flip(np.swapaxes(miximg.get_fdata().astype(np.uint8),0,2),axis = 1)

orimg = crop_orimg(barename,hepo_z)
CT = np.flip(np.swapaxes(orimg.get_fdata(),0,2),axis = 1)


TISSUE = (CT>-600).astype(np.uint8)  # APLICO UN THRESHOLD PARA ELIMINAR EL AIRE
# LIMPIAMOS LA IMAGEN MEDIANTE EROSION Y DILATACION -- 
kernel = np.ones((7, 7), np.uint8)
TISSUE = cv2.erode(TISSUE, kernel)
TISSUE = cv2.dilate(TISSUE, kernel)


# EN REGION SIN ORGANOS, ASIGNAR VALOR SI ES TEJIDO
if args.noXCAT == True:
    img[(img==0) & (TISSUE==1)] = 140  # 140 para tejido blando no asignado a organo
if args.noXCAT != True:
    img[(img==0) & (TISSUE==1)] = 11  # 11 para tejido blando no asignado a organo

print("shape = ",np.shape(img))
print("Labels in numerical model = ",np.unique(img))
regions = np.unique(img)
print("Organos en Modelo numerico= ")
for i in range(np.size(regions)):
    if args.noXCAT == True:
        print("ID =",regions[i], " Organ= ",class_map[regions[i]])
    if args.noXCAT != True:
        print("ID =",regions[i], " Organ= ",class_map_XCAT[regions[i]])

pxdm = orimg.header['pixdim']
voxel_spacing = [0.1*pxdm[1],0.1*pxdm[2],0.1*pxdm[3]]
#voxel_spacing = [0.1, 0.1, 0.1]


if args.noXCAT == True:
    labels_mix=np.fromiter(class_map.keys(), dtype=int)   #Load the labels saved in the class_map_mix dictionary
    names_mix=class_map.values()
    NLabels = np.max(labels_dataset_mix)+1
if args.noXCAT != True:
    labels_mix=np.fromiter(class_map_XCAT.keys(), dtype=int)   #Load the labels saved in the class_map_mix dictionary for XCAT
    names_mix=class_map_XCAT.values()
    NLabels = np.max(labels_dataset_XCAT)+1

#Read from excel file the labels for the data set
df=pd.read_excel('Thermal_dielectric_acoustic_MR properties_database_V4.2(Excel)_Tv1_sorted.xls',skiprows=[0,1])

names=df.iloc[:,1].to_numpy()
density=df.iloc[:,2].to_numpy()
sos=df.iloc[:,65].to_numpy()
a0=df.iloc[:,75].to_numpy()

density=density[0:NLabels] 
sos=sos[0:NLabels]         
a0=a0[0:NLabels]     

print('density: ',density[0:4]) #Example      

if args.noXCAT == True:
    image_Z = density[labels_dataset_mix[img]]*sos[labels_dataset_mix[img]]
    image_Z[img==51]=2.0*image_Z[img==51]  # MIOCARDIUM -- ESTO NO SERIA MIOCARDIO, SINO PERICARDIO
    image_Z[img==156]=2.0*image_Z[img==156]  # MIOCARDIUM
#    image_Z[img>166]=2.0*image_Z[img>166]  # OTHER CARDIAC MUSCLES
    image_A = a0[labels_dataset_mix]; 
if args.noXCAT != True:
    image_Z = density[labels_dataset_XCAT[img]]*sos[labels_dataset_XCAT[img]]
    image_Z[img==1]=2.0*image_Z[img==1]  # MIOCARDIUM
    image_Z[img==2]=2.0*image_Z[img==2]  # MIOCARDIUM
    image_Z[img==3]=2.0*image_Z[img==3]  # MIOCARDIUM
    image_Z[img==4]=2.0*image_Z[img==4]  # MIOCARDIUM
    image_A = a0[labels_dataset_XCAT]; 


image_L = img   #Using labels directly.  
plt.imshow(np.sum(image_Z[:,:,:],1),'gray');
print(image_Z.dtype,image_A.dtype,image_L.dtype)

if args.noXCAT == True:
    heart = (image_L==153).astype(image_L.dtype)  #LV=153 en mix
if args.noXCAT != True:
    heart = (image_L==5).astype(image_L.dtype)  #LV=1 en XCAT

from skimage.measure import label, regionprops, regionprops_table
props = regionprops(heart)
heart_pos = props[0].centroid
print("heart_coordinates (z,y,x)= ", heart_pos)



### Por ahora todos frames temporales iguales hasta incorporar latido
image_Z = np.tile(image_Z,(10,1,1,1))
image_A = np.tile(image_A,(10,1,1,1))
image_L = np.tile(image_L,(10,1,1,1))

POINTS = pointsgen(image_Z)




# --------- CLOSEST POINT TO HEART --------
NN = np.linalg.norm(POINTS-heart_pos,axis=1)
index = np.argmin(NN)
initial_pos = np.array(POINTS[index,:])
print("initial_pos (z,y,x)= ",initial_pos)


# --- PREPROCESADO ---
from scipy.ndimage import gaussian_filter
image_Zf = np.copy(image_Z)
variability = 0.002

sig = 1.5  #PREFILTERING 0.75
for it in range(np.shape(image_Zf)[0]):
    image_Zf[it,:,:,:] = gaussian_filter(image_Zf[it,:,:,:], sigma=(sig,sig,sig))

image_Zf = image_Zf / np.max(image_Zf)  #Normalized (as only the relative change matters)
image_Zfn = variability*np.random.poisson(image_Zf/variability)

if args.noXCAT == True:
    image_Zfn[(image_L>=151) & (image_L<=154) ] = image_Zf[(image_L>=151) & (image_L<=154)]
    VEIN = np.array((image_L==52) | (image_L==53)).astype(bool)     # Venas, para uso posterior
    ARTERY = np.array((image_L==155) | (image_L==162) | (image_L==163) | (image_L==164) | (image_L==165)).astype(bool)     #Arterias, para uso posterior
    CHAMBER = np.array((image_L==151) | (image_L==152) | (image_L==153) | (image_L==154)).astype(bool)
if args.noXCAT != True:
    image_Zfn[(image_L>=5) & (image_L<=8) ] = image_Zf[(image_L>=5) & (image_L<=8)]
    VEIN = np.array((image_L==43) | (image_L==10)).astype(bool)     # Venas, para uso posterior
    ARTERY = np.array((image_L==42) | (image_L==9)).astype(bool)    #Arterias, para uso posterior
    CHAMBER = np.array((image_L==5) | (image_L==6) | (image_L==7) | (image_L==8)).astype(bool)


#Las venas tienen etiquetas en XCAT de 10 (coronarias) y 43 (resto)
#y las arterias 9 y 42. 
# --------------------------------ADAPTAR -------------------
import fastmorph
from scipy import ndimage

# VENAS  -----
BLOOD = np.zeros_like(VEIN)
for it in range(np.shape(VEIN)[0]):
    BLOOD[it,:,:,:] = fastmorph.erode(VEIN[it,:,:,:])    
VEIN_WALL = np.logical_xor(VEIN,BLOOD)
image_Zfn[BLOOD] = image_Zf[BLOOD]
#plt.figure(figsize=(6,6))
#plt.subplot(121)
#plt.imshow(VEIN[:,:,150,0]);
#plt.subplot(122)
#plt.imshow(BLOOD[:,:,150,0])

# ARTERIAS -----
BLOOD = np.zeros_like(ARTERY)
for it in range(np.shape(ARTERY)[0]):
    BLOOD[it,:,:,:] = fastmorph.erode(ARTERY[it,:,:,:])    
ARTERY_WALL = np.logical_xor(ARTERY,BLOOD)
image_Zfn[BLOOD] = image_Zf[BLOOD]

#CAMARAS DEL CORAZON
BLCHAMBER = np.zeros_like(CHAMBER)
for it in range(np.shape(CHAMBER)[0]):
    BLCHAMBER[it,:,:,:] = fastmorph.erode(CHAMBER[it,:,:,:])
CHAMBER_WALL = np.logical_xor(CHAMBER,BLCHAMBER)
image_Zfn[BLCHAMBER] = image_Zf[BLCHAMBER]




if args.noXCAT == True:
    np.savez_compressed(pwd+'/'+barename+'_mix.npz', image_Z = image_Zfn.astype(np.float32), image_A = image_A.astype(np.float32), image_L = image_L.astype(np.uint8),heart_pos = heart_pos, initial_pos = initial_pos, POINTS = POINTS)
if args.noXCAT != True:
    np.savez_compressed(pwd+'/'+barename+'_XCAT.npz', image_Z = image_Zfn.astype(np.float32), image_A = image_A.astype(np.float32), image_L = image_L.astype(np.uint8),heart_pos = heart_pos, initial_pos = initial_pos, POINTS = POINTS)

gc.collect()
