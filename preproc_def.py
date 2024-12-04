import os
import nibabel as nib
import numpy as np
import gc
import glob
import cv2
from valves_def import thin_valve

#ESTRUCTURAS PARA TOTALSEGMENTATOR
strut = [10,11,12,13,14,61,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115]
invstrut = [0,1,2,3,4,5,6,7,8,9,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,116,117]
lungl = [10,11,12,13,14]
fribs = [92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115]

pwdsts = os.getcwd()+'/segms/TS/'
pwdspt = os.getcwd()+'/segms/PT'
pwdsmo = os.getcwd()+'/segms/MO/'

################## COMIENZA TOTALSEGMENTATOR

def TS_total(TSbarename,args,fakeimg):

#    pwdsts = os.getcwd()+'/segms/TS/'
    if os.path.exists(pwdsts+'TS/'+TSbarename+'.nii'):
        print('Preprocessing TS total for ' + TSbarename)
        
        TS = nib.load(pwdsts+'TS/'+TSbarename+'.nii')
        TS_d =TS.get_fdata()
        TS_affine = TS.affine
        TS_img_d = np.zeros((TS.shape[0],TS.shape[1],TS.shape[2]))

        for st in strut:
            if st in lungl:
                if args.flungs == True:
                    TS_img_d = TS_img_d + (TS_d == st) * TS_d * 150 / st
                if args.flungs != True:
                    TS_img_d = TS_img_d + (TS_d == st) * TS_d
            if st == 61:
                if args.fheart == True:
                    TS_img_d = TS_img_d + (TS_d == 61) * TS_d * 51 / 61
                if args.fheart != True:
                    TS_img_d = TS_img_d + (TS_d == 61) * TS_d
            if st in fribs:
                TS_img_d = TS_img_d + (TS_d == st) * TS_d * 159 / st
        for ist in invstrut:
            TS_img_d = TS_img_d + (TS_d == ist) * TS_d

        
        TS_masked_img = nib.Nifti1Image(TS_img_d,TS_affine)
        nib.save(TS_masked_img,pwdsts+'/TS_'+TSbarename+'.nii.gz')
        
        gc.collect()

    else:
        print('path to: '+pwdsts+'TS/'+TSbarename+'.nii'+" does not exist, creating fake files")
        nib.save(fakeimg,pwdsts+'/TS_'+TSbarename+'_F.nii.gz')
        gc.collect()



def TS_body(TSbarename,fakeimg):

    if os.path.exists(pwdsts+'TS/'+TSbarename+'_b.nii'):
        print('Preprocessing TS body for ' + TSbarename)
        
        TSb = nib.load(pwdsts+'TS/'+TSbarename+'_b.nii')
        TSb_d =TSb.get_fdata()
        TSb_affine = TSb.affine
        
        TSb_t = (TSb_d == 1) * TSb_d * 140
        TSb_e = (TSb_d == 2) * TSb_d * 140 / 2

        TSb_mask = TSb_t + TSb_e
        
        TSb_masked_img = nib.Nifti1Image(TSb_mask,TSb_affine)
        nib.save(TSb_masked_img,pwdsts+'/TS_'+TSbarename+'_b.nii.gz')
        
        gc.collect()

    else:
        print('path to: '+pwdsts+'TS/'+TSbarename+'_b.nii'+" does not exist, creating fake files")
        nib.save(fakeimg,pwdsts+'/TS_'+TSbarename+'_F_b.nii.gz')
        gc.collect()



def TS_bronc(TSbarename,fakeimg):

    if os.path.exists(pwdsts+'TS/'+TSbarename+'_lv.nii'):
        print('Preprocessing TS lung vessels for ' + TSbarename)
        
        TSlv = nib.load(pwdsts+'TS/'+TSbarename+'_lv.nii')
        TSlv_d =TSlv.get_fdata()
        TSlv_affine = TSlv.affine
        
        TSlv_b1 = (TSlv_d == 1) * TSlv_d * 160
        TSlv_b2 = (TSlv_d == 2) * TSlv_d * 160 / 2

        TSlv_mask = TSlv_b1 + TSlv_b2
        
        TSlv_masked_img = nib.Nifti1Image(TSlv_mask,TSlv_affine)
        nib.save(TSlv_masked_img,pwdsts+'/TS_'+TSbarename+'_lv.nii.gz')
        
        gc.collect()

    else:
        print('path to: '+pwdsts+'TS/'+TSbarename+'_lv.nii'+" does not exist, creating fake files")
        nib.save(fakeimg,pwdsts+'/TS_'+TSbarename+'_F_lv.nii.gz')
        gc.collect()





############# COMIENZA PLATIPY


        
def PTlungs(barename,fakeimg):
    
#    pwdspt = os.getcwd()+'/segms/PT/'
    if os.path.exists(pwdspt+'/'+barename):
        print('Preprocessing PT-respiratory for ' + barename)
    
        if os.path.exists(pwdspt+'/'+barename+'/Auto_Lung.nii.gz'):
            PT_l = nib.load(pwdspt+'/'+barename+'/Auto_Lung.nii.gz')
            PT_l_d = PT_l.get_fdata() * 150
            PT_affine = PT_l.affine
            PT_l_masked_img = nib.Nifti1Image(PT_l_d,PT_affine)
            nib.save(PT_l_masked_img,pwdspt+'/prePT_'+barename+'_l.nii.gz')
        else:
            print('path to: '+pwdspt+'/'+barename+"/Auto_Lung.nii.gz does not exist, creating empty file")
            nib.save(fakeimg,pwdspt+'/prePT_'+barename+'_F_l.nii.gz')
        
        if os.path.exists(pwdspt+'/'+barename+'/Auto_Bronchus.nii.gz'):
            PT_b = nib.load(pwdspt+'/'+barename+'/Auto_Bronchus.nii.gz')
            PT_b_d = PT_b.get_fdata() * 160
            PT_affine = PT_l.affine
            PT_b_masked_img = nib.Nifti1Image(PT_b_d,PT_affine)
            nib.save(PT_b_masked_img,pwdspt+'/prePT_'+barename+'_b.nii.gz')
        else:
            print('path to: '+pwdspt+'/'+barename+"/Auto_Bronchus.nii.gz does not exist, creating empty file")
            nib.save(fakeimg,pwdspt+'/prePT_'+barename+'_F_b.nii.gz')
        
        gc.collect()

    else:
        print('path to: '+pwdspt+'/'+barename+" does not exist, creating fake empty files")
        nib.save(fakeimg,pwdspt+'/prePT_'+barename+'_F_l.nii.gz')
        nib.save(fakeimg,pwdspt+'/prePT_'+barename+'_F_b.nii.gz')
        gc.collect()



def PTstru(barename,args,fakeimg):

