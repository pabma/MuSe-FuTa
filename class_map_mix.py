import numpy as np


class_map = {
        0: "zero",
        1: "spleen",
        2: "kidney_right",
        3: "kidney_left",
        4: "gallbladder",
        5: "liver",
        6: "stomach",
        7: "pancreas",
        8: "adrenal_gland_right",
        9: "adrenal_gland_left",
        10: "lung_upper_lobe_left",
        11: "lung_lower_lobe_left",
        12: "lung_upper_lobe_right",
        13: "lung_middle_lobe_right",
        14: "lung_lower_lobe_right",
        15: "esophagus",
        16: "trachea",
        17: "thyroid_gland",
        18: "small_bowel",
        19: "duodenum",
        20: "colon", ## Asignado como instestino grueso (17)... ¿Lumen (39)?
        21: "urinary_bladder",
        22: "prostate",
        23: "kidney_cyst_left",   # Quiste renal, sin asignacion directa en el excel
        24: "kidney_cyst_right",   # Quiste renal, sin asignacion directa en el excel
        25: "sacrum",  ## Asignado cortical, ¿cancellous?
        26: "vertebrae_S1",
        27: "vertebrae_L5",
        28: "vertebrae_L4",
        29: "vertebrae_L3",
        30: "vertebrae_L2",
        31: "vertebrae_L1",
        32: "vertebrae_T12",
        33: "vertebrae_T11",
        34: "vertebrae_T10",
        35: "vertebrae_T9",
        36: "vertebrae_T8",
        37: "vertebrae_T7",
        38: "vertebrae_T6",
        39: "vertebrae_T5",
        40: "vertebrae_T4",
        41: "vertebrae_T3",
        42: "vertebrae_T2",
        43: "vertebrae_T1",
        44: "vertebrae_C7",
        45: "vertebrae_C6",
        46: "vertebrae_C5",
        47: "vertebrae_C4",
        48: "vertebrae_C3",
        49: "vertebrae_C2",
        50: "vertebrae_C1",
        51: "heart",  ## Cambiado a 13 para TsyPT solo. Asignado como 64 = heart_lumen en los 3 segmentadores, asignado como 1 en XCAT. #transformado en 15 (musculo, pero no musculo cardiaco) en XCAT
        52: "aorta",
        53: "pulmonary_vein",
        54: "brachiocephalic_trunk",
        55: "subclavian_artery_right",
        56: "subclavian_artery_left",
        57: "common_carotid_artery_right",
        58: "common_carotid_artery_left",
        59: "brachiocephalic_vein_left",
        60: "brachiocephalic_vein_right",
        61: "atrial_appendage_left",  ## Creo que no es musculo cardiaco (13), asi que lo he asignado como sangre (22), 7 en XCAT.
        62: "superior_vena_cava",
        63: "inferior_vena_cava",
        64: "portal_vein_and_splenic_vein",
        65: "iliac_artery_left",
        66: "iliac_artery_right",
        67: "iliac_vena_left",
        68: "iliac_vena_right",
        69: "humerus_left",  ## Asignado como hueso cortical
        70: "humerus_right",  ## Asignado como hueso cortical
        71: "scapula_left",
        72: "scapula_right",
        73: "clavicula_left",  ## Ambos tipos de hueso, asignado como cortical
        74: "clavicula_right",  ## Ambos tipos de hueso, asignado como cortical
        75: "femur_left",  ## Asignado como hueso cortical
        76: "femur_right",  ## Asignado como hueso cortical
        77: "hip_left",
        78: "hip_right",
        79: "spinal_cord",
        80: "gluteus_maximus_left",
        81: "gluteus_maximus_right",
        82: "gluteus_medius_left",
        83: "gluteus_medius_right",
        84: "gluteus_minimus_left",
        85: "gluteus_minimus_right",
        86: "autochthon_left",
        87: "autochthon_right",
        88: "iliopsoas_left",
        89: "iliopsoas_right",
        90: "brain",
        91: "skull",
        92: "rib_left_1",
        93: "rib_left_2",
        94: "rib_left_3",
        95: "rib_left_4",
        96: "rib_left_5",
        97: "rib_left_6",
        98: "rib_left_7",
        99: "rib_left_8",
        100: "rib_left_9",
        101: "rib_left_10",
        102: "rib_left_11",
        103: "rib_left_12",
        104: "rib_right_1",
        105: "rib_right_2",
        106: "rib_right_3",
        107: "rib_right_4",
        108: "rib_right_5",
        109: "rib_right_6",
        110: "rib_right_7",
        111: "rib_right_8",
        112: "rib_right_9",
        113: "rib_right_10",
        114: "rib_right_11",
        115: "rib_right_12",
        116: "sternum",  ## Asignado como cancellous, pero con el nucleo cortical.
        117: "costal_cartilages",
        118: "",
        119: "",
        120: "",
        121: "",
        122: "",
        123: "",
        124: "",
        125: "",
        126: "",
        127: "",
        128: "",
        129: "",
        130: "",
        131: "",
        132: "",
        133: "",
        134: "",
        135: "",
        136: "",
        137: "",
        138: "",
        139: "",
        140: "unknown_tissue",
        141: "skeletal_muscle",
        142: "visceral_fat",
        143: "subcutaneous_fat",
        144: "",
        145: "",
        146: "",
        147: "",
        148: "",
        149: "",
        150: "lungs",
        151: "atrium_left",  ## Asignado como sangre (22), lumen? (64)
        152: "atrium_right",  ## Asignado como sangre (22), lumen? (64)
        153: "ventricle_left",  ## Asignado como sangre (22), lumen? (64)
        154: "ventricle_right",  ## Asignado como sangre (22), lumen? (64)
        155: "pulmonary_artery",
        156: "myocardium",
        157: "",
        158: "thoracic_fat",     ## Nueva asignacion en el excel de propiedades, etiqueta 63, excel renombrado a Tv1
        159: "ribs",   ## Todas las costillas juntas en lugar de una a una como hasta ahora.
        160: "bronchus",
        161: "",
        162: "left_anterior_descendant_artery",
        163: "circumflex_artery",
        164: "left_coronary_artery",
        165: "right_coronary_artery",
        166: "",
        167: "mitral_valve",   ## Asignada como musculo cardiaco, pero relativamente distinta
        168: "tricuspid_valve",  ## Asignada como musculo cardiaco, pero relativamente distinta
        169: "aortic_valve",  ## Asignada como musculo cardiaco, pero relativamente distinta
        170: "pulmonic_valve",  ## Asignada como musculo cardiaco, pero relativamente distinta
        171: "",  ## Aqui iba el sinoatrial_conduct_node
        172: "",  ## Aqui iba el atrioventricular conduct node.
        173: "",
        174: "",
        175: "",
        176: "",
        177: "mitral_valve_2",
        178: "tricuspid_valve_2",
        179: "",
        180: "",
        181: "atrium_left_wall",
        182: "atrium_right_wall",
        183: "",  # es el miocardio, 156
        184: "ventricle_right_wall"
    }

