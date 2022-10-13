#import cv2
import os
from PIL import Image, ExifTags

def is_image_aspect_ratio_valid(img_url):
	#img = cv2.imread(img_url)
	#dimensions = tuple(img.shape[1::-1]) # gives: (width, height)
	# print("dimensions: " + str(dimensions))
	#aspect_ratio = dimensions[0] / dimensions[1] # divide w / h
	# print("aspect_ratio: " + str(aspect_ratio))
	#if aspect_ratio < 1:
	#	return False
	return True


def is_image_size_valid(img_url, mb_limit):
	image_size = os.path.getsize(img_url)
	# print("image size: " + str(image_size))
	if image_size > mb_limit:
		return False
	return True

def rotate_image(img):
  try:
    image = Image.open(img)
    for orientation in ExifTags.TAGS.keys():
      if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = dict(image._getexif().items())

    if exif[orientation] == 3:
        image = image.rotate(180, expand=True)
    elif exif[orientation] == 6:
        image = image.rotate(270, expand=True)
    elif exif[orientation] == 8:
        image = image.rotate(90, expand=True)
    image.save(img)
    image.close()
    return image
  except (AttributeError, KeyError, IndexError):
    # cases: image don't have getexif
    pass