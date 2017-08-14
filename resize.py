import os
import errno
import random
import string
from PIL import Image
from PIL import ImageChops

width = 360
height = 257


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

directory = "./"
for subdir, dirs, images in os.walk(directory):
    if hasNumbers(subdir):
        for sub, dirs, images in os.walk(subdir):

            for currentImage in images:
                if ".jpg" in currentImage:

                    currentImage = os.getcwd() + "/" + sub.replace("./", "") + "/" + currentImage
                    thisImage = Image.open(currentImage)
                    if 'JPEG'in thisImage.format:
                        # use nearest neighbour
                        image = thisImage.resize(
                            (width, height), Image.NEAREST)
                        ext = ".jpg"
                        image.save(currentImage)
