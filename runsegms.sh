# It requieres to put the nifti images in *.nii.gz format, and beggining with CT_* in the main folder from which this sofware will be run. It will run the apps (TotalSegmentator, Platipy and Moose). It will put the original images in a folder called 'orig' if there is need to resize or reorient them, and the segmented images in a folder called 'used'. 'used' is a very important folder for this software. To run in write "sh runsegms.sh" in a prompt.

#!/bin/bash

pwd
if [ ! -d used ]; then
	mkdir used
fi

if [ ! -d orig/reoriented ]; then
	mkdir -p orig/reoriented
fi

if [ ! -d segms/TS ]; then
	mkdir -p segms/TS
fi
if [ ! -d segms/PT ]; then
	mkdir -p segms/PT
fi
if [ ! -d segms/MO/MO ]; then
	mkdir -p segms/MO/MO
fi

for f in *.nii.gz; do
	python3 runsegms/checkaxis.py $f
done

for f in *.nii.gz; do
	echo $f
	echo ${f%.nii.gz}
	TotalSegmentator -i $f -o segms/TS/TS/${f%.nii.gz} --ml
	TotalSegmentator -i $f -o segms/TS/TS/${f%.nii.gz}_b --task body --ml
	TotalSegmentator -i $f -o segms/TS/TS/${f%.nii.gz}_lv --task lung_vessels --ml
##	TotalSegmentator -i $f -o segms/TS/TS/${f%.nii.gz}_ca --task coronary_arteries --ml
	platipy segmentation cardiac -o segms/PT/${f%.nii.gz} $f
	platipy segmentation bronchus -o segms/PT/${f%.nii.gz} $f
	python3 runsegms/moose3.py $f
	mv $f used
done

#time -o time.txt
