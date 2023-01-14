from django.db import models
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill  # , ResizeToFill


def cat_upload_location(instance, filename, **kwargs):
	file_path = 'service/{employee_id}/{name}-{filename}'.format(
			employee_id=str(instance.employee.id), name=str(instance.name), filename=filename
		) 
	return file_path

class ModelCategory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    description = models.CharField(max_length=896)

    img = ProcessedImageField(format='PNG', processors=[ResizeToFill(128, 128)], options={'quality': 70},default='CategoryDefaultImage.jpg', upload_to=cat_upload_location, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="date updated")
    
    # class Meta:
    #     verbose_name = "Category"
    #     verbose_name_plural = "Categories"
    #     ordering = ['title']

    def __str__(self):
        return self.name