#    pwdspt = os.getcwd()+'/segms/PT/'
    if os.path.exists(pwdspt+'/'+barename):
        print('Preprocessing PT-structures for ' + barename)
        
        PT_h = nib.load(pwdspt+'/'+barename+'/Heart.nii.gz')
        PT_h_d = PT_h.get_fdata() * 51
     
        PT_atrL = nib.load(pwdspt+'/'+barename+'/Atrium_L.nii.gz')
        PT_affine = PT_atrL.affine
        if args.fheart == True:
            PT_atrL_d = PT_atrL.get_fdata() * 51
        if args.fheart != True:
            PT_atrL_d = PT_atrL.get_fdata() * 151
        
        PT_atrR = nib.load(pwdspt+'/'+barename+'/Atrium_R.nii.gz')
        if args.fheart == True:
            PT_atrR_d = PT_atrR.get_fdata() * 51
        if args.fheart != True:
            PT_atrR_d = PT_atrR.get_fdata() * 152
        
        PT_venL = nib.load(pwdspt+'/'+barename+'/Ventricle_L.nii.gz')
        if args.fheart == True:
            PT_venL_d = PT_venL.get_fdata() * 51
        if args.fheart != True:
            PT_venL_d = PT_venL.get_fdata() * 153
        
        PT_venR = nib.load(pwdspt+'/'+barename+'/Ventricle_R.nii.gz')
        if args.fheart == True:
            PT_venR_d = PT_venR.get_fdata() * 51
        if args.fheart != True:
            PT_venR_d = PT_venR.get_fdata() * 154

        PT_h_mask_d = PT_h_d
        PT_ch_mask_d = PT_atrL_d + PT_atrR_d + PT_venL_d + PT_venR_d

        
        PT_h_masked_img = nib.Nifti1Image(PT_h_mask_d,PT_affine)
        nib.save(PT_h_masked_img,pwdspt+'/PT_'+barename+'_h.nii.gz')
       
        PT_ch_masked_img = nib.Nifti1Image(PT_ch_mask_d,PT_affine)
        nib.save(PT_ch_masked_img,pwdspt+'/PT_'+barename+'_ch.nii.gz')
        
        gc.collect()

    else:
        print('path to: '+pwdspt+'/'+barename+" does not exist, creating fake files")
        nib.save(fakeimg,pwdspt+'/PT_'+barename+'_F_h.nii.gz')
        nib.save(fakeimg,pwdspt+'/PT_'+barename+'_F_ch.nii.gz')
        gc.collect()
        


def PTarte(barename,args,fakeimg):

#    pwdspt = os.getcwd()+'/segms/PT/'
    if os.path.exists(pwdspt+'/'+barename):
        print('Preprocessing PT-coronary_arteries for ' + barename)
        
        PT_a = nib.load(pwdspt+'/'+barename+'/A_Aorta.nii.gz')
        PT_aort_d = PT_a.get_fdata() * 52
        
        PT_vcs = nib.load(pwdspt+'/'+barename+'/V_Venacava_S.nii.gz')
        PT_vcs_d = PT_vcs.get_fdata() * 62
        
        PT_pul_a = nib.load(pwdspt+'/'+barename+'/A_Pulmonary.nii.gz')
        PT_pul_a_d = PT_pul_a.get_fdata() * 155
        
        PT_LADA = nib.load(pwdspt+'/'+barename+'/A_LAD.nii.gz')
        PT_affine = PT_LADA.affine
        if args.harteries == True:
            PT_LADA_d = PT_LADA.get_fdata() * 162
        if args.harteries != True:
            PT_LADA_d = PT_LADA.get_fdata() * 0
        
        PT_cflx = nib.load(pwdspt+'/'+barename+'/A_Cflx.nii.gz')
        if args.harteries == True:
            PT_cflx_d = PT_cflx.get_fdata() * 163
        if args.harteries != True:
            PT_cflx_d = PT_cflx.get_fdata() * 0

        PT_CA_l = nib.load(pwdspt+'/'+barename+'/A_Coronary_L.nii.gz')
        if args.harteries == True:
            PT_CA_l_d = PT_CA_l.get_fdata() * 164
        if args.harteries != True:
            PT_CA_l_d = PT_CA_l.get_fdata() * 0

        PT_CA_r = nib.load(pwdspt+'/'+barename+'/A_Coronary_R.nii.gz')
        if args.harteries == True:
            PT_CA_r_d = PT_CA_r.get_fdata() * 165
        if args.harteries != True:
            PT_CA_r_d = PT_CA_r.get_fdata() * 0
        
        PT_hart_mask_d = PT_LADA_d + PT_cflx_d + PT_CA_l_d + PT_CA_r_d + PT_aort_d + PT_vcs_d + PT_pul_a_d

        PT_hart_masked_img = nib.Nifti1Image(PT_hart_mask_d,PT_affine)
        nib.save(PT_hart_masked_img,pwdspt+'/prePT_'+barename+'_hart.nii.gz')

        gc.collect()

    else:
        print('path to: '+pwdspt+'/'+barename+" does not exist, creating fake empty file")
        nib.save(fakeimg,pwdspt+'/prePT_'+barename+'_F_hart.nii.gz')
        gc.collect()
        
        
        
def PTvalv(barename,args,fakeimg):

#    pwdspt = os.getcwd()+'/segms/PT/'
    if os.path.exists(pwdspt+'/'+barename):
        print('Preprocessing PT-valves for ' + barename)

        PT_miV = nib.load(pwdspt+'/'+barename+'/Valve_Mitral.nii.gz')
        PT_affine = PT_miV.affine
        if args.hvalves == True:
            PT_miV_d = PT_miV.get_fdata() * 167
            PT_miV_d = thin_valve(PT_miV_d)         # PARA ADELGAZAR LA VALVULA MITRAL.
        if args.fheart == True:
            PT_miV_d = PT_miV.get_fdata() * 51
        if args.fheart != True and args.hvalves != True:
            PT_miV_d = PT_miV.get_fdata() * 0

        PT_triV = nib.load(pwdspt+'/'+barename+'/Valve_Tricuspid.nii.gz')
        if args.hvalves == True:
            PT_triV_d = PT_triV.get_fdata() * 168
            PT_triV_d = thin_valve(PT_triV_d)       # PARA ADELGAZAR LA VALVULA TRICUSPIDE.
        if args.fheart == True:
            PT_triV_d = PT_triV.get_fdata() * 51
        if args.fheart != True and args.hvalves != True:
            PT_triV_d = PT_triV.get_fdata() * 0

        PT_aV = nib.load(pwdspt+'/'+barename+'/Valve_Aortic.nii.gz')
        if args.hvalves == True:
            PT_aV_d = PT_aV.get_fdata() * 169
        if args.fheart == True:
            PT_aV_d = PT_aV.get_fdata() * 51
        if args.fheart != True and args.hvalves != True:
            PT_aV_d = PT_aV.get_fdata() * 0

        PT_pV = nib.load(pwdspt+'/'+barename+'/Valve_Pulmonic.nii.gz')
        if args.hvalves == True:
            PT_pV_d = PT_pV.get_fdata() * 170
        if args.fheart == True:
            PT_pV_d = PT_pV.get_fdata() * 51
        if args.fheart != True and args.hvalves != True:
            PT_pV_d = PT_pV.get_fdata() * 0

#        PT_SCN = nib.load(pwdspt+'/'+barename+'/CN_Sinoatrial.nii.gz')
#        if args.hvalves == True:
#            PT_SCN_d = PT_SCN.get_fdata() * 171
#        if args.fheart == True:
#            PT_SCN_d = PT_SCN.get_fdata() * 51
#        if args.fheart != True and args.hvalves != True:
#            PT_SCN_d = PT_SCN.get_fdata() * 0

#        PT_ACN = nib.load(pwdspt+'/'+barename+'/CN_Atrioventricular.nii.gz')
#        if args.hvalves == True:
#            PT_ACN_d = PT_ACN.get_fdata() * 172
#        if args.fheart == True:
#            PT_ACN_d = PT_ACN.get_fdata() * 51
#        if args.fheart != True and args.hvalves != True:
#            PT_ACN_d = PT_ACN.get_fdata() * 0

        PT_VyCN_mask_d = PT_triV_d + PT_miV_d + PT_aV_d + PT_pV_d# + PT_SCN_d + PT_ACN_d  #   SOLAPAN TANTO CON hart COMO con h

        PT_VyCN_masked_img = nib.Nifti1Image(PT_VyCN_mask_d,PT_affine)
        nib.save(PT_VyCN_masked_img,pwdspt+'/prePT_'+barename+'_VyCN.nii.gz')
        
        gc.collect()

    else:
        print('path to: '+pwdspt+'/'+barename+" does not exist, creating fake files")
        nib.save(fakeimg,pwdspt+'/prePT_'+barename+'_F_VyCN.nii.gz')
        gc.collect()



