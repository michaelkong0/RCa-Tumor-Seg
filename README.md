## **Some various code - saved for version control**

#### DatasetStatistics.ipnyb
Evaluate the dataset, ensure masks are correct
Also does analysis of tumor bounding boxes

#### UNetTest.ipnyb
Use the implementation of 3D UNet found at https://github.com/wolny/pytorch-3dunet
Simple testing implementation simply brute forcing 2 images as training and one as validation

###### test_config.yml and train_config.yml
Configuration files for testing of the unet

#### checkCUDA.py
Simple script to be run in command terminal to check if torch, CUDA,cuDNN, etc. are installed and operating correctly

#### evaluateFOV.ipynb
Attempts to analyse the field of view of the images. Still requires manual viewing for confirmation

#### distanceMetrics.ipnyb
Rudimentary efforts to calcuate some distance metrics

#### nnUNetTest.ipynb
transition to nnUNet implementation, same as UNetTest, but instead testing the functionality of the nnUNet
See: https://github.com/MIC-DKFZ/nnUNet
Also, method of data storage is much different, see code.