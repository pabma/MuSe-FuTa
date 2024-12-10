import argparse
import sys
import shutil
import os
import nibabel as nib
import gc
import reorient_nii
import numpy as np
from scipy.ndimage import zoom
#import SimpleITK as sitk

gc.collect()

## resample_volume and the commented parts are related with the try to resize the image to 1 mm spacing and zoom it to have a image of the same physical size. For that, you first need to resample the image with SimpleITK, and then zoom the image with scipy

##def resample_volume(volume_path, interpolator = sitk.sitkLinear, new_spacing = [1.0, 1.0, 1.0]):
##    volume = sitk.ReadImage(volume_path)
##    original_spacing = volume.GetSpacing()
##    original_size = volume.GetSize()
##    new_size = [int(round(osz*ospc/nspc)) for osz,ospc,nspc in zip(original_size, original_spacing, new_spacing)]
##    return sitk.Resample(volume, new_size, sitk.Transform(), interpolator,
##                         volume.GetOrigin(), new_spacing, volume.GetDirection(), 0,
##                         volume.GetPixelID())


pwd = os.getcwd()

file = sys.argv[1]

print('file = '+file)
barename = file.replace(".nii.gz","")

##img = resample_volume(pwd+'/'+file)
##sitk.WriteImage(img, pwd+'/sitk_'+file)

#imgn = nib.load(pwd+'/'+file)
img = nib.load(pwd+'/'+file)
#imgn = nib.load(pwd+'/sitk_'+file)
#imgn_d = imgn.get_fdata()

print('original image shape ',img.shape)

#pxdm = img.header['pixdim']
#print('orig pixdim',pxdm)
#print('sitk pixdim', imgn.header['pixdim'])

print('zooming '+barename)
#imgn_d_z = zoom(imgn_d,(pxdm[1],pxdm[2],pxdm[3]))
#imgn_z = nib.Nifti1Image(imgn_d_z,imgn.affine)

seg_data = img.get_fdata().astype(np.int32)

original_spacing = np.array([pxdm[1],pxdm[2],pxdm[3]])
new_spacing = np.array([1.0, 1.0, 1.0])
zoom_factors = original_spacing / new_spacing

resampled_data = zoom(seg_data, zoom_factors, order=0)

new_affine = img.affine.copy()
# Update the affine's scaling to reflect new spacing
new_affine[0,0] = new_spacing[0] * (new_affine[0,0] / abs(new_affine[0,0]))
new_affine[1,1] = new_spacing[1] * (new_affine[1,1] / abs(new_affine[1,1]))
new_affine[2,2] = new_spacing[2] * (new_affine[2,2] / abs(new_affine[2,2]))

new_img = nib.Nifti1Image(resampled_data, new_affine)
print('new image shape ',new_img.shape)
#pxdm_n = new_img.header['pixdim']
#print('zoomed pixdim',pxdm_n)

imgn_aff = new_img.affine
imgn_axcod = nib.aff2axcodes(imgn_aff)
print('ax_codes = ',imgn_axcod)
if imgn_axcod != ('L', 'A', 'S'):
    print(barename+" must be reoriented to 'LAS' and zoomed to 1 mm spacing")
    imgn_r = reorient_nii.reorient(new_img,'LAS')
    nib.save(imgn_r,pwd+'/'+barename+'_r.nii.gz')
    shutil.move(pwd+'/'+file,pwd+'/reoriented')
else:
    print(barename+" has been zoomed to 1 mm spacing")
    nib.save(imgn_z,pwd+'/'+barename+'_1mm.nii.gz')
    shutil.move(pwd+'/'+file,pwd+'/orig')

#os.remove(pwd+'/sitk_'+file)

gc.collect()