def PTmix_1(barename):
    print('Adding Platipy lungs and valves')
    if os.path.exists(pwdspt+'/prePT_'+barename+'_l.nii.gz'):
        PT_m1_l = nib.load(pwdspt+'/prePT_'+barename+'_l.nii.gz')
    if os.path.exists(pwdspt+'/prePT_'+barename+'_F_l.nii.gz'):
        PT_m1_l = nib.load(pwdspt+'/prePT_'+barename+'_F_l.nii.gz')
    if os.path.exists(pwdspt+'/prePT_'+barename+'_VyCN.nii.gz'):
        PT_m1_v = nib.load(pwdspt+'/prePT_'+barename+'_VyCN.nii.gz')
    if os.path.exists(pwdspt+'/prePT_'+barename+'_F_VyCN.nii.gz'):
        PT_m1_v = nib.load(pwdspt+'/prePT_'+barename+'_F_VyCN.nii.gz')
    PT_m1_d = PT_m1_l.get_fdata()+PT_m1_v.get_fdata()
    PT_affine = PT_m1_l.affine
    PT_m1_masked_img = nib.Nifti1Image(PT_m1_d,PT_affine)
    nib.save(PT_m1_masked_img,pwdspt+'/PT_'+barename+'_1.nii.gz')
    
    gc.collect()



def PTmix_2(barename):
    print('Adding Platipy bronchus and heart arteries')
    if os.path.exists(pwdspt+'/prePT_'+barename+'_b.nii.gz'):
        PT_m2_b = nib.load(pwdspt+'/prePT_'+barename+'_b.nii.gz')
    if os.path.exists(pwdspt+'/prePT_'+barename+'_F_b.nii.gz'):
        PT_m2_b = nib.load(pwdspt+'/prePT_'+barename+'_F_b.nii.gz')
    if os.path.exists(pwdspt+'/prePT_'+barename+'_hart.nii.gz'):
        PT_m2_a = nib.load(pwdspt+'/prePT_'+barename+'_hart.nii.gz')
    if os.path.exists(pwdspt+'/prePT_'+barename+'_F_hart.nii.gz'):
        PT_m2_a = nib.load(pwdspt+'/prePT_'+barename+'_F_hart.nii.gz')
    PT_m2_d = PT_m2_b.get_fdata()+PT_m2_a.get_fdata()
    PT_affine = PT_m2_b.affine
    PT_m2_masked_img = nib.Nifti1Image(PT_m2_d,PT_affine)
    nib.save(PT_m2_masked_img,pwdspt+'/PT_'+barename+'_2.nii.gz')
    
    gc.collect()




########### COMIENZA MOOSE