#Asignacion de las estructuras de mix como estructuras de XCAT. He supuesto ventriculos y auriculas como llenas de sangre, y las he asignado como tales segun XCAT. DEBERIA SER REVISADO DE ARRIBA A ABAJO
labels_dataset_mix_XCAT=np.array([0,36,29,31,19,18,26,28,33,33,21,21,20,20,20,22,64,72,49,49,50,44,45,30,32,38,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,1,42,43,42,42,42,42,42,43,43,7,43,43,43,42,42,43,43,38,38,38,38,38,38,38,38,38,38,40,15,15,15,15,15,15,15,15,15,15,16,38,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,58,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,15,11,11,0,0,0,0,0,0,20,7,8,5,6,42,1,0,11,37,64,0,9,9,9,9,0,3,4,1,2,0,0,0,0,0,0,0,3,4,0,3,4,0,2])


# Lista de asignacion para el mix de 3 segmentadores, v4.2 del excel. Ventric/auric como sangre (22), tejido blando en 140 como 11
labels_dataset_mix=np.array([0,1,2,2,3,4,5,7,8,8,9,9,9,9,9,11,12,46,16,16,17,21,31,0,0,18,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,13,6,6,6,6,6,6,6,6,6,22,6,6,6,6,6,6,6,18,18,18,18,18,18,18,18,14,14,28,20,20,20,20,20,20,20,20,20,20,15,65,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,38,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,63,20,63,19,0,0,0,0,0,0,9,22,22,22,22,6,13,0,63,14,42,0,6,6,6,6,0,13,13,13,13,0,0,0,0,0,0,13,13,0,0,13,13,0,13])


# Para aquellas asignaciones en las que tengo dudas y que deberian ser revisadas
labels_dataset_mix_check=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

