import argparse
import sys
import shutil
import os
import nibabel as nib
import gc
import reorient_nii
from scipy.ndimage import zoom

gc.collect()

pwd = os.getcwd()

file = sys.argv[1]

print('file = '+file)
barename = file.replace(".nii.gz","")
imgn = nib.load(pwd+'/'+file)
imgn_d = imgn.get_fdata()

pxdm = imgn.header['pixdim']

print('zooming '+barename)
imgn_d_z = zoom(imgn_d,(pxdm[1],pxdm[2],pxdm[3]))
imgn_z = nib.Nifti1Image(imgn_d_z,imgn.affine)

for i in range(1,4):
    imgn_z.header["pixdim"][i] = pxdm[i] / pxdm[i]

imgn_aff = imgn_z.affine
imgn_axcod = nib.aff2axcodes(imgn_aff)
print('ax_codes = ',imgn_axcod)
if imgn_axcod != ('L', 'A', 'S'):
    print(barename+" must be reoriented to 'LAS' and zoomed to 1 mm spacing")
    imgn_r = reorient_nii.reorient(imgn,'LAS')
    nib.save(imgn_r,pwd+'/'+barename+'_r_1mm.nii.gz')
    shutil.move(pwd+'/'+file,pwd+'/orig/reoriented')
else:
    print(barename+" has been zoomed to 1 mm spacing")
    nib.save(imgn_z,pwd+'/'+barename+'_1mm.nii.gz')
    shutil.move(pwd+'/'+file,pwd+'/orig')


    
gc.collect()
