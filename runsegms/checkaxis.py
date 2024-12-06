import argparse
import sys
import shutil
import os
import nibabel as nib
import gc
import reorient_nii
from scipy.ndimage import zoom
import SimpleITK as sitk

gc.collect()

def resample_volume(volume_path, interpolator = sitk.sitkLinear, new_spacing = [1.0, 1.0, 1.0]):
    volume = sitk.ReadImage(volume_path)
    original_spacing = volume.GetSpacing()
    original_size = volume.GetSize()
    new_size = [int(round(osz*ospc/nspc)) for osz,ospc,nspc in zip(original_size, original_spacing, new_spacing)]
    return sitk.Resample(volume, new_size, sitk.Transform(), interpolator,
                         volume.GetOrigin(), new_spacing, volume.GetDirection(), 0,
                         volume.GetPixelID())


pwd = os.getcwd()

file = sys.argv[1]

print('file = '+file)
barename = file.replace(".nii.gz","")

#img = resample_volume(pwd+'/'+file)
#sitk.WriteImage(img, pwd+'/sitk_'+file)

imgn = nib.load(pwd+'/'+file)
#imgn = nib.load(pwd+'/sitk_'+file)
imgn_d = imgn.get_fdata()

#pxdm = imgo.header['pixdim']
#print('orig pixdim',pxdm)
#print('sitk pixdim', imgn.header['pixdim'])

#print('zooming '+barename)
#imgn_d_z = zoom(imgn_d,(pxdm[1],pxdm[2],pxdm[3]))
#imgn_z = nib.Nifti1Image(imgn_d_z,imgn.affine)

#os.remove(pwd+'/sitk_'+file)

imgn_aff = imgn.affine
imgn_axcod = nib.aff2axcodes(imgn_aff)
print('ax_codes = ',imgn_axcod)
if imgn_axcod != ('L', 'A', 'S'):
    print(barename+" must be reoriented to 'LAS'") # and zoomed to 1 mm spacing")
    imgn_r = reorient_nii.reorient(imgn,'LAS')
    nib.save(imgn_r,pwd+'/'+barename+'_r.nii.gz')
    shutil.move(pwd+'/'+file,pwd+'/reoriented')
#else:
#    print(barename+" has been zoomed to 1 mm spacing")
#    nib.save(imgn_z,pwd+'/'+barename+'_1mm.nii.gz')
#    shutil.move(pwd+'/'+file,pwd+'/orig')
    
gc.collect()