## Asignacion de XCAT para v4.2 del excel:
labels_dataset_XCAT=np.array([0,13,13,13,13,22,22,22,22,6,6,19,19,23,23,20,15,9,4,3,9,9,11,24,25,26,5,27,7,66,67,66,67,8,2,2,1,14,18,10,28,29,6,6,21,31,17,17,17,16,39,33,33,34,35,36,37,13,38,68,30,30,40,40,42,42,43,44,45,45,45,46,46,47,48,49,69,51,13,52,53,52,53,53,54,52,55,53,56,53,53,53,52,57,58,58,58,59,53,53,60,61,61,58,62,62,62,58,58,61,52,53])


# Antigua lista de asignacion, version V1 de TS y v4.1 del excel propiedades, no es valido para las nuevas versiones de ambos.
#labels_dataset_TS1=np.array([0, 1, 2, 2, 3, 4, 5, 6, 6, 6, 7, 8, 8, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 12, 13, 13, 13, 13, 13, 14, 15, 14, 14, 14, 14, 16, 16, 17, 18, 18, 18, 18, 18, 18, 18, 18,18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 21])
    
# Antigua asignacion de densidades para XCAT y v4.1 del excel de propiedades, no valida en las nuevas versiones.
#labels_dataset_XCAT_old=np.array([0,13,13,13,13,22,22,22,22,6,6,19,19,23,23,20,15,9,4,3,9,9,11,24,25,26,5,27,7,2,2,2,2,8,2,2,1,18,18,10,28,29,14,14,30,31,17,17,17,32,17,33,33,34,35,36,37,13,38,39,30,30,40,41,42,12,43,44,45,45,45,46,46,47,48,49,50,51,13,52,53,52,53,53,54,52,55,53,56,53,53,53,52,57,58,58,58,59,53,53,60,61,61,58,62,62,62,58,58,61,52,53])

