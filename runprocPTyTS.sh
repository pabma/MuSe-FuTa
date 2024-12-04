#!/bin/bash

if [ ! -d mix ]; then
	mkdir mix
fi

for f in used/*.gz; do

###	python3 preproc.py -o ${f%.nii.gz} $1 $2 $3 $4  # ORIGINAL con Moose
	python3 preproc_TSyPT.py -o ${f%.nii.gz} $1 $2 $3 $4  # Sin Moose

###	python3 mix_img.py -o ${f%.nii.gz} $1 $2 $3 $4  # ORIGINAL
	python3 mix_img_TSyPT.py -o ${f%.nii.gz} $1 $2 $3 $4 # Platipy y TotalSegmentator

	python3 postproc_valves.py -o ${f%.nii.gz}

done

#time -o time.txt
