import os
import sys
import argparse
from moosez import moose
import gc

gc.collect()

# Eliminated the models 'vertebrae', 'fast_vertebrae' as they are incompatible with something in the Platipy or TS segmentators
# Eliminated the models 'fast_organs', 'fast_cardiac' to avoid overcharge the processor in the creation of the mix file and because their results were not always right
#Eliminated the models 'body', 'body_composition' and 'PUMA4' as their output is, currently, bad.

models = ('lungs','organs','ribs','muscles','cardiac','digestive','all_bones_v1','PUMA','ALPACA','peripheral_bones')


pwd = os.getcwd()

file = sys.argv[1]

input_dir = pwd +'/'+file                            # '/home/pablo/test-env/'
accelerator = 'cuda'


#for modv in models:
if __name__ == '__main__':
    for modv in models:
        print('running Moosev3 '+modv+' model for '+file)
        moose(input_dir,'clin_ct_'+modv,pwd+'/segms/MO/MO',accelerator)
        gc.collect()

gc.collect()

