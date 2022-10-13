from django.db import models
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill#, ResizeToFill

def report_upload_location(instance, filename, **kwargs):
	file_path = 'home/{name}-{filename}'.format(
			name=str(instance.title), filename=filename
		) 
	return file_path

# Create your models here.
class ReportMoudel(models.Model):
    addedAt = models.DateTimeField(auto_now_add=True, verbose_name="Added at")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    title = models.CharField(max_length=100, null=False, blank=False)
    orderNumber = models.CharField(max_length=100)
    type = models.CharField(max_length=500)
    message = models.CharField(max_length=500, null=False, blank=False)
    image = ProcessedImageField(format='PNG', processors=[ResizeToFill(512, 512)], options={'quality': 70}, upload_to=report_upload_location, blank=True)
    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        ordering = ['title']

    def __str__(self):
        return self.title