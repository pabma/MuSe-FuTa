import argparse
import os
import glob
import nibabel as nib
import numpy as np
import gc
from preproc_def import TS_total, TS_body, TS_bronc, PTlungs, PTstru, PTarte, PTvalv, MOProc, PTmix_1, PTmix_2, MOmix_1, MOmix_2

gc.collect()

# Eliminated the models 'vertebrae', 'fast_vertebrae' as they are incompatible with something in the Platipy or TS segmentators
# Eliminated the models 'fast_organs' and 'fast_cardiac' to avoid overcharge the processor in the creation of the mix file, also, they didn't got the best results
# Eliminated the models 'body', 'body_composition' and 'PUMA4' as their output is currently bad. Check later for possible updates in this models.

models = ('lungs','organs','ribs','muscles','cardiac','digestive','all_bones_v1','PUMA','ALPACA', 'peripheral_bones')

parser = argparse.ArgumentParser(description="options for lungs and heart structures, options fheart and harteries or hvalves are incompatible and would result in strage behaviors")
parser.add_argument("--flungs",default="none", action='store_true', help ='do not show lung lobes, lungs are a single structure')
parser.add_argument("--fheart",default="none", action='store_true', help='do not show any heart structures, only the whole heart')
parser.add_argument("--hvalves",default="none", action='store_true', help ='includes valves and conduits in the heart')
parser.add_argument("--harteries",default="none", action='store_true', help ='includes the arteries which irrigate the heart')
parser.add_argument("-o", "--Output", help = "Esto solo deberia aparecer si el directorio used no existe")
args=parser.parse_args()

pwd = os.getcwd()

#fnames = os.listdir(pwd+'/used')
#print(fnames)

file = args.Output
barefile = file.replace("used/","")
print(barefile)

img = nib.load(pwd+'/used/'+barefile+'.nii.gz')
img_d = img.get_fdata()
img_affine = img.affine
img_m = img_d - img_d
fakeimg = nib.Nifti1Image(img_m,img_affine)

TS_total(barefile,args,fakeimg)
TS_body(barefile,fakeimg)
TS_bronc(barefile,fakeimg)

PTlungs(barefile,fakeimg)
PTstru(barefile,args,fakeimg)
PTarte(barefile,args,fakeimg)
PTvalv(barefile,args,fakeimg)

PTmix_1(barefile)
PTmix_2(barefile)

for model in models:
    MOProc(barefile,args,fakeimg,model)

MOmix_1(barefile)
MOmix_2(barefile)

gc.collect()
