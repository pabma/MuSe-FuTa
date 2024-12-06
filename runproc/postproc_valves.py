import argparse
import os
import nibabel as nib
import numpy as np
import gc
import cv2
from valves_def import valve_split, valve_rot
import math

gc.collect()
    
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--Output", help = "Esto solo deberia aparecer si el directorio used no existe")
args=parser.parse_args()

pwd = os.getcwd()

file = args.Output
barefile = file.replace("used/","")
print(barefile)

valve_list = [167,168]

img_d, valve_mask_d, img_affine = valve_split(barefile,valve_list)           #### RECORDAR DESCOMENTAR

valve_mix_1 = nib.Nifti1Image(img_d + valve_mask_d, img_affine)           #### RECORDAR DESCOMENTAR
nib.save(valve_mix_1,pwd+'/mix/'+barefile+'_mix_1.nii.gz')           #### RECORDAR DESCOMENTAR



#########################################################
# A PARTIR DE AQUI, GIRO DE VALVULAS
#########################################################
pi = math.pi

angles = [pi/4,pi/3]

for ang in angles:
    valv_rot_d,img_affine = valve_rot(barefile,ang,valve_list)
    valv_r_i = nib.Nifti1Image(valv_rot_d, img_affine)
    ang_s = str(ang)
    nib.save(valv_r_i, barefile+'_valv_rot_'+ang_s+'.nii.gz')

gc.collect()