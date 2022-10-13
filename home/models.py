from django.db import models
#from athumb.fields import ImageWithThumbsField
from imagekit.models.fields import ProcessedImageField

from imagekit.processors import ResizeToFill#, ResizeToFill

def Home_upload_location(instance, filename, **kwargs):
	file_path = 'home/{name}-{filename}'.format(
			name=str(instance.name), filename=filename
		) 
	return file_path
# Create your models here.

class HomeSliderMoudel(models.Model):
    Added_at = models.DateTimeField(auto_now_add=True, verbose_name="Added at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    img_x_large = ProcessedImageField(format='PNG', processors=[ResizeToFill(512, 512)], options={'quality': 70}, upload_to=Home_upload_location, blank=True)

   # img = models.ImageField(default='HomeDefaultImage.jpg', upload_to=Home_upload_location, blank=True)
   # img_large = ImageSpecField(source='img', processors=[ResizeToFill(512, 512)], format='JPEG', options={'quality': 70})
    #img_medium = ImageSpecField(source='img', processors=[ResizeToFill(256, 256)], format='JPEG', options={'quality': 70})
   # img_small = ImageSpecField(source='img', processors=[ResizeToFill(128, 128)], format='JPEG', options={'quality': 70})
    #img_tag = ImageSpecField(source='img', processors=[ResizeToFill(28, 28)], format='JPEG', options={'quality': 70})

    class Meta:
        verbose_name = "Home slider"
        verbose_name_plural = "Home sliders"
        ordering = ['name']

    def __str__(self):
        return self.name

class HomeContainersModel(models.Model):
    Added_at = models.DateTimeField(auto_now_add=True, verbose_name="Added at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    #ContainerId = models.IntegerField(max_length=100)
   # img = models.ImageField(default='HomeDefaultImage.jpg', upload_to=Home_upload_location, blank=True)
   # img_large = ImageSpecField(source='img', processors=[ResizeToFill(512, 512)], format='PNG', options={'quality': 70})
   # img_medium = ImageSpecField(source='img', processors=[ResizeToFill(256, 256)], format='PNG', options={'quality': 70})
   # img_small = ImageSpecField(source='img', processors=[ResizeToFill(128, 128)], format='PNG', options={'quality': 70})
   # img_tag = ImageSpecField(source='img', processors=[ResizeToFill(28, 28)], format='PNG', options={'quality': 70})
    
    img_x_large = ProcessedImageField(format='PNG', processors=[ResizeToFill(512, 512)], options={'quality': 70}, upload_to=Home_upload_location, blank=True)

        
    class Meta:
        verbose_name = "Home container"
        verbose_name_plural = "Home containers"
        ordering = ['name']

    def __str__(self):
        return self.name
