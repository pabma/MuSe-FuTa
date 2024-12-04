#!/bin/bash

## PYTHONS MODIFICADOS EN NOTEPAD++

for f in used/*.gz; do

	python3 NPZ_gen_mix_XCAT.py -o ${f%.nii.gz} $1
	
done

#time -o time.txt
