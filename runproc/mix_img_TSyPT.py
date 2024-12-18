import argparse
import os
import glob
import nibabel as nib
import numpy as np
import statistics as st
import gc
#from scipy import stats

## NOTE: WE MIGHT BE ABLE TO REDUCE COMPUTING TIME GREATLY BY EMPTYING A SPHERE AROUND THE HEART (Use Platipy's heart centroid as centre), RUNNING THE CHOICE PART THERE AND THEN COPYING THAT PIECE BACK INTO THE TS BASE, IT REQUIRES A BIT OF REPROGRAMMING THOUGH.

gc.collect()

parser = argparse.ArgumentParser()
parser.add_argument("--flungs",default="none", action='store_true')
parser.add_argument("--fheart",default="none", action='store_true')
parser.add_argument("--hvalves",default="none", action='store_true')
parser.add_argument("--harteries",default="none", action='store_true')
parser.add_argument("-o", "--Output", help = "Esto solo deberia aparecer si el directorio used no existe")
args=parser.parse_args()

pwd = os.getcwd()
pwdsts = os.getcwd()+'/segms/TS/'
pwdspt = os.getcwd()+'/segms/PT/'
pwdsmo = os.getcwd()+'/segms/MO/'


hstrut = [61,151,152,153,154,156,181,182,184]  # Main carcdiac structures.
hart = [162,163,164,165]  # Coronary arteries, priorized over structures if they are present, but not over the valves.
llobes = [10,11,12,13,14]  # Bronchii are prioritize over the lungs or lung lobes.
hvalv = [167,168,169,170]  # Cardiac valves, maximum priority over anything else.

def checklist(lis,tup):
    for hv in tup:
        if hv in lis:
            return True

name = args.Output
barename = name.replace("used/","")
print("Assembling "+barename)

TSfiles = glob.glob(pwdsts+'TS_'+barename+'_*', recursive=True)
TSfile = pwdsts+'TS_'+barename+'.nii.gz'
PTfiles = glob.glob(pwdspt+'PT_'+barename+'_*', recursive=True)
MOfiles = glob.glob(pwdsmo+'MO_'+barename+'_*', recursive=True)
#    TOTfiles = TSfiles+PTfiles+MOfiles
PARfiles = TSfiles+PTfiles+MOfiles
#print(PARfiles)    ### To check the order of the tensors, which must be in concordance with the order in which the files are included. Index 0 will always be assigned to TotalSegmentator total segmentation. This might be used to assign a label to a voxel in a different way of what I use later on.

# 0 = TS total, 1 = TS body, 2 = TS lung vessels, 3 = PT bronchus - heart arteries, 4 = PT lungs - valves, 5 = PT full heart, 6 = PT heart chambers, 7 = Moose pulmonary artery


TSimg = nib.load(TSfile)
TSimg_d = TSimg.get_fdata()
TS_affine = TSimg.affine
all_img = np.expand_dims(TSimg_d, axis = 0)
print(all_img.shape)
    
for Pfile in PARfiles:
#    print(Pfile)
    img = nib.load(Pfile)
    img_d =img.get_fdata()
    
    img_d_e = np.expand_dims(img_d, axis = 0)
    all_img = np.append(all_img, img_d_e, axis = 0)
    
    
#full_img = nib.Nifti1Image(all_img,TS_affine)
#nib.save(full_img,pwd+'/mix/'+barename+'_mix_0.nii.gz')

        
print(all_img.shape)

res_img_d = np.zeros((all_img.shape[1],all_img.shape[2],all_img.shape[3]))


for x in range(0,all_img.shape[1]):
    for y in range(0,all_img.shape[2]):
        for z in range(0,all_img.shape[3]):

            d = np.unique(all_img[:,x,y,z])
            e = len(d)
            f = []
            g = []
            h = []
            if e == 1:
                res_img_d[x,y,z] = d[0]
            if e == 2:
                res_img_d[x,y,z] = d[-1]
            if e >= 3:
            
                for i in range(0,all_img.shape[0]): #len(all_img[:,x,y,z])):
                    if all_img[i,x,y,z] != 0 and all_img[i,x,y,z] != 140:
                        f.append(all_img[i,x,y,z])
                        res_img_d[x,y,z] = st.mode(f)
                fl =len(f)

                if 16 in d and (150 or 160) in d and checklist(d,llobes) != True:
                    res_img_d[x,y,z] = 16
                if 16 in d and 150 in d and 160 not in d and checklist(d,llobes) == True:
                    for i in range(0,fl):
                        if f[i] != 150:
                            g.append(f[i])
                    res_img_d[x,y,z] = st.mode(g)
                if 160 in d and 16 not in d and (150 or 10 or 11 or 12 or 13 or 14) in d:
                    res_img_d[x,y,z] = 160
                if 16 not in d and 160 not in d and 150 in d and checklist(d,llobes) == True:
                    for i in range(0,fl):
                        if f[i] != 150:
                            g.append(f[i])
                    res_img_d[x,y,z] = st.mode(g)

                if checklist(d,hstrut) == True:
                    for hs in hstrut:
                        if hs in d and checklist(d,hart) != True and checklist(d,hvalv) != True:
                            res_img_d[x,y,z] = hs
                if checklist(d,hart) == True:
                    for ha in hart:
                        if ha in d and checklist(d,hvalv) != True:
                            res_img_d[x,y,z] = ha
                if checklist(d,hvalv) == True:
                    for hv in hvalv:
                        if hv in d:
                            res_img_d[x,y,z] = hv
                if 155 in d and 51 in d:
                    res_img_d[x,y,z] = 155
                # To give both aortic and pulmonary valves a more fitting shape.
#                if 169 in d and 52 in d:
#                    res_img_d[x,y,z] = 52
#                if 170 in d and 155 in d:
#                    res_img_d[x,y,z] = 155


res_img = nib.Nifti1Image(res_img_d,TS_affine)
nib.save(res_img,pwd+'/mix/'+barename+'_mix_0.nii.gz')

gc.collect()
