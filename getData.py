#!/usr/bin/env python
# This file will pull jordans from flight club and
# store them in folders name after them
import requests
import urllib2
import os
import errno
from bs4 import BeautifulSoup
import random
import string
from PIL import Image
from PIL import ImageChops
from requests.auth import HTTPDigestAuth
import json
import sys


def makeDirectories():

    for i in range(1, 24):
        try:
            os.makedirs(str(i))
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise


def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


def get_jordan_images_from_flight_club(start=1, end=23):

    for j in range(start, end + 1):
        link = "https://www.flightclub.com/air-jordans/air-jordan-" + str(j)

        r = requests.get(link)

        data = r.text

        soup = BeautifulSoup(data, "html5lib")
        n = 0
        if soup.find_all(class_="page-number"):
            n = len(soup.find_all(class_="page-number")) / 2

        number_pages = 1 if n == 0 else n
        print("Jordan - " + str(j) + "Num pages - " + str(number_pages))

        for p in range(1, number_pages + 1):
            link = link + "/?=" + str(p)
            data = r.text
            soup = BeautifulSoup(data, "html5lib")
            jordans = soup.find_all(class_="category-products")
            for i, jordan in enumerate(jordans):

                products = jordan.find_all(class_="product-image")
                for k, images in enumerate(products):

                    img = images.img['src']

                    img_data = requests.get(img).content

                    imagepath = str(j) + '/' + randomword(10) + '.jpg'
                    with open(imagepath, 'wb') as handler:
                        handler.write(img_data)


def compareImages(im1, im2):

    image1 = Image.open(im1)
    image2 = Image.open(im2)

    return (tuple(image1.getdata()) == tuple(image2.getdata()))


def getImageData(img):
    data = tuple(img.getdata())
    return hash(data)


def isDuplicateImage(image, directory):
    image = Image.open(image)
    for subdir, dirs, images in os.walk(directory):
        for currentImage in images:
            currentImage = directory + currentImage
            currentImage = Image.open(currentImage)
            if compareImages(currentImage, image):
                os.remove(currentImage)


def get_jordans_from_bing(start=2, end=23):

    headers = {'Ocp-Apim-Subscription-Key': '91efc80b326247049766e0b8be5976ba', }

    for i in range(start, end + 1):

        params = (('q', 'jordan ' + str(i)),
                  ('mkt', 'en-us'), ('count', '150'), )

        data = requests.get(
            'https://api.cognitive.microsoft.com/bing/v5.0/images/search',
            headers=headers,
            params=params)

        jordans = data.json()

        for jordan_dict in jordans['queryExpansions']:

            url = jordan_dict['thumbnail']['thumbnailUrl']

            imagepath = str(i) + '/' + randomword(10) + '.jpg'

            img_data = requests.get(url).content

            with open(imagepath, 'wb') as handler:

                handler.write(img_data)


# for key in jordans.keys():
#     print(jordans[key])

# list1 = hash(tuple([1, 2, 4]))
# list2 = hash(tuple([1, 2, 3, 4]))
# str1 = "1234"
# str2 = "1234"
# print(hash(str1), hash(str2))
# print(list2, list1)
# get_jordans_from_bing()
# makeDirectories()
# get_jordan_images_from_flight_club(1, 23)
# isDuplicateImage("10/aexolopjge.jpg", "10/")

# for i, link in enumerate(jordans):
#     img = link.img['src']

# parse html for image tags

# create directories named after the respective model

# download image to directory
# total = 0
# for j in range(21, 24):
#     for p in range(1, 10):

#         link = "https://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_nkw=jordan+" + \
#             str(j) + "&_pgn=" + str(p) + "&_skc=192&rt=nc"

#         print("Jordan " + str(j))
#         r = requests.get(link)

#         data = r.text

#         soup = BeautifulSoup(data, "html5lib")

#         grid = soup.find_all(class_="img")
#         for i, gridSet in enumerate(grid):
#             for k, sneakers in enumerate(gridSet):

#                 image = sneakers.find("img")

#                 if image != -1 and image is not None:
#                     total += 1
#                     img = None
#                     try:
#                         if image.attrs['imgurl']:

#                             img = image.attrs['imgurl']

#                             img_data = requests.get(img).content

#                             imagepath = str(j) + '/' + randomword(10) + '.jpg'

#                             with open(imagepath, 'wb') as handler:
#                                 print("written to file")
#                                 handler.write(img_data)

#                     except KeyError as e:
#                         print("No imgurl")


# print(str(total))
