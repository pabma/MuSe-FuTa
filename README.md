# TartagliaS
This Multiple Segmentation Fusion algorithm has been developed as part of the Tartaglia IA project to improve medical research.

The first step to take in order to build this multiple segmentation fusion is (amazingly, I know) to install the Medical Image Segmentators we have chosen. In this first iteration, we have worked with only 3 segmentators, although two of them have several different models, this segmentators are TotalSegmentator, Platipy and Moose(v3).

STEP 1) To install and use them, follow the next instructions:

1) Create a virtual environment.
   - mkdir [a_name -> direcotry/environment name]
   - cd [a_name]
   - conda create --name [a_name] python=3.10
  
2) Install the Segmentators and other necessary apps.
   - conda activate [a_name]
   - pip3 install torch torchvision torchaudio
   - python3 -m pip install tensorflow
   - pip3 install TotalSegmentator
   - sudo apt-get install xvfb (ubuntu installation process, yours might be different)
   - pip install fury
   - pip3 install platipy
   - pip install upgrade platipy
   - pip install platipy[cardiac]
   - pip install platipy[nnunet]
   - pip install platipy[backend]
   - pip install moosez
   - python3 -m pip install -U nilearn
   - pip install xlrd
   - pip install reorient-nii
   - pip install mpdaf

3) How to run them all, and in darkness bind them.
   - copy 'runsegms.sh', 'moose.py' and 'checklist.py' to [a_name]
   - Be sure that there is no current file or directory in [a_name] which begins with CT_*
   - copy your original CT files to [a_name], and change their names so they begin with CT_*
   - run 'sh runsegms.sh' (linux)
   - enjoy some time doing something else while they run

This will create several directories and run all the segmentators in order, placing their output files in the right directories. BE WARNED, ADVENTURER!!  IF YOU CHANGE THE NAME OR REMOVE ANY OF THIS DIRECTORIES, THE NEXT STEPS ARE DOOMED TO FAIL UNLESS YOU CHANGE ALSO THE CODE!!  The directory 'Used' is of special importance here, beware of put or remove files there.
