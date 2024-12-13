#!/bin/bash

if [ ! -d mix ]; then
	mkdir mix
fi

for f in used/*.gz; do

	python3 runproc/preproc.py -o ${f%.nii.gz} $1 $2 $3 $4  # ORIGINAL with Moose
#	python3 runproc/preproc_TSyPT.py -o ${f%.nii.gz} $1 $2 $3 $4  # Without Moose

	python3 runproc/mix_img.py -o ${f%.nii.gz} $1 $2 $3 $4  # ORIGINAL
#	python3 runproc/mix_img_TSyPT.py -o ${f%.nii.gz} $1 $2 $3 $4 # Platipy y TotalSegmentator

	python3 runproc/postproc_valves.py -o ${f%.nii.gz}

done

#time -o time.txt
