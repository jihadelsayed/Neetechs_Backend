import os

from django.conf import settings
from django.core import serializers as ser
from django.core.files.storage import FileSystemStorage, default_storage
from rest_framework import serializers
from rest_framework.serializers import ImageField

from Service.models import (ModelCategory, ModelComments, ModelCountry,
                            ModelState, ModelSubCategory, ServicePost)

#from rest_framework_recaptcha.fields import ReCaptchaField


IMAGE_SIZE_MAX_BYTES = 2000 * 2000 * 8  # 8MB
MIN_TITLE_LENGTH = 3
MIN_BODY_LENGTH = 20


class CategorySerializer(serializers.ModelSerializer):
	children = serializers.SerializerMethodField('get_SubCategorys')

	class Meta:
		model = ModelCategory
		fields = ['pk', 'name', 'img', 'children']

	def get_SubCategorys(self, obj):
		# .last().created_at.strftime("%Y-%m-%d %I:%M %p")
		SubCategorys = ModelSubCategory.objects.filter(Category_id=obj.id)
		# print(SubCategorys)
		return SubCategorySerializer(SubCategorys, many=True).data


class AllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelCategory
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelSubCategory
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelCountry
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelState
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePost
        fields = ['city']


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePost
        fields = ['likes']


class DisLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePost
        fields = ['disLikes']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelComments
        fields = '__all__'


class ServicePostSerializer(serializers.ModelSerializer):
	site_id = serializers.SerializerMethodField('get_site_id_from_employee')
	picture = serializers.SerializerMethodField(
	    'get_profilepicture_from_employee', required=False)
#	likes = serializers.MultipleChoiceField('get_likes_from_pk')
#	disLikes = serializers.MultipleChoiceField('get_disLikes_from_pk')

	createdAt = serializers.DateTimeField(
	    format='%Y-%m-%d %I:%M %p', required=False)
	updatedAt = serializers.DateTimeField(
	    format='%Y-%m-%d %I:%M %p', required=False)
	expiration_date = serializers.DateTimeField(
	    format='%Y-%m-%d %I:%M %p', required=False)

	class Meta:
		model = ServicePost
		fields = ['pk', 'expiration_date', 'stripeId', 'createdAt', 'enhet', 'likes', 'disLikes', 'picture', 'updatedAt', 'bedomning', 'title', 'AboutSeller', 'sellerName', 'slug', 'pris',
		    'site_id', 'image', 'image2', 'image3', 'image4', 'image5', 'beskrivning', 'status', 'tillganligFran', 'tillganligTill', 'category', 'underCategory', 'country', 'state', 'city']

	def get_site_id_from_employee(self, service_post):
		site_id = service_post.employee.site_id
		return site_id

	def get_profilepicture_from_employee(self, service_post):
		picture = service_post.employee.picture.url
		return picture
#	def get_likes_from_pk(self, service_post):
#		postNumber= service_post.pk
#		postLikes = ModelLikes.objects.get(postNumber_id=postNumber).likes
#		serialized_obj = ser.serialize('json', postLikes)
#		print(serialized_obj)
#
	#	return postLikes

#	def get_disLikes_from_pk(self, service_post):
#		postNumber= service_post.pk
#		postDisLikes = ModelDisLikes.objects.get(postNumber_id=postNumber).disLikes
#		serialized_obj = ser.serialize('json', postDisLikes)

#		return postDisLikes

	def validate_image_url(self, service_post):
		image = service_post.image
		new_url = image.url
		if "?" in new_url:
			new_url = image.url[:image.url.rfind("?")]
		return new_url

	def validate_image2_url(self, service_post):
		image2 = service_post.image2
		new_url = image2.url
		if "?" in new_url:
			new_url = image2.url[:image2.url.rfind("?")]
		return new_url

	def validate_image3_url(self, service_post):
		image3 = service_post.image3
		new_url = image3.url
		if "?" in new_url:
			new_url = image3.url[:image3.url.rfind("?")]
		return new_url

	def validate_image4_url(self, service_post):
		image4 = service_post.image4
		new_url = image4.url
		if "?" in new_url:
			new_url = image4.url[:image4.url.rfind("?")]
		return new_url

	def validate_image5_url(self, service_post):
		image5 = service_post.image5
		new_url = image5.url
		if "?" in new_url:
			new_url = image5.url[:image5.url.rfind("?")]
		return new_url


class ServicePostUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = ServicePost
		fields = ['title', 'expiration_date', 'expiration_date', 'stripeId', 'pris', 'enhet', 'image', 'image2', 'image3', 'image4',
		    'image5', 'beskrivning', 'status', 'tillganligFran', 'tillganligTill', 'category', 'underCategory', 'country', 'state', 'city']


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
#	createdAt = serializers.DateTimeField(format='%Y-%m-%d %I:%M %p')
#	updatedAt = serializers.DateTimeField(format='%Y-%m-%d %I:%M %p')
	#recaptcha = ReCaptchaField()

	class Meta:
		model = ServicePost
		fields = ['title','expiration_date','stripeId','enhet', 'employee', 'pris', 'image', 'image2', 'image3', 'image4', 'image5', 'beskrivning', 'status', 'tillganligFran', 'tillganligTill', 'category', 'underCategory', 'country', 'state', 'city']
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










