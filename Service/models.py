import os
from binascii import hexlify
from datetime import datetime, timedelta

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill  # , ResizeToFill
from PIL import Image


def upload_location(instance, filename, **kwargs):
	file_path = 'service/{employee_id}/{title}-{filename}'.format(
			employee_id=str(instance.employee.id), title=str(instance.title), filename=filename
		) 
	return file_path

def cat_upload_location(instance, filename, **kwargs):
	file_path = 'service/{employee_id}/{name}-{filename}'.format(
			employee_id=str(instance.employee.id), name=str(instance.name), filename=filename
		) 
	return file_path

class ModelCategory(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Category")
    img = ProcessedImageField(format='PNG', processors=[ResizeToFill(128, 128)], options={'quality': 70},default='CategoryDefaultImage.jpg', upload_to=cat_upload_location, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="date updated")
    
    # class Meta:
    #     verbose_name = "Category"
    #     verbose_name_plural = "Categories"
    #     ordering = ['title']

    def __str__(self):
        return self.name

class ModelSubCategory(models.Model):
    Category = models.ForeignKey(ModelCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Under category")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="date updated")
    def __str__(self):
        return self.name

class ModelCountry(models.Model):
    name = models.CharField(max_length=30)
    objects = models.Manager()  # default manager

    def __str__(self):
        return self.name

class ModelState(models.Model):
    country = models.ForeignKey(ModelCountry, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# Create your models here.
class ServicePost(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(StatusOptions='published')
    StatusOptions= (
    ('draft','Draft'),
    ('published','Published'),
    )
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    title = models.CharField(max_length=50, null=False, blank=False)
    stripeId = models.CharField(max_length=200,null=True, blank=True)
    site_id = models.CharField(max_length=50, null=True, blank=True)
    createdAt = models.DateTimeField(null=True, blank=True,auto_now_add=True, verbose_name="date published")
    updatedAt = models.DateTimeField(null=True, blank=True,auto_now=True, verbose_name="date updated")
    slug = models.SlugField(max_length=500,blank=True, unique=True)
    pris = models.IntegerField()
    bedomning = models.DecimalField(default=0, decimal_places=1, max_digits=2, validators=[MaxValueValidator(5),MinValueValidator(0)])
    beskrivning = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=10,choices=StatusOptions,
        default="published", verbose_name="Is published?")
    tillganligFran = models.DateTimeField(default=timezone.now)
    tillganligTill = models.DateTimeField(default=timezone.now)
    image = ProcessedImageField(default='ServiceDefaultImage.jpg',format='PNG', processors=[ResizeToFill(512, 512)], options={'quality': 70}, upload_to=upload_location, blank=False, null=False)
    image2 = ProcessedImageField(format='PNG', processors=[ResizeToFill(512, 512)], options={'quality': 70}, upload_to=upload_location, blank=True, null=True)
    image3 = ProcessedImageField(format='PNG', processors=[ResizeToFill(512, 512)], options={'quality': 70}, upload_to=upload_location, blank=True, null=True)
    image4 = ProcessedImageField(format='PNG', processors=[ResizeToFill(512, 512)], options={'quality': 70}, upload_to=upload_location, blank=True, null=True)
    image5 = ProcessedImageField(format='PNG', processors=[ResizeToFill(512, 512)], options={'quality': 70}, upload_to=upload_location, blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="post_like", blank=True)
    disLikes = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="post_disLikes", blank=True)
    #likes = models.ManyToManyField(ModelLikes,related_name="post_like", on_delete=models.CASCADE, blank=True)
    #disLikes = models.ManyToManyField(ModelDisLikes,related_name="post_disLikes", on_delete=models.CASCADE, blank=True)
    #comments = models.ManyToManyField(ModelComments,related_name="post_comments", on_delete=models.CASCADE, blank=True)

    category = models.CharField(max_length=1024, blank=True, null=True)
    enhet = models.CharField(max_length=30, blank=True, null=True)
    underCategory = models.CharField(max_length=1024, blank=True, null=True)
    country = models.CharField(verbose_name="contry", max_length=1024, blank=True, null=True)
    state = models.CharField(verbose_name="Lansting", max_length=1024, blank=True, null=True)
    city = models.CharField(verbose_name="Kommun", max_length=1024, blank=True, null=True)
    AboutSeller = models.CharField(verbose_name="AboutSeller", max_length=1024, blank=True, null=True)
    sellerName = models.CharField(verbose_name="Seller name", max_length=1024, blank=True, null=True)
    expiration_date = models.DateTimeField(default=datetime.now() + timedelta(days=30),auto_now=False, auto_now_add=False, null=True, blank=True)

    objects = models.Manager()  # default manager
    postobjects = PostObjects()  # custom manager
    
    class Meta:
        ordering = ('-updatedAt',)

    def __str__(self):
        return self.title



def _createHash():
   """This function generate 10 character long hash"""
   return hexlify(os.urandom(5)).decode()


@receiver(post_delete, sender=ServicePost)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)


def pre_save_service_post_receiever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.employee.email + "-" + instance.title + "-" + str(_createHash))
	if not instance.site_id:
		instance.site_id = instance.employee.site_id
	if not instance.AboutSeller:
		instance.AboutSeller = instance.employee.about
	if not instance.sellerName:
		instance.sellerName = instance.employee.first_name
pre_save.connect(pre_save_service_post_receiever, sender=ServicePost)


#class ModelLikes(models.Model):
  #  likes = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="post_like", blank=True)
 #   postNumber = models.ForeignKey(ServicePost, on_delete=models.CASCADE)
    


#class ModelDisLikes(models.Model):
  #  disLikes = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="post_disLikes", blank=True)
 #   postNumber = models.ForeignKey(ServicePost, on_delete=models.CASCADE)



class ModelComments(models.Model):
    comment = models.CharField(verbose_name="Seller name", max_length=1024, blank=True)
    postNumber = models.ForeignKey(ServicePost, on_delete=models.CASCADE)

