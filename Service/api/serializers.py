import os

from django.conf import settings
from django.core import serializers as ser
from django.core.files.storage import FileSystemStorage, default_storage
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.serializers import ImageField

from Service.models import (ModelCategory, ModelComments, ModelCountry,
                            ModelState, ModelSubCategory, ServicePost)

#from rest_framework_recaptcha.fields import ReCaptchaField # Assuming not used as per cleanup instruction for ServicePostCreateSerializer


IMAGE_SIZE_MAX_BYTES = 2000 * 2000 * 8  # 8MB - Maximum allowed size for image uploads (8 Megabytes).
MIN_TITLE_LENGTH = 3 # Minimum allowed length for title fields.
MIN_BODY_LENGTH = 20 # Minimum allowed length for body/description fields.



class SubCategorySerializer(serializers.ModelSerializer):
	"""Serializes all fields for ModelSubCategory instances."""
	class Meta:
		model = ModelSubCategory
		fields = '__all__' # Includes all fields from the ModelSubCategory model.


class ServiceCategorySerializer(serializers.ModelSerializer):
	"""
	Serializes ModelCategory instances, including its subcategories
	via the `get_SubCategorys` method.
	"""
	children = serializers.SerializerMethodField('get_SubCategorys') # Field to embed subcategories.

	class Meta:
		model = ModelCategory
		# Specifies fields to include in the serialized output.
		fields = ['pk', 'name', 'img', 'children']
		ref_name = "ServiceCategory"

	@extend_schema_field(SubCategorySerializer(many=True))
	def get_SubCategorys(self, obj):
		"""
		Retrieves and serializes subcategories related to the given ModelCategory instance.
		NOTE: This method name uses 'SubCategorys' which is unconventional.
		Consider if this is similar to Category.serializers.CategorySerializer's get_children method.
		"""
		subcategories = ModelSubCategory.objects.filter(Category_id=obj.id)
		return SubCategorySerializer(subcategories, many=True).data


class AllCategorySerializer(serializers.ModelSerializer):
    """Serializes all fields for ModelCategory instances."""
    class Meta:
        model = ModelCategory
        fields = '__all__' # Includes all fields from the ModelCategory model.


class CountrySerializer(serializers.ModelSerializer):
    """Serializes all fields for ModelCountry instances."""
    class Meta:
        model = ModelCountry
        fields = '__all__' # Includes all fields from the ModelCountry model.


class StateSerializer(serializers.ModelSerializer):
    """Serializes all fields for ModelState instances."""
    # FIXME: The model is currently set to ModelCategory, which is incorrect.
    # It should be ModelState.
    class Meta:
        model = ModelCategory # Should be ModelState
        fields = '__all__' # Includes all fields from the specified model.


class CitySerializer(serializers.ModelSerializer):
    """
    Serializes only the 'city' field from ServicePost instances.
    Likely used for specific use cases where only city information is needed.
    """
    class Meta:
        model = ServicePost
        fields = ['city'] # Exposes only the 'city' field.


class LikesSerializer(serializers.ModelSerializer):
    """
    Serializes only the 'likes' field from ServicePost instances.
    Likely used for operations specifically related to service post likes.
    """
    class Meta:
        model = ServicePost
        fields = ['likes'] # Exposes only the 'likes' field (ManyToManyField).


class DisLikesSerializer(serializers.ModelSerializer):
    """
    Serializes only the 'disLikes' field from ServicePost instances.
    Likely used for operations specifically related to service post dislikes.
    """
    class Meta:
        model = ServicePost
        fields = ['disLikes'] # Exposes only the 'disLikes' field (ManyToManyField).


class CommentsSerializer(serializers.ModelSerializer):
    """Serializes all fields for ModelComments instances."""
    class Meta:
        model = ModelComments
        fields = '__all__' # Includes all fields from the ModelComments model.