class_map_XCAT ={
    0: "zero",
    1: "myoLV_act",		# hrt_myoLV_act - activity in left ventricle myocardium
    2: "myoRV_act",		# hrt_myoRV_act - activity in right ventricle myocardium
    3: "myoLA_act",		# hrt_myoLA_act - activity in left atrium myocardium
    4: "myoRA_act",		# hrt_myoRA_act - activity in right atrium myocardium
    5: "bldplLV_act",	# hrt_bldplLV_act - activity in left ventricle chamber (blood pool)
    6: "bldplRV_act",        # hrt_bldplRV_act - activity in right ventricle chamber (blood pool)
    7: "bldplLA_act",	# hrt_bldplLA_act - activity in left atria chamber (blood pool)
    8: "bldplRA_act",		# hrt_bldplRA_act - activity in right atria chamber (blood pool)
    9: "coronary_art_activity",	# coronary_art_activity - activity in the coronary arteries
    10: "coronary_vein_activity",	# coronary_vein_activity - activity in the coronary veins
    11: "body_activity",		# body_activity (background activity);
    12: "skin_activity",		# skin_activity (used if skin_thickness is > 0)
    13: "rbreast_activity",		# right breast activity;
    14: "lbreast_activity",		# left breast activity;
    15: "muscle_activity",		# muscle activity;
    16: "brain_activity",		# brain activity;
    17: "sinus_activity",		# sinus activity;
    18: "liver_activity",		# liver_activity;
    19: "gall_bladder_activity",	# gall_bladder_activity;
    20: "r_lung_activity",		# right_lung_activity;
    21: "l_lung_activity",             # left_lung_activity;
    22: "esophagus_activity",		# esophagus_activity;
    23: "esophagus_cont_activity",	# esophagus_contents_activity
    24: "laryngopharynx_activity",	# laryngopharynx_activity
    25: "larynx_activity",		# larynx_activity
    26: "st_wall_activity",		# st_wall_activity;  (stomach wall)
    27: "st_cnts_activity",		# st_cnts_activity;   (stomach contents)
    28: "pancreas_activity",		# pancreas_activity;
    29: "r_kidney_cortex_activity",	# right_kidney_cortex_activity;
    30: "r_kidney_medulla_activity",	# right_kidney_medulla_activity;
    31: "l_kidney_cortex_activity",	# left_kidney_cortex_activity;
    32: "l_kidney_medulla_activity",	# left_kidney_medulla_activity;
    33: "adrenal_activity",		# adrenal_activity;
    34: "r_renal_pelvis_activity",	# right_renal_pelvis_activity;
    35: "l_renal_pelvis_activity",     # left_renal_pelvis_activity;
    36: "spleen_activity",		# spleen_activity;
    37: "rib_activity",		# rib_activity;
    38: "cortical_bone_activity",	# cortical_bone_activity;
    39: "spine_activity",		# spine_activity;
    40: "spinal_cord_activity",	# spinal_cord_activity;
    41: "bone_marrow_activity",	# bone_marrow_activity;
    42: "art_activity",		# artery_activity;
    43: "vein_activity",		# vein_activity;
    44: "bladder_activity",		# bladder_activity;
    45: "prostate_activity",		# prostate_activity;
    46: "asc_li_activity",		# ascending_large_intest_activity;
    47: "trans_li_activity",		# transcending_large_intest_activity;
    48: "desc_li_activity",		# desc_large_intest_activity;
    49: "sm_intest_activity",		# small_intest_activity;
    50: "rectum_activity",		# rectum_activity;
    51: "sem_activity",		# sem_vess_activity;
    52: "vas_def_activity",		# vas_def_activity;
    53: "test_activity",		# testicular_activity;
    54: "penis_activity",		# penis_activity
    55: "epididymus_activity",		# epididymus_activity;
    56: "ejac_duct_activity",		# ejaculatory_duct_activity;
    57: "pericardium_activity",     	# pericardium activity;
    58: "cartilage_activity",		# cartilage activity;
    59: "intest_air_activity",	# activity of intestine contents (air); 
    60: "ureter_activity",		# ureter activity; 
    61: "urethra_activity",		# urethra activity; 
    62: "lymph_activity",		# lymph normal activity; 
    63: "lymph_abnormal_activity",	# lymph abnormal activity; 
    64: "trach_bronch_activity",	# trachea_bronchi_activity;
    65: "airway_activity",		# airway tree activity
    66: "uterus_activity",		# uterus_activity;
    67: "vagina_activity",		# vagina_activity;
    68: "right_ovary_activity",	# right_ovary_activity;
    69: "left_ovary_activity",	# left_ovary_activity;
    70: "fallopian_tubes_activity",	# fallopian tubes_activity;
    71: "parathyroid_activity",	# parathyroid_activity;
    72: "thyroid_activity",		# thyroid_activity;
    73: "thymus_activity",		# thymus_activity;
    74: "salivary_activity",		# salivary_activity;
    75: "pituitary_activity",	# pituitary_activity;
    76: "eye_activity",		# eye_activity;
    77: "lens_activity", 		# eye_lens_activity;
    78: "lesn_activity",		# activity for heart lesion, plaque, or spherical lesion
    79: "Corpus_Callosum_act",	# activity of Corpus_Callosum
    80: "Caudate_act",		# activity of Caudate
    81: "Internal_capsule_act",	# activity of Internal_capsule
    82: "Putamen_act",		# activity of Putamen
    83: "Globus_pallidus_act",	# activity of Globus_pallidus
    84: "Thalamus_act",		# activity of Thalamus
    85: "Fornix_act",			# activity of Fornix
    86: "Anterior_commissure_act",	# activity of Anterior_commissure
    87: "Amygdala_act",		# activity of Amygdala
    88: "Hippocampus_act",		# activity of Hippocampus
    89: "Lateral_ventricle_act",	# activity of Lateral_ventricle
    90: "Third_ventricle_act",		# activity of Third_ventricle
    91: "Fourth_ventricle_act",	# activity of Fourth_ventricle
    92: "Cerebral_aqueduct_act",	# activity of Cerebral_aqueduct
    93: "Mamillary_bodies_act",	# activity of Mamillary_bodies
    94: "Cerebral_peduncles_act",	# activity of Cerebral_peduncles
    95: "Superior_colliculus_act",	# activity of Superior_colliculus
    96: "Inferior_colliculus_act",	# activity of Inferior_colliculus
    97: "Pineal_gland_act",		# activity of Pineal_gland
    98: "Periacquaductal_grey_outer_act",	# activity of Periacquaductal_grey_outer
    99: "Periacquaductal_grey_act",		# activity of Periacquaductal_grey_inner
    100: "Pons_act",				# activity of Pons
    101: "Superior_cerebellar_peduncle_act",	# activity of Superior_cerebellar_peduncle
    102: "Middle_cerebellar_peduncle_act",	# activity of Middle_cerebellar_peduncle
    103: "Substantia_nigra_act",		# activity of Substantia_nigra
    104: "Medulla_act",			# activity of Medulla
    105: "Medullary_pyramids_act",		# activity of Medullary_pyramids
    106: "Inferior_olive_act",			# activity of Inferior_olive
    107: "Tegmentum_of_midbrain_act",	# activity of Tegmentum_of_midbrain
    108: "Midbrain_act",			# activity of Midbrain
    109: "cerebellum_act",		# activity of cerebellum
    110: "white_matter_act",		# activity of remaining white matter 
    111: "grey_matter_act",		# activity of remaining grey matter
}
