#### This code put into chelist.py allows to resize and zoom the image, resample_volume and the commented parts are related with the try to resize the image to 1 mm spacing and zoom it to have a image of the same physical size. For that, you first need to resample the image with SimpleITK, and then zoom the image with scipy

#from scipy.ndimage import zoom
#import SimpleITK as sitk

#def resample_volume(volume_path, interpolator = sitk.sitkLinear, new_spacing = [1.0, 1.0, 1.0]):
#    volume = sitk.ReadImage(volume_path)
#    original_spacing = volume.GetSpacing()
#    original_size = volume.GetSize()
#    new_size = [int(round(osz*ospc/nspc)) for osz,ospc,nspc in zip(original_size, original_spacing, new_spacing)]
#    return sitk.Resample(volume, new_size, sitk.Transform(), interpolator,
#                         volume.GetOrigin(), new_spacing, volume.GetDirection(), 0,
#                         volume.GetPixelID())



#img = resample_volume(pwd+'/'+file)
#sitk.WriteImage(img, pwd+'/sitk_'+file)


#imgn = nib.load(pwd+'/sitk_'+file)

#pxdm = imgo.header['pixdim']
#print('orig pixdim',pxdm)
#print('sitk pixdim', imgn.header['pixdim'])

#print('zooming '+barename)
#imgn_d_z = zoom(imgn_d,(pxdm[1],pxdm[2],pxdm[3]))
#imgn_z = nib.Nifti1Image(imgn_d_z,imgn.affine)

#os.remove(pwd+'/sitk_'+file)
