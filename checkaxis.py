import argparse
import sys
import shutil
import os
import nibabel as nib
import gc
import reorient_nii

gc.collect()

pwd = os.getcwd()

file = sys.argv[1]

print('file = '+file)
barename = file.replace(".nii.gz","")
imgn = nib.load(pwd+'/'+file)
imgn_aff = imgn.affine
imgn_axcod = nib.aff2axcodes(imgn_aff)
print('ax_codes = ',imgn_axcod)
if imgn_axcod != ('L', 'A', 'S'):
    print(barename+" must be reoriented to 'LAS'")
    imgn_r = reorient_nii.reorient(imgn,'LAS')
    nib.save(imgn_r,pwd+'/'+barename+'_r.nii.gz')
    shutil.move(pwd+'/'+file,pwd+'/reoriented')
    
gc.collect()
