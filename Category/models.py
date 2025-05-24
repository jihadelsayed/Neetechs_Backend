from django.db import models
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill  # , ResizeToFill


def cat_upload_location(instance, filename, **kwargs):
	"""
	Generates the upload path for category images.
	
	Args:
		instance: The ModelCategory instance being saved.
		filename: The original filename of the uploaded image.
		
	Returns:
		str: The generated file path for the image.
		
	Note:
		This function uses `instance.employee.id` in the path.
		However, the `ModelCategory` model does not explicitly define an `employee` field.
		This suggests the `employee` attribute might be added dynamically,
		inherited, or this function might be intended for a different model.
		If `ModelCategory` instances are not expected to have an `employee` attribute,
		this will cause an AttributeError.
	"""
	file_path = 'service/{employee_id}/{name}-{filename}'.format(
			employee_id=str(instance.employee.id), name=str(instance.name), filename=filename
		) 
	return file_path

class ModelCategory(models.Model):
	"""
	Represents a category for services or products.
	Categories can be hierarchical, allowing for subcategories through the 'parent' field.
	"""
	name = models.CharField(max_length=255)  # The name of the category.
	parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE) # Optional parent category for hierarchical structure.
	description = models.CharField(max_length=896)  # A detailed description of the category.

	img = ProcessedImageField(format='PNG', processors=[ResizeToFill(128, 128)], options={'quality': 70},default='CategoryDefaultImage.jpg', upload_to=cat_upload_location, blank=True) # Image for the category, processed and resized.
	createdAt = models.DateTimeField(auto_now_add=True, verbose_name="date published") # Timestamp when the category was created.
	updatedAt = models.DateTimeField(auto_now=True, verbose_name="date updated") # Timestamp when the category was last updated.

	# TODO: Uncomment and review this Meta class if specific ordering or verbose names are needed.
	# class Meta:
	#     verbose_name = "Category"
	#     verbose_name_plural = "Categories"
	#     ordering = ['title'] # Note: 'title' is not a field in this model, likely 'name' was intended.

	def __str__(self):
		return self.name