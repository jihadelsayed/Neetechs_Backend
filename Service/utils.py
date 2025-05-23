"""Utility functions for image processing, including validation and rotation,
for the Service app.
"""
#import cv2 # Commented out as it's not used in the current active code.
import os
from PIL import Image, ExifTags

def is_image_aspect_ratio_valid(img_url):
	"""
	Validates if the aspect ratio of an image is acceptable.
	NOTE: Currently, this validation is disabled and always returns True.
	"""
	# TODO: This aspect ratio validation logic using OpenCV is commented out.
	# If this validation is required, ensure OpenCV (cv2) is a project dependency
	# and uncomment/test this section. Otherwise, this function can be removed
	# or the logic implemented using Pillow if preferred and feasible.
	#img = cv2.imread(img_url)
	#dimensions = tuple(img.shape[1::-1]) # gives: (width, height)
	#aspect_ratio = dimensions[0] / dimensions[1] # divide w / h
	#if aspect_ratio < 1:
	#	return False
	return True


def is_image_size_valid(img_url, mb_limit):
	"""
	Checks if the size of an image file at `img_url` exceeds `mb_limit`.

	Args:
		img_url (str): Path to the image file.
		mb_limit (int): Maximum allowed size in bytes.
	
	Returns:
		bool: True if the image size is within the limit, False otherwise.
	"""
	image_size = os.path.getsize(img_url)
	if image_size > mb_limit:
		return False
	return True

def rotate_image(img):
  """
  Rotates an image based on its EXIF orientation tag.
  The `img` parameter should be a path to the image file.
  The image is rotated in place (overwriting the original file).
  """
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
    image.save(img) # Overwrites the original image file.
    image.close()
    return image # Returns the Pillow Image object.
  except (AttributeError, KeyError, IndexError):
    # Silently ignore errors if EXIF data is missing or malformed.
    # Consider logging these errors for debugging if issues arise.
    pass