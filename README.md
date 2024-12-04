# TartagliaS
This Multiple Segmentation Fusion/Ensemble algorithm has been developed as part of the Tartaglia IA project to improve medical research.

The first step to take in order to build this multiple segmentation fusion/ensemble is (amazingly, I know) to install the Medical Image Segmentators we have chosen. In this first iteration, we have worked with only three segmentators, although two of them have several different models, this segmentators are TotalSegmentator, Platipy and Moose(v3).

Some versions of the algorithm do not currently use the Moose output. If you do not desire to install it, or any other segmentator, edit the requirements.txt file accordingly, although, if you remove TotalSegmentator, you will have to edit also the code later on in order for it to work properly.

STEP 1) To install and use the segmentators, follow the next instructions (ubuntu OS, a couple places might have to be edited in requirements.txt for other OS):

1) Create a virtual environment:
   - mkdir [a_name -> direcotry/environment name].
   - cd [a_name].
   - conda create --name [a_name] python=3.10.
  
2) Install the Segmentators and other necessary packets:
   - conda activate [a_name].
   - Download 'requirements.txt' into [a_name].
   - pip install -r requrirements.txt.
   - Look for some CTs to segment, a few places to find CTs are:
        - https://zenodo.org/records/10047292 (Full TotalSegmentator training dataset, there are several repeated images here under different name)
        - https://zenodo.org/records/10047263 (Reduced TotalSegmentator training dataset)
        - https://www.cancerimagingarchive.net/collection/ct-images-in-covid-19/
        - https://www.kaggle.com/datasets/mohamedhanyyy/chest-ctscan-images

3) How to run them all, and in darkness bind them:
   - Download 'runsegms.sh', 'moose.py' and 'checklist.py' into [a_name].
   - Be sure that there is no current file or directory in [a_name] which begins with CT_*.
   - Copy your original CT files to [a_name], and change their names so they begin with CT_*.
   - Run 'sh runsegms.sh' (linux OS).
   - Enjoy some time doing something else while they run.

This will create several directories and run all the segmentators in order, placing their output files in the right directories. BE WARNED, ADVENTURER!!  IF YOU CHANGE THE NAME OR REMOVE ANY OF THIS DIRECTORIES, THE NEXT STEPS ARE DOOMED TO FAIL UNLESS YOU CHANGE ALSO THE CODE!!  The directory 'Used' is of special importance here, beware of put or remove files there.
