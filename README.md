# TartagliaS
This Multiple Segmentation Ensemble Algorithm has been developed as part of the Tartaglia IA project to improve medical research.

The first step to take in order to build this multiple segmentation ensemble is (amazingly, I know) to install the Medical Image Segmentators we have chosen. In this first iteration, we have worked with only three segmentators, although two of them have several different models, this segmentators are TotalSegmentator, Platipy and Moose(v3).

STEP 1) To install and use the segmentators, follow the next instructions (ubuntu OS, a couple places might have to be edited in requirements.txt for other OS):

   1) Create a virtual environment:
      - mkdir [a_name -> direcotry/environment name]
      - cd [a_name]
      - conda create --name [a_name] python=3.10
  
   2) Install the Segmentators and other necessary packets:
      - conda activate [a_name]
      - Download 'requirements.txt' into [a_name].
      - pip install -r requirements.txt
      - Look for some CTs to download and segment, a few places to find CTs are:
        - https://zenodo.org/records/10047292 (Full TotalSegmentator training dataset, there are several repeated images here under different name)
        - https://zenodo.org/records/10047263 (Reduced TotalSegmentator training dataset)
        - https://www.cancerimagingarchive.net/collection/ct-images-in-covid-19/
        - https://www.kaggle.com/datasets/mohamedhanyyy/chest-ctscan-images

   3) How to run them all, and (later on) in darkness bind them:
      - Download 'runsegms.sh' and the folder 'runsegms' into [a_name].
      - Be sure that there is no current file or directory in [a_name] which begins with CT_* or any file ending in *.nii.gz.
      - Copy your original CT files to [a_name] in *.nii.gz format, and change their names so they begin with CT_*.
      - Run 'sh runsegms.sh' (linux OS).
      - Enjoy some time doing something else while they run.

This will create several directories and run all the segmentators in order, placing their output files in the right directories. BE WARNED, ADVENTURER!!  IF YOU CHANGE THE NAME OR REMOVE ANY OF THIS DIRECTORIES, THE NEXT STEPS ARE DOOMED TO FAIL UNLESS YOU CHANGE ALSO THE CODE!! The directory 'Used' is of special importance here, beware of put or remove files there.

STEP 2) To run the processing and assembling of the segmented images.

   - For some versions of the software, you might need to take the next steps in order for this part to run properly:
     - pip uninstall stl
     - pip install numpy-stl
     - pip install fastmorph
   - Download 'runproc.sh' and 'runprocPTyTS.sh' into [a_name]. This two files are, in fact, the same but with different commented lines so, if you are up to edit them yourself, you can use only one of them and edit it as you need.
   - Download the files 'preproc.py', 'preproc_TSyPT.py', 'mix_img.py', 'mix_img_TSyPT.py', 'postproc_valves.py', 'preproc_def.py', 'postproc_valves.py' and 'valves_def.py' into [a_name]
   - run 'sh runproc.sh' or 'sh runproc_PTyTS.sh' (linux). There are several input options to choose here:
      - --flungs .- Will fuse/assemble the lung lobes into a single structure representing the lungs.
      - --fheart .- Will fuse/assemble all the heart structures into a single structure representingt the full heart withuot any cardiac structures (This option is incompatible with the next ones, so take care or weird things might happen).
      - --harteries .- Will include the coronary arteries into the assembled image. If this option is not set, those structures will not be included.
      - --hvalves .- Will include the different heart valves (mitral, tricuspid, aortic and pulmonary) into the assembled image (Important choice for another part of this project which will simulate the heartbeat).
   - Enjoy some time doing anything else while the software is assembling the segmented images.

This will create a directory called 'mix', where the ensembled images will be put, ready to be used in the postprocessing. -- And, right now, several images with the valves rotated by a certain degree into your main directory.

The ensembled image will be cretaed partly using the 'mode' between the different segmented model images for each voxel, plus some specifically picked up choices to assure the presence of certain structures, like the valves, which show up only in one segmentator model. 

STEP 3) In order to generate the npz files, which will be used to simulate the ultrasound image.

   - Download 'runnpz.sh', 'NPZ_gen_mix_XCAT.py', 'class_map_mix.py', 'npzgen_def.py' and 'Thermal_dielectric_acoustic_MR properties_database_V4.2(Excel)_Tv1_sorted.xls' into [a_name]
   - run 'sh runnpz.sh' (Linux OS). You have the option to run it from the original mixed file, using --noXCAT. If you do not use this option, the software will automatically generate a file in mix with the XCAT labels, and generate a npz file with it. **NOTE: RIGHT NOW, YOU CANNOT USE THE XCAT LABELS IF YOU WANT THE VALVES TO MOVE.

This will generate a npz file in your main directory, assigning several tissue properties to each label, like density or sound speed, and creating the frames which will allow the Ultrasound simulator to run properly.