def MOProc(MObarename,args,fakeimg,model):  # Abre cada uno de los modelos de MOOSE con estructuras interesantes y los reorganiza para asignar a cada estructura una capa propia equivalente a una de TS o a alguna de las nuevas que vamos a introducir.
    
    
    
    if model == 'organs':
                
        if os.path.exists(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz'):
            print('Preprocessing MO model = '+model+' for '+MObarename)

            MO_o = nib.load(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz')
            MO_o_d = MO_o.get_fdata()
            MO_o_affine = MO_o.affine
#            MO_r_d = np.flip(MO_r_d_f, axis = 0) INNECESARIO HACER EL FLIP
            
            if args.flungs == True:
                MO_o_lulL = (MO_o_d == 12) * MO_o_d * 150 / 12
                MO_o_lllL = (MO_o_d == 9) * MO_o_d * 150 / 9
                MO_o_lulR = (MO_o_d == 13) * MO_o_d * 150 / 13
                MO_o_lmlR = (MO_o_d == 11) * MO_o_d * 150 / 11
                MO_o_lllR = (MO_o_d == 10) * MO_o_d * 150 / 10
            if args.flungs != True:
                MO_o_lulL = (MO_o_d == 12) * MO_o_d * 10 / 12
                MO_o_lllL = (MO_o_d == 9) * MO_o_d * 11 / 9
                MO_o_lulR = (MO_o_d == 13) * MO_o_d * 12 / 13
                MO_o_lmlR = (MO_o_d == 11) * MO_o_d * 13 / 11
                MO_o_lllR = (MO_o_d == 10) * MO_o_d * 14 / 10
            
            MO_o_adrl = (MO_o_d == 1) * MO_o_d * 9
            MO_o_adrr = (MO_o_d == 2) * MO_o_d * 8 / 2
            MO_o_blad = (MO_o_d == 3) * MO_o_d * 21 / 3
            MO_o_brai = (MO_o_d == 4) * MO_o_d * 90 / 4
            MO_o_galb = (MO_o_d == 5) * MO_o_d * 4 / 5
            MO_o_kidl = (MO_o_d == 6) * MO_o_d * 3 / 6
            MO_o_kidr = (MO_o_d == 7) * MO_o_d * 2 / 7
            MO_o_live = (MO_o_d == 8) * MO_o_d * 5 / 8
            
            MO_o_panc = (MO_o_d == 14) * MO_o_d * 7 / 14
            MO_o_sple = (MO_o_d == 15) * MO_o_d / 15
            MO_o_stom = (MO_o_d == 16) * MO_o_d * 6 / 16
            MO_o_trac = (MO_o_d == 19) * MO_o_d * 16 / 19
                
            MO_o_mask_d = MO_o_adrl + MO_o_adrr + MO_o_blad + MO_o_brai + MO_o_galb + MO_o_kidl + MO_o_kidr + MO_o_live + MO_o_lulL + MO_o_lllL + MO_o_lulR + MO_o_lmlR + MO_o_lllR + MO_o_panc + MO_o_sple + MO_o_stom + MO_o_trac
                
            MO_o_masked_img = nib.Nifti1Image(MO_o_mask_d,MO_o_affine)
            nib.save(MO_o_masked_img,pwdsmo+'MO_'+MObarename+'_o.nii.gz')
                    
            gc.collect()
                    
        else:
            print('path to: '+pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz does not exist, creating fake files')
            nib.save(fakeimg,pwdsmo+'MO_'+MObarename+'_F_o.nii.gz')
            gc.collect()
            
            
    
    if model == 'lungs':
                
        if os.path.exists(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz'):
            print('Preprocessing MO model = '+model+' for '+MObarename)

            MO_l = nib.load(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz')
            MO_l_d = MO_l.get_fdata()
            MO_l_affine = MO_l.affine
#            MO_r_d = np.flip(MO_r_d_f, axis = 0) INNECESARIO HACER EL FLIP


            if args.flungs == True:
                MO_l_lulL = (MO_l_d == 1) * MO_l_d * 150
                MO_l_lllL = (MO_l_d == 2) * MO_l_d * 150 / 2
                MO_l_lulR = (MO_l_d == 3) * MO_l_d * 150 / 3
                MO_l_lmlR = (MO_l_d == 4) * MO_l_d * 150 / 4
                MO_l_lllR = (MO_l_d == 5) * MO_l_d * 150 / 5
            if args.flungs != True:
                MO_l_lulL = (MO_l_d == 1) * MO_l_d * 10
                MO_l_lllL = (MO_l_d == 2) * MO_l_d * 11 / 2
                MO_l_lulR = (MO_l_d == 3) * MO_l_d * 12 / 3
                MO_l_lmlR = (MO_l_d == 4) * MO_l_d * 13 / 4
                MO_l_lllR = (MO_l_d == 5) * MO_l_d * 14 / 5
                
            MO_l_mask_d = MO_l_lulL + MO_l_lllL + MO_l_lulR + MO_l_lmlR + MO_l_lllR
              
              
            MO_l_masked_img = nib.Nifti1Image(MO_l_mask_d,MO_l_affine)
            nib.save(MO_l_masked_img,pwdsmo+'MO_'+MObarename+'_l.nii.gz')
                    
            gc.collect()
                    
        else:
            print('path to: '+pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz does not exist, creating fake files')
            nib.save(fakeimg,pwdsmo+'MO_'+MObarename+'_F_l.nii.gz')
            gc.collect()
                
                
                
    if model == 'ribs':
#            print(pwdsmo+MObarename+'/'+model)
                
        if os.path.exists(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz'):
            print('Preprocessing MO model = '+model+' for '+MObarename)

            MO_r = nib.load(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz')
            MO_r_d = MO_r.get_fdata()
            MO_r_affine = MO_r.affine
#                    MO_r_d = np.flip(MO_r_d_f, axis = 0) INNECESARIO HACER EL FLIP

        ### Costillas incluidas en una sola etiqueta para que dejen de dar la lata.
            MO_r_rL01 = (MO_r_d == 14) * MO_r_d * 159 / 14
            MO_r_rL02 = (MO_r_d == 15) * MO_r_d * 159 / 15
            MO_r_rL03 = (MO_r_d == 16) * MO_r_d * 159 / 16
            MO_r_rL04 = (MO_r_d == 17) * MO_r_d * 159 / 17
            MO_r_rL05 = (MO_r_d == 18) * MO_r_d * 159 / 18
            MO_r_rL06 = (MO_r_d == 19) * MO_r_d * 159 / 19
            MO_r_rL07 = (MO_r_d == 20) * MO_r_d * 159 / 20
            MO_r_rL08 = (MO_r_d == 21) * MO_r_d * 159 / 21
            MO_r_rL09 = (MO_r_d == 22) * MO_r_d * 159 / 22
            MO_r_rL10 = (MO_r_d == 23) * MO_r_d * 159 / 23
            MO_r_rL11 = (MO_r_d == 24) * MO_r_d * 159 / 24
            MO_r_rL12 = (MO_r_d == 25) * MO_r_d * 159 / 25
            MO_r_rR01 = (MO_r_d == 1) * MO_r_d * 159
            MO_r_rR02 = (MO_r_d == 2) * MO_r_d * 159 / 2
            MO_r_rR03 = (MO_r_d == 3) * MO_r_d * 159 / 3
            MO_r_rR04 = (MO_r_d == 4) * MO_r_d * 159 / 4
            MO_r_rR05 = (MO_r_d == 5) * MO_r_d * 159 / 5
            MO_r_rR06 = (MO_r_d == 6) * MO_r_d * 159 / 6
            MO_r_rR07 = (MO_r_d == 7) * MO_r_d * 159 / 7
            MO_r_rR08 = (MO_r_d == 8) * MO_r_d * 159 / 8
            MO_r_rR09 = (MO_r_d == 9) * MO_r_d * 159 / 9
            MO_r_rR10 = (MO_r_d == 10) * MO_r_d * 159 / 10
            MO_r_rR11 = (MO_r_d == 11) * MO_r_d * 159 / 11
            MO_r_rR12 = (MO_r_d == 12) * MO_r_d * 159 / 12
                    
            MO_r_ster = (MO_r_d == 27) * MO_r_d * 116 / 27
                    
            MO_r_mask_d = MO_r_rL01 +MO_r_rL02 + MO_r_rL03 + MO_r_rL04 + MO_r_rL05 + MO_r_rL06 + MO_r_rL07 + MO_r_rL08 + MO_r_rL09 + MO_r_rL10 + MO_r_rL11 + MO_r_rL12 + MO_r_rR01 + MO_r_rR02 + MO_r_rR03 + MO_r_rR04 + MO_r_rR05 + MO_r_rR06 + MO_r_rR07 + MO_r_rR08 + MO_r_rR09 + MO_r_rR10 + MO_r_rR11 + MO_r_rR12 + MO_r_ster
                
            MO_r_masked_img = nib.Nifti1Image(MO_r_mask_d,MO_r_affine)
            nib.save(MO_r_masked_img,pwdsmo+'MO_'+MObarename+'_r.nii.gz')
                    
            gc.collect()
                    
        else:
            print('path to: '+pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz does not exist, creating fake files')
            nib.save(fakeimg,pwdsmo+'MO_'+MObarename+'_F_r.nii.gz')
            gc.collect()



    if model == 'muscles':
                
        if os.path.exists(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz'):
            print('Preprocessing MO model = '+model+' for '+MObarename)

            MO_m = nib.load(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz')
            MO_m_d = MO_m.get_fdata()
            MO_m_affine = MO_m.affine
#            MO_r_d = np.flip(MO_r_d_f, axis = 0) INNECESARIO HACER EL FLIP


            MO_m_autl = (MO_m_d == 1) * MO_m_d * 86
            MO_m_autr = (MO_m_d == 2) * MO_m_d * 87 / 2
                
            MO_m_mask_d = MO_m_autl + MO_m_autr
            
            MO_m_masked_img = nib.Nifti1Image(MO_m_mask_d,MO_m_affine)
            nib.save(MO_m_masked_img,pwdsmo+'preMO_'+MObarename+'_m.nii.gz')
                    
            gc.collect()
                    
        else:
            print('path to: '+pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz does not exist, creating fake files')
            nib.save(fakeimg,pwdsmo+'preMO_'+MObarename+'_F_m.nii.gz')
            gc.collect()
            
            
            
    if model == 'peripheral_bones':
                
        if os.path.exists(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz'):
            print('Preprocessing MO model = '+model+' for '+MObarename)

            MO_pb = nib.load(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz')
            MO_pb_d = MO_pb.get_fdata()
            MO_pb_affine = MO_pb.affine
#            MO_r_d = np.flip(MO_r_d_f, axis = 0) INNECESARIO HACER EL FLIP


            MO_pb_clal = (MO_pb_d == 3) * MO_pb_d * 73 / 3
            MO_pb_clar = (MO_pb_d == 4) * MO_pb_d * 74 / 4
            MO_pb_feml = (MO_pb_d == 5) * MO_pb_d * 75 / 5
            MO_pb_femr = (MO_pb_d == 6) * MO_pb_d * 76 / 6
            MO_pb_huml = (MO_pb_d == 11) * MO_pb_d * 69 / 11
            MO_pb_humr = (MO_pb_d == 12) * MO_pb_d * 70 / 12
            MO_pb_scal = (MO_pb_d == 21) * MO_pb_d * 71 / 21
            MO_pb_scar = (MO_pb_d == 22) * MO_pb_d * 72 / 22
            MO_pb_skul = (MO_pb_d == 23) * MO_pb_d * 91 / 23
                
            MO_pb_mask_d = MO_pb_clal + MO_pb_clar + MO_pb_feml + MO_pb_femr + MO_pb_huml + MO_pb_humr + MO_pb_scal + MO_pb_scar + MO_pb_skul
            
            MO_pb_masked_img = nib.Nifti1Image(MO_pb_mask_d,MO_pb_affine)
            nib.save(MO_pb_masked_img,pwdsmo+'preMO_'+MObarename+'_pb.nii.gz')
                    
            gc.collect()
                    
        else:
            print('path to: '+pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz does not exist, creating fake files')
            nib.save(fakeimg,pwdsmo+'preMO_'+MObarename+'_F_pb.nii.gz')
            gc.collect()
            
            
            
    if model == 'cardiac':
                
        if os.path.exists(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz'):
            print('Preprocessing MO model = '+model+' for '+MObarename)

            MO_c = nib.load(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz')
            MO_c_d = MO_c.get_fdata()
            MO_c_affine = MO_c.affine
                
            MO_c_aort = (MO_c_d == 6) * MO_c_d * 52 / 6
            MO_c_invc = (MO_c_d == 11) * MO_c_d * 63 / 11
            MO_c_pslv = (MO_c_d == 12) * MO_c_d * 64 / 12
            MO_c_pula = (MO_c_d == 13) * MO_c_d * 155 / 13
                
            if args.fheart == True:
                MO_c_myoc = (MO_c_d == 1) * MO_c_d * 51
                MO_c_atrL = (MO_c_d == 2) * MO_c_d * 51 / 2
                MO_c_atrR = (MO_c_d == 3) * MO_c_d * 51 / 3
                MO_c_venL = (MO_c_d == 4) * MO_c_d * 51 / 4
                MO_c_venR = (MO_c_d == 5) * MO_c_d * 51 / 5
            if args.fheart != True:
                MO_c_myoc = (MO_c_d == 1) * MO_c_d * 156
                MO_c_atrL = (MO_c_d == 2) * MO_c_d * 151 / 2
                MO_c_atrR = (MO_c_d == 3) * MO_c_d * 152 / 3
                MO_c_venL = (MO_c_d == 4) * MO_c_d * 153 / 4
                MO_c_venR = (MO_c_d == 5) * MO_c_d * 154 / 5
                
            MO_c_mask_d = MO_c_myoc + MO_c_atrL + MO_c_atrR + MO_c_venL + MO_c_venR + MO_c_aort +MO_c_invc + MO_c_pslv + MO_c_pula
                
            MO_c_masked_img = nib.Nifti1Image(MO_c_mask_d,MO_c_affine)
            nib.save(MO_c_masked_img,pwdsmo+'preMO_'+MObarename+'_c.nii.gz')
                    
            gc.collect()
                    
        else:
            print('path to: '+pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz does not exist, creating fake files')
            nib.save(fakeimg,pwdsmo+'preMO_'+MObarename+'_F_c.nii.gz')
            gc.collect()
            
            
        
    if model == 'digestive':
                
        if os.path.exists(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz'):
            print('Preprocessing MO model = '+model+' for '+MObarename)

            MO_d = nib.load(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz')
            MO_d_d = MO_d.get_fdata()
            MO_d_affine = MO_d.affine
            
            MO_d_colo = (MO_d_d == 1) * MO_d_d * 20
            MO_d_duod = (MO_d_d == 2) * MO_d_d * 19 / 2
            MO_d_esop = (MO_d_d == 3) * MO_d_d * 15 / 3
            MO_d_smbo = (MO_d_d == 4) * MO_d_d * 18 / 4
                
            MO_d_mask_d = MO_d_colo + MO_d_duod + MO_d_esop + MO_d_smbo
                
            MO_d_masked_img = nib.Nifti1Image(MO_d_mask_d,MO_d_affine)
            nib.save(MO_d_masked_img,pwdsmo+'preMO_'+MObarename+'_d.nii.gz')
                    
            gc.collect()
                    
        else:
            print('path to: '+pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz does not exist, creating fake files')
            nib.save(fakeimg,pwdsmo+'preMO_'+MObarename+'_F_d.nii.gz')
            gc.collect()
            
            
            
    if model == 'all_bones_v1':
                
        if os.path.exists(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz'):
            print('Preprocessing MO model = '+model+' for '+MObarename)

            MO_b = nib.load(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz')
            MO_b_d = MO_b.get_fdata()
            MO_b_affine = MO_b.affine
            
            MO_b_skul = (MO_b_d == 14) * MO_b_d * 91 / 14
            MO_b_ster = (MO_b_d == 16) * MO_b_d * 116 / 16
                
            MO_b_mask_d = MO_b_skul + MO_b_ster
                
            MO_b_masked_img = nib.Nifti1Image(MO_b_mask_d,MO_b_affine)
            nib.save(MO_b_masked_img,pwdsmo+'preMO_'+MObarename+'_b.nii.gz')
                    
            gc.collect()
                    
        else:
            print('path to: '+pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz does not exist, creating fake files')
            nib.save(fakeimg,pwdsmo+'preMO_'+MObarename+'_F_b.nii.gz')
            gc.collect()
            
        
        
    if model == 'PUMA':
                
        if os.path.exists(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz'):
            print('Preprocessing MO model = '+model+' for '+MObarename)

            MO_P = nib.load(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz')
            MO_P_d = MO_P.get_fdata()
            MO_P_affine = MO_P.affine
            
            MO_P_sple = (MO_P_d == 1) * MO_P_d
            MO_P_galb = (MO_P_d == 3) * MO_P_d * 4 / 3
            MO_P_live = (MO_P_d == 4) * MO_P_d * 5 / 4
            MO_P_stom = (MO_P_d == 5) * MO_P_d * 6 / 5
            MO_P_panc = (MO_P_d == 6) * MO_P_d * 7 / 6
            MO_P_lung = (MO_P_d == 8) * MO_P_d * 150 / 8
            MO_P_esop = (MO_P_d == 17) * MO_P_d * 15 / 17
            MO_P_trac = (MO_P_d == 18) * MO_P_d * 16 / 18
            MO_P_brai = (MO_P_d == 20) * MO_P_d * 90 / 20
            MO_P_blad = (MO_P_d == 23) * MO_P_d * 21 / 23
                
            MO_P_invc = (MO_P_d == 16) * MO_P_d * 63 / 16
            MO_P_pula = (MO_P_d == 14) * MO_P_d * 155 / 14
            MO_P_aort = (MO_P_d == 15) * MO_P_d * 52 / 15

            if args.fheart == True:
                MO_P_atrL = (MO_P_d == 10) * MO_P_d * 51 / 10
                MO_P_atrR = (MO_P_d == 12) * MO_P_d * 51 / 12
                MO_P_venL = (MO_P_d == 11) * MO_P_d * 51 / 11
                MO_P_venR = (MO_P_d == 13) * MO_P_d * 51 / 13
                MO_P_myoc = (MO_P_d == 9) * MO_P_d * 51 / 9
            if args.fheart != True:
                MO_P_atrL = (MO_P_d == 10) * MO_P_d * 151 / 10
                MO_P_atrR = (MO_P_d == 12) * MO_P_d * 152 / 12
                MO_P_venL = (MO_P_d == 11) * MO_P_d * 153 / 11
                MO_P_venR = (MO_P_d == 13) * MO_P_d * 154 / 13
                MO_P_myoc = (MO_P_d == 9) * MO_P_d * 156 / 9
                
            MO_P_mask_d = MO_P_sple + MO_P_galb + MO_P_live + MO_P_stom + MO_P_panc + MO_P_lung + MO_P_esop + MO_P_trac + MO_P_invc + MO_P_atrL + MO_P_atrR + MO_P_venL + MO_P_venR + MO_P_pula + MO_P_myoc + MO_P_aort + MO_P_brai + MO_P_blad
                
            MO_P_masked_img = nib.Nifti1Image(MO_P_mask_d,MO_P_affine)
            nib.save(MO_P_masked_img,pwdsmo+'MO_'+MObarename+'_P.nii.gz')
                    
            gc.collect()
                    
        else:
            print('path to: '+pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz does not exist, creating fake files')
            nib.save(fakeimg,pwdsmo+'MO_'+MObarename+'_F_P.nii.gz')
            gc.collect()
            
            
            
    if model == 'ALPACA':
                
        if os.path.exists(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz'):
            print('Preprocessing MO model = '+model+' for '+MObarename)

            MO_A = nib.load(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz')
            MO_A_d = MO_A.get_fdata()
            MO_A_affine = MO_A.affine
            
            MO_A_aort = (MO_A_d == 6) * MO_A_d * 52 / 6
            MO_A_pula = (MO_A_d == 3) * MO_A_d * 155 / 3
                
            if args.fheart == True:
                MO_A_venL = (MO_A_d == 1) * MO_A_d * 51
                MO_A_venR = (MO_A_d == 2) * MO_A_d * 51 / 2
            if args.fheart != True:
                MO_A_venL = (MO_A_d == 1) * MO_A_d * 153
                MO_A_venR = (MO_A_d == 2) * MO_A_d * 154 / 2
                
            MO_A_mask_d = MO_A_aort + MO_A_venL + MO_A_venR + MO_A_pula
                
            MO_A_masked_img = nib.Nifti1Image(MO_A_mask_d,MO_A_affine)
            nib.save(MO_A_masked_img,pwdsmo+'preMO_'+MObarename+'_A.nii.gz')
                    
            gc.collect()
                    
        else:
            print('path to: '+pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz does not exist, creating fake files')
            nib.save(fakeimg,pwdsmo+'preMO_'+MObarename+'_F_A.nii.gz')
            gc.collect()
            
            
            
    if model == 'PUMA4':
                
        if os.path.exists(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz'):
            print('Preprocessing MO model = '+model+' for '+MObarename)

            MO_P4 = nib.load(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz')
            MO_P4_d = MO_P4.get_fdata()
            MO_P4_affine = MO_P4.affine
            
            MO_P4_sple = (MO_P4_d == 1) * MO_P4_d
            MO_P4_galb = (MO_P4_d == 3) * MO_P4_d * 4 / 3
            MO_P4_live = (MO_P4_d == 4) * MO_P4_d * 5 / 4
            MO_P4_stom = (MO_P4_d == 5) * MO_P4_d * 6 / 5
            MO_P4_panc = (MO_P4_d == 6) * MO_P4_d * 7 / 6
            MO_P4_lung = (MO_P4_d == 8) * MO_P4_d * 150 / 8
            MO_P4_hear = (MO_P4_d == 9) * MO_P4_d * 51 / 9
            MO_P4_esop = (MO_P4_d == 11) * MO_P4_d * 15 / 11
            MO_P4_trac = (MO_P4_d == 12) * MO_P4_d * 16 / 12
            MO_P4_smbo = (MO_P4_d == 13) * MO_P4_d * 18 / 13
            MO_P4_duod = (MO_P4_d == 14) * MO_P4_d * 19 / 14
            MO_P4_colo = (MO_P4_d == 15) * MO_P4_d * 20 / 15
            MO_P4_brai = (MO_P4_d == 16) * MO_P4_d * 90 / 16
            MO_P4_subf = (MO_P4_d == 18) * MO_P4_d * 143 / 18
            MO_P4_visf = (MO_P4_d == 19) * MO_P4_d * 142 / 19
            MO_P4_blad = (MO_P4_d == 21) * MO_P4_d
            MO_P4_fill = (MO_P4_d == 22) * MO_P4_d * 140 / 22
                
            MO_P4_mask_d = MO_P4_sple + MO_P4_galb + MO_P4_live + MO_P4_stom + MO_P4_panc + MO_P4_lung + MO_P4_hear + MO_P4_esop + MO_P4_trac + MO_P4_smbo + MO_P4_duod + MO_P4_colo + MO_P4_brai + MO_P4_subf + MO_P4_visf + MO_P4_blad + MO_P4_fill
                
            MO_P4_masked_img = nib.Nifti1Image(MO_P4_mask_d,MO_P4_affine)
            nib.save(MO_P4_masked_img,pwdsmo+'MO_'+MObarename+'_P4.nii.gz')
                    
            gc.collect()
                    
        else:
            print('path to: '+pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz does not exist, creating fake files')
            nib.save(fakeimg,pwdsmo+'MO_'+MObarename+'_F_P4.nii.gz')
            gc.collect()
            
    if model == 'fast_organs':
                
        if os.path.exists(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz'):
            print('Preprocessing MO model = '+model+' for '+MObarename)

            MO_fo = nib.load(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz')
            MO_fo_d = MO_fo.get_fdata()
            MO_fo_affine = MO_fo.affine
#            MO_r_d = np.flip(MO_r_d_f, axis = 0) INNECESARIO HACER EL FLIP
            
            if args.flungs == True:
                MO_fo_lulL = (MO_fo_d == 12) * MO_fo_d * 150 / 12
                MO_fo_lllL = (MO_fo_d == 9) * MO_fo_d * 150 / 9
                MO_fo_lulR = (MO_fo_d == 13) * MO_fo_d * 150 / 13
                MO_fo_lmlR = (MO_fo_d == 11) * MO_fo_d * 150 / 11
                MO_fo_lllR = (MO_fo_d == 10) * MO_fo_d * 150 / 10
            if args.flungs != True:
                MO_fo_lulL = (MO_fo_d == 12) * MO_fo_d * 10 / 12
                MO_fo_lllL = (MO_fo_d == 9) * MO_fo_d * 11 / 9
                MO_fo_lulR = (MO_fo_d == 13) * MO_fo_d * 12 / 13
                MO_fo_lmlR = (MO_fo_d == 11) * MO_fo_d * 13 / 11
                MO_fo_lllR = (MO_fo_d == 10) * MO_fo_d * 14 / 10
            
            MO_fo_adrl = (MO_fo_d == 1) * MO_fo_d * 9
            MO_fo_adrr = (MO_fo_d == 2) * MO_fo_d * 8 / 2
            MO_fo_blad = (MO_fo_d == 3) * MO_fo_d * 21 / 3
            MO_fo_brai = (MO_fo_d == 4) * MO_fo_d * 90 / 4
            MO_fo_galb = (MO_fo_d == 5) * MO_fo_d * 4 / 5
            MO_fo_kidl = (MO_fo_d == 6) * MO_fo_d * 3 / 6
            MO_fo_kidr = (MO_fo_d == 7) * MO_fo_d * 2 / 7
            MO_fo_live = (MO_fo_d == 8) * MO_fo_d * 5 / 8
            
            MO_fo_panc = (MO_fo_d == 14) * MO_fo_d * 7 / 14
            MO_fo_sple = (MO_fo_d == 15) * MO_fo_d / 15
            MO_fo_stom = (MO_fo_d == 16) * MO_fo_d * 6 / 16
            MO_fo_trac = (MO_fo_d == 19) * MO_fo_d * 16 / 19
                
            MO_fo_mask_d = MO_fo_adrl + MO_fo_adrr + MO_fo_blad + MO_fo_brai + MO_fo_galb + MO_fo_kidl + MO_fo_kidr + MO_fo_live + MO_fo_lulL + MO_fo_lllL + MO_fo_lulR + MO_fo_lmlR + MO_fo_lllR + MO_fo_panc + MO_fo_sple + MO_fo_stom + MO_fo_trac
                
            MO_fo_masked_img = nib.Nifti1Image(MO_fo_mask_d,MO_fo_affine)
            nib.save(MO_fo_masked_img,pwdsmo+'MO_'+MObarename+'_fo.nii.gz')
                    
            gc.collect()
                    
        else:
            print('path to: '+pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz does not exist, creating fake files')
            nib.save(fakeimg,pwdsmo+'MO_'+MObarename+'_F_fo.nii.gz')
            gc.collect()
    
    
    
    if model == 'fast_cardiac':
                
        if os.path.exists(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz'):
            print('Preprocessing MO model = '+model+' for '+MObarename)

            MO_fc = nib.load(pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz')
            MO_fc_d = MO_fc.get_fdata()
            MO_fc_affine = MO_fc.affine
                
            MO_fc_aort = (MO_fc_d == 6) * MO_fc_d * 52 / 6
            MO_fc_invc = (MO_fc_d == 11) * MO_fc_d * 63 / 11
            MO_fc_pslv = (MO_fc_d == 12) * MO_fc_d * 64 / 12
            MO_fc_pula = (MO_fc_d == 13) * MO_fc_d * 155 / 13
                
            if args.fheart == True:
                MO_fc_myoc = (MO_fc_d == 1) * MO_fc_d * 51
                MO_fc_atrL = (MO_fc_d == 2) * MO_fc_d * 51 / 2
                MO_fc_atrR = (MO_fc_d == 3) * MO_fc_d * 51 / 3
                MO_fc_venL = (MO_fc_d == 4) * MO_fc_d * 51 / 4
                MO_fc_venR = (MO_fc_d == 5) * MO_fc_d * 51 / 5
            if args.fheart != True:
                MO_fc_myoc = (MO_fc_d == 1) * MO_fc_d * 156
                MO_fc_atrL = (MO_fc_d == 2) * MO_fc_d * 151 / 2
                MO_fc_atrR = (MO_fc_d == 3) * MO_fc_d * 152 / 3
                MO_fc_venL = (MO_fc_d == 4) * MO_fc_d * 153 / 4
                MO_fc_venR = (MO_fc_d == 5) * MO_fc_d * 154 / 5
                
            MO_fc_mask_d = MO_fc_myoc + MO_fc_atrL + MO_fc_atrR + MO_fc_venL + MO_fc_venR + MO_fc_aort +MO_fc_invc + MO_fc_pslv + MO_fc_pula
                
            MO_fc_masked_img = nib.Nifti1Image(MO_fc_mask_d,MO_fc_affine)
            nib.save(MO_fc_masked_img,pwdsmo+'MO_'+MObarename+'_fc.nii.gz')
                    
            gc.collect()
                    
        else:
            print('path to: '+pwdsmo+'MO/clin_CT_'+model+'_segmentation_'+MObarename+'.nii.gz does not exist, creating fake files')
            nib.save(fakeimg,pwdsmo+'MO_'+MObarename+'_F_fc.nii.gz')
            gc.collect()
            
            

def MOmix_1(barename):
    print('Adding Moose3 models all_bones_v1, ALPACA, digestive and muscles')
    if os.path.exists(pwdsmo+'preMO_'+barename+'_b.nii.gz'):
        MO_m1_b = nib.load(pwdsmo+'preMO_'+barename+'_b.nii.gz')
    if os.path.exists(pwdsmo+'preMO_'+barename+'_F_b.nii.gz'):
        MO_m1_b = nib.load(pwdsmo+'preMO_'+barename+'_F_b.nii.gz')
    if os.path.exists(pwdsmo+'preMO_'+barename+'_A.nii.gz'):
        MO_m1_A = nib.load(pwdsmo+'preMO_'+barename+'_A.nii.gz')
    if os.path.exists(pwdsmo+'preMO_'+barename+'_F_A.nii.gz'):
        MO_m1_A = nib.load(pwdsmo+'preMO_'+barename+'_F_A.nii.gz')
    if os.path.exists(pwdsmo+'preMO_'+barename+'_d.nii.gz'):
        MO_m1_d = nib.load(pwdsmo+'preMO_'+barename+'_d.nii.gz')
    if os.path.exists(pwdsmo+'preMO_'+barename+'_F_d.nii.gz'):
        MO_m1_d = nib.load(pwdsmo+'preMO_'+barename+'_F_d.nii.gz')
    if os.path.exists(pwdsmo+'preMO_'+barename+'_m.nii.gz'):
        MO_m1_m = nib.load(pwdsmo+'preMO_'+barename+'_m.nii.gz')
    if os.path.exists(pwdsmo+'preMO_'+barename+'_F_m.nii.gz'):
        MO_m1_m = nib.load(pwdsmo+'preMO_'+barename+'_F_m.nii.gz')
    
    MO_m1_d = MO_m1_b.get_fdata()+MO_m1_A.get_fdata()+MO_m1_d.get_fdata()+MO_m1_m.get_fdata()
    MO_affine = MO_m1_b.affine
    MO_m1_masked_img = nib.Nifti1Image(MO_m1_d,MO_affine)
    nib.save(MO_m1_masked_img,pwdsmo+'MO_'+barename+'_1.nii.gz')
    
    gc.collect()
    
    
    
def MOmix_2(barename):
    print('Adding Moose3 models cardiac and peripheral_bones')
    if os.path.exists(pwdsmo+'preMO_'+barename+'_c.nii.gz'):
        MO_m2_c = nib.load(pwdsmo+'preMO_'+barename+'_c.nii.gz')
    if os.path.exists(pwdsmo+'preMO_'+barename+'_F_c.nii.gz'):
        MO_m2_c = nib.load(pwdsmo+'preMO_'+barename+'_F_c.nii.gz')
    if os.path.exists(pwdsmo+'preMO_'+barename+'_pb.nii.gz'):
        MO_m2_pb = nib.load(pwdsmo+'preMO_'+barename+'_pb.nii.gz')
    if os.path.exists(pwdsmo+'preMO_'+barename+'_F_pb.nii.gz'):
        MO_m2_pb = nib.load(pwdsmo+'preMO_'+barename+'_F_pb.nii.gz')
    
    MO_m2_d = MO_m2_c.get_fdata()+MO_m2_pb.get_fdata()
    MO_affine = MO_m2_c.affine
    MO_m2_masked_img = nib.Nifti1Image(MO_m2_d,MO_affine)
    nib.save(MO_m2_masked_img,pwdsmo+'MO_'+barename+'_2.nii.gz')
    
    gc.collect()
    

## A PARTIR DE AQUI, SI SOLO UTILIZAMOS PLATIPY Y TOTALSEGMENTATOR, MODIFICACION DE LAS VALVULAS, QUIZAS USABLE TAMBIEN PARA OTROS CASOS


# GENERA ESTRUCTURAS DE MIOCARDIO Y MUSCULO CARDIACO EN TORNO A LAS CAMARAS CARDIACAS PARA PLATIPY, QUE SEGMENTA EL CONJUNTO CAMARA+MUSCULO DE CADA REGION CONJUNTAMENTE.
def PTstruPTyTS(barename,args,fakeimg):
    
    kernel = np.ones((2,2),np.uint8)
    kernelm = np.ones((3,3),np.uint8)
#    pwdspt = os.getcwd()+'/segms/PT/'
    if os.path.exists(pwdspt+'/'+barename):
        print('Preprocessing PT-structures for ' + barename)
        
        PT_h = nib.load(pwdspt+'/'+barename+'/Heart.nii.gz')
        PT_h_d = PT_h.get_fdata() * 51
     
        PT_atrL = nib.load(pwdspt+'/'+barename+'/Atrium_L.nii.gz')
        PT_affine = PT_atrL.affine
        if args.fheart == True:
            PT_atrL_d = PT_atrL.get_fdata() * 51
        else:
            PT_atrL_d = PT_atrL.get_fdata() * 151
            PT_atrL_d_er = cv2.erode(PT_atrL_d,kernel,iterations=1)
            PT_atrL_d_mio = ( PT_atrL_d - PT_atrL_d_er ) * 181 / 151   # *156 miocardio, *51 corazon, ¿etiqueta nueva?
#            PT_atrL_d = PT_atrL_d * 191 / 151   # comentada puesto que no la estaba usando
        
        PT_atrR = nib.load(pwdspt+'/'+barename+'/Atrium_R.nii.gz')
        if args.fheart == True:
            PT_atrR_d = PT_atrR.get_fdata() * 51
        else:
            PT_atrR_d = PT_atrR.get_fdata() * 152
            PT_atrR_d_er = cv2.erode(PT_atrR_d,kernel,iterations=1)
            PT_atrR_d_mio = ( PT_atrR_d - PT_atrR_d_er ) * 182 / 152   # *156 miocardio, *51 corazon, ¿etiqueta nueva?
            PT_atrR_d = PT_atrR_d * 192 / 152
        
        PT_venL = nib.load(pwdspt+'/'+barename+'/Ventricle_L.nii.gz')
        if args.fheart == True:
            PT_venL_d = PT_venL.get_fdata() * 51
        else:
            PT_venL_d = PT_venL.get_fdata() * 153
            PT_venL_d_er = cv2.erode(PT_venL_d,kernelm,iterations=3)
            PT_venL_d_mio = ( PT_venL_d - PT_venL_d_er ) * 156 / 153
            PT_venL_d = cv2.erode(PT_venL_d,kernel,iterations=1) * 193 / 153
        
        PT_venR = nib.load(pwdspt+'/'+barename+'/Ventricle_R.nii.gz')
        if args.fheart == True:
            PT_venR_d = PT_venR.get_fdata() * 51
        else:
            PT_venR_d = PT_venR.get_fdata() * 154
            PT_venR_d_er = cv2.erode(PT_venR_d,kernel,iterations=1)
            PT_venR_d_mio = ( PT_venR_d - PT_venR_d_er ) * 184 / 154   # *156 miocardio, *51 corazon, ¿etiqueta nueva?
            PT_venR_d = PT_venR_d * 194 / 154

        PT_h_mask_d = PT_h_d
        PT_ch_mask_d = PT_atrL_d_er + PT_atrR_d_er + PT_venL_d_er + PT_venR_d_er
        PT_ch2_mask_d = PT_atrL_d + PT_atrR_d + PT_venL_d + PT_venR_d
        PT_mio_mask_d = PT_atrL_d_mio + PT_atrR_d_mio + PT_venL_d_mio + PT_venR_d_mio

        
        PT_h_masked_img = nib.Nifti1Image(PT_h_mask_d,PT_affine)
        nib.save(PT_h_masked_img,pwdspt+'/PT_'+barename+'_h.nii.gz')
       
        PT_ch_masked_img = nib.Nifti1Image(PT_ch_mask_d,PT_affine)
        nib.save(PT_ch_masked_img,pwdspt+'/PT_'+barename+'_ch.nii.gz')
        
        PT_ch2_masked_img = nib.Nifti1Image(PT_ch2_mask_d,PT_affine)
        nib.save(PT_ch2_masked_img,pwdspt+'/PT_'+barename+'_ch2.nii.gz')
        
        PT_mio_masked_img = nib.Nifti1Image(PT_mio_mask_d,PT_affine)
        nib.save(PT_mio_masked_img,pwdspt+'/PT_'+barename+'_mio.nii.gz')
        
        gc.collect()

    else:
        print('path to: '+pwdspt+'/'+barename+" does not exist, creating fake files")
        nib.save(fakeimg,pwdspt+'/PT_'+barename+'_F_h.nii.gz')
        nib.save(fakeimg,pwdspt+'/PT_'+barename+'_F_ch.nii.gz')
        gc.collect()
        


# ACTUALMENTE, ESTA SUBRUTINA NO HACE NADA
def PTvalv_eroded(barename,args,fakeimg):

#    pwdspt = os.getcwd()+'/segms/PT/'
    if os.path.exists(pwdspt+'/'+barename):
        print('Preprocessing PT-valves for ' + barename)

        PT_miV = nib.load(pwdspt+'/'+barename+'/Valve_Mitral.nii.gz')  # left atr - ventr
        PT_affine = PT_miV.affine
        if args.hvalves == True:
            PT_miV_d = PT_miV.get_fdata() * 167
        if args.fheart == True:
            PT_miV_d = PT_miV.get_fdata() * 51
        if args.fheart != True and args.hvalves != True:
            PT_miV_d = PT_miV.get_fdata() * 0

        PT_triV = nib.load(pwdspt+'/'+barename+'/Valve_Tricuspid.nii.gz') # right atr - ventr
        if args.hvalves == True:
            PT_triV_d = PT_triV.get_fdata() * 168
        if args.fheart == True:
            PT_triV_d = PT_triV.get_fdata() * 51
        if args.fheart != True and args.hvalves != True:
            PT_triV_d = PT_triV.get_fdata() * 0

        PT_aV = nib.load(pwdspt+'/'+barename+'/Valve_Aortic.nii.gz')
        if args.hvalves == True:
            PT_aV_d = PT_aV.get_fdata() * 169
        if args.fheart == True:
            PT_aV_d = PT_aV.get_fdata() * 51
        if args.fheart != True and args.hvalves != True:
            PT_aV_d = PT_aV.get_fdata() * 0

        PT_pV = nib.load(pwdspt+'/'+barename+'/Valve_Pulmonic.nii.gz')
        if args.hvalves == True:
            PT_pV_d = PT_pV.get_fdata() * 170
        if args.fheart == True:
            PT_pV_d = PT_pV.get_fdata() * 51
        if args.fheart != True and args.hvalves != True:
            PT_pV_d = PT_pV.get_fdata() * 0

        PT_SCN = nib.load(pwdspt+'/'+barename+'/CN_Sinoatrial.nii.gz')
        if args.hvalves == True:
            PT_SCN_d = PT_SCN.get_fdata() * 171
        if args.fheart == True:
            PT_SCN_d = PT_SCN.get_fdata() * 51
        if args.fheart != True and args.hvalves != True:
            PT_SCN_d = PT_SCN.get_fdata() * 0

        PT_ACN = nib.load(pwdspt+'/'+barename+'/CN_Atrioventricular.nii.gz')
        if args.hvalves == True:
            PT_ACN_d = PT_ACN.get_fdata() * 172
        if args.fheart == True:
            PT_ACN_d = PT_ACN.get_fdata() * 51
        if args.fheart != True and args.hvalves != True:
            PT_ACN_d = PT_ACN.get_fdata() * 0

        PT_VyCN_mask_d = PT_triV_d + PT_miV_d + PT_aV_d + PT_pV_d + PT_SCN_d + PT_ACN_d  #   SOLAPAN TANTO CON hart COMO con h

        PT_VyCN_masked_img = nib.Nifti1Image(PT_VyCN_mask_d,PT_affine)
        nib.save(PT_VyCN_masked_img,pwdspt+'/prePT_'+barename+'_VyCN.nii.gz')
        
        gc.collect()

    else:
        print('path to: '+pwdspt+'/'+barename+" does not exist, creating fake files")
        nib.save(fakeimg,pwdspt+'/prePT_'+barename+'_F_VyCN.nii.gz')
        gc.collect()
