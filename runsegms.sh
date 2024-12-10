# Requiere poner las imagenes nifti (*.nii.gz) con nombre iniciado en ct_* en el directorio en el cual se vaya a usar esta aplicacion, que correra las tres aplicaciones (TotalSegmentator, Platipy y Moose) y despues movera las imágenes a un directorio llamado used. Las imagenes originales deben ser mantenidas en ese directorio para que el resto de la aplicacion (preprocesado y fusion de estructuras) funcione. Para usarla, escribir "sh runsegms.sh"
#!/bin/bash

pwd
if [ ! -d used ]; then
	mkdir used
fi

if [ ! -d reoriented ]; then
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

for f in *.gz; do
	python3 checkaxis.py $f
done

for f in *.gz; do
	echo $f
	echo ${f%.nii.gz}
	TotalSegmentator -i $f -o segms/TS/TS/${f%.nii.gz} --ml
	TotalSegmentator -i $f -o segms/TS/TS/${f%.nii.gz}_b --task body --ml
	TotalSegmentator -i $f -o segms/TS/TS/${f%.nii.gz}_lv --task lung_vessels --ml
##	TotalSegmentator -i $f -o segms/TS/TS/${f%.nii.gz}_ca --task coronary_arteries --ml
	platipy segmentation cardiac -o segms/PT/${f%.nii.gz} $f
	platipy segmentation bronchus -o segms/PT/${f%.nii.gz} $f
	python3 moose3.py $f
	mv $f used
done

#time -o time.txt
