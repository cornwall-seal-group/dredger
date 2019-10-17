# dredger

This project loops through an images folder of seals and looks for a folder for the specified orientation. If the folder exists, then all the images will be submitted to the classifier.

At the moment `main.py` has the orientation hardcoded, if you want to change per orientation, change `main.py` and re-run the process. In the future this will be an arguement sent to the process.

## How it works

Based on the orientation configured, the process will look through all seal folders and looks for the particular orientation folder. If the folder exists then it will work out how many images for this orientation there is.

We want 50 images for each seal, so if there are less than 50 images for the given orientation (this is expected!!) then the script will work out how many angles it needs to duplicate of each image and make rotations of each image and submit. This way you get lots of images for a particular seal to be trained against.

The process creates a classifier and submits all these images with their tags to the classifier. You can then use the Azure Custom Vision UI to view the images submitted, and verify!, you can then train the model.
