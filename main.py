import re
import os
import csv
import math
import config
from shutil import copy2, move
from PIL import Image
from train.trainer import create_classifier_model


# seal-images/
#   LF1/
#       originals/
#       bottling-left/
#       wet-head-right/
#   LF28/
#       originals/
#       bottling-left/
#       wet-head-right/

# Get the tag to know which folders to look through
# Loop through the seal folders to find the see whether it has a folder for that tag
# Calculate the number of images needed per tag, rotate images until we get enough


if __name__ == '__main__':
    create_classifier_model('wet-head-right')