class ServicePostSerializer(serializers.ModelSerializer):
	"""
	Serializes ServicePost instances for read operations, including related employee
	information like site_id and profile picture URL.
	It also explicitly formats DateTimeFields.
	"""
	site_id = serializers.SerializerMethodField('get_site_id_from_employee') # Custom field for employee's site_id.
	picture = serializers.SerializerMethodField( # Custom field for employee's profile picture URL.
	    'get_profilepicture_from_employee', required=False)

	# Explicitly defining DateTimeField formats for consistent API output.
	createdAt = serializers.DateTimeField(
	    format='%Y-%m-%d %I:%M %p', required=False) # Formats createdAt timestamp.
	updatedAt = serializers.DateTimeField(
	    format='%Y-%m-%d %I:%M %p', required=False) # Formats updatedAt timestamp.
	expiration_date = serializers.DateTimeField(
	    format='%Y-%m-%d %I:%M %p', required=False) # Formats expiration_date timestamp.

	class Meta:
		model = ServicePost
		# Includes most fields from ServicePost, plus custom method fields.
		fields = ['pk', 'expiration_date', 'stripeId', 'createdAt', 'enhet', 'likes', 'disLikes', 'picture', 'updatedAt', 'bedomning', 'title', 'AboutSeller', 'sellerName', 'slug', 'pris',
		    'site_id', 'image', 'image2', 'image3', 'image4', 'image5', 'beskrivning', 'status', 'tillganligFran', 'tillganligTill', 'category', 'underCategory', 'country', 'state', 'city']

	@extend_schema_field(serializers.CharField())
	def get_site_id_from_employee(self, service_post):
		"""Retrieves the site_id of the employee associated with the service post."""
		site_id = service_post.employee.site_id
		return site_id

	@extend_schema_field(serializers.URLField())
	def get_profilepicture_from_employee(self, service_post):
		"""Retrieves the URL of the profile picture for the employee associated with the service post."""
		# Note: Accessing .url might cause issues if the image file doesn't exist or storage fails.
		# Consider adding error handling or using a method that safely gets the URL.
		picture = service_post.employee.picture.url
		return picture

	def validate_image_url(self, service_post):
		"""Removes query parameters from the main image URL, if present."""
		image = service_post.image
		new_url = image.url
		if "?" in new_url:
			new_url = image.url[:image.url.rfind("?")]
		return new_url

	def validate_image2_url(self, service_post):
		"""Removes query parameters from the image2 URL, if present."""
		image2 = service_post.image2
		new_url = image2.url
		if "?" in new_url:
			new_url = image2.url[:image2.url.rfind("?")]
		return new_url

	def validate_image3_url(self, service_post):
		"""Removes query parameters from the image3 URL, if present."""
		image3 = service_post.image3
		new_url = image3.url
		if "?" in new_url:
			new_url = image3.url[:image3.url.rfind("?")]
		return new_url

	def validate_image4_url(self, service_post):
		"""Removes query parameters from the image4 URL, if present."""
		image4 = service_post.image4
		new_url = image4.url
		if "?" in new_url:
			new_url = image4.url[:image4.url.rfind("?")]
		return new_url

	def validate_image5_url(self, service_post):
		"""Removes query parameters from the image5 URL, if present."""
		image5 = service_post.image5
		new_url = image5.url
		if "?" in new_url:
			new_url = image5.url[:image5.url.rfind("?")]
		return new_url


class ServicePostUpdateSerializer(serializers.ModelSerializer):
	"""
	Serializer for updating existing ServicePost instances.
	Includes a specific subset of fields that are considered updatable.
	"""
	class Meta:
		model = ServicePost
		# Specifies the fields that can be updated.
		# Note: 'expiration_date' is listed twice.
		fields = ['title', 'expiration_date', 'expiration_date', 'stripeId', 'pris', 'enhet', 'image', 'image2', 'image3', 'image4',
		    'image5', 'beskrivning', 'status', 'tillganligFran', 'tillganligTill', 'category', 'underCategory', 'country', 'state', 'city']


# TODO: Review this custom validate() method. If image validation logic is still needed, integrate it properly or remove this block.
"""
	def validate(self, service_post):
		try:
			title = service_post['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError(
				    {"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

			beskrivning = service_post['beskrivning']
			if len(beskrivning) < MIN_BODY_LENGTH:
				raise serializers.ValidationError(
				    {"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})

			image = service_post['image']
			url = os.path.join(settings.TEMP , str(image))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in image.chunks():
					destination.write(chunk)
				destination.close()

			# Check image size
			if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
				os.remove(url)
				raise serializers.ValidationError(
				    {"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

			# Check image aspect ratio
			if not is_image_aspect_ratio_valid(url):
				os.remove(url)
				raise serializers.ValidationError(
				    {"response": "Image height must not exceed image width. Try a different image."})

			os.remove(url)
		except KeyError:
			pass
		return service_post
"""


class ServicePostCreateSerializer(serializers.ModelSerializer):
	"""
	Serializer for creating new ServicePost instances.
	Defines the fields required for creating a new service post.
	"""
	# Commented out DateTimeFields, assuming default DRF handling or that they are not set at creation.
#	createdAt = serializers.DateTimeField(format='%Y-%m-%d %I:%M %p')
#	updatedAt = serializers.DateTimeField(format='%Y-%m-%d %I:%M %p')
	# recaptcha = ReCaptchaField() # Assuming 'rest_framework_recaptcha' is not used based on earlier cleanup.

	class Meta:
		model = ServicePost
		# Specifies the fields available during the creation of a ServicePost.
		fields = ['title','expiration_date','stripeId','enhet', 'employee', 'pris', 'image', 'image2', 'image3', 'image4', 'image5', 'beskrivning', 'status', 'tillganligFran', 'tillganligTill', 'category', 'underCategory', 'country', 'state', 'city']
		read_only_fields = ['employee']
	
# TODO: CRITICAL REVIEW - This custom save() method manually handles instance creation, file saving, and validation.
# This is highly unconventional for DRF ModelSerializers and prone to errors.
# It likely duplicates DRF/Django's built-in functionality.
# Consider removing this entirely and relying on the default ModelSerializer behavior,
# moving custom validation to .validate() or field validators.
	"""
	def save(self):
		try:
			image = self.validated_data['image']			
			image2 = self.validated_data['image2']
			image3 = self.validated_data['image3']
			image4 = self.validated_data['image4']
			image5 = self.validated_data['image5']
			title = self.validated_data['title']
			enhet = self.validated_data['enhet']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})
			
			beskrivning = self.validated_data['beskrivning']
			if len(beskrivning) < MIN_BODY_LENGTH:
				raise serializers.ValidationError({"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})
			pris = self.validated_data['pris']
			status = self.validated_data['status']
			tillganligFran = self.validated_data['tillganligFran']
			tillganligTill = self.validated_data['tillganligTill']
			category = self.validated_data['category']
			underCategory = self.validated_data['underCategory']
			country = self.validated_data['country']
			state = self.validated_data['state']
			city = self.validated_data['city']
			
			service_post = ServicePost(
								employee=self.validated_data['employee'],
								title=title,
								pris=pris,
								beskrivning=beskrivning,
								status=status,
								tillganligFran=tillganligFran,
								tillganligTill=tillganligTill,
								category=category,
								underCategory=underCategory,
								country=country,
								state=state,
								city=city,
								image=image,
								image2=image2,
								image3=image3,
								image4=image4,
								image5=image5,
								)

			url = os.path.join(settings.MEDIA_ROOT , str(image))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
			 	for chunk in image.chunks():
			 		destination.write(chunk)
			 	destination.close()

			# # Check image size
			if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
			 	os.remove(url)
			 	raise serializers.ValidationError({"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

			# # Check image aspect ratio
			if not is_image_aspect_ratio_valid(url):
			 	os.remove(url)
			 	raise serializers.ValidationError({"response": "Image height must not exceed image width. Try a different image."})

			# os.remove(url)
			service_post.save()
			return service_post
		except KeyError:
			raise serializers.ValidationError({"response": "You must have a title, some content, and an image."})
	"""





