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
	"""
	Generates the upload path for service post images.
	The path is structured as: service/<employee_id>/<title>-<filename>.

	Args:
		instance: The ServicePost instance being saved.
		filename: The original filename of the uploaded image.
		**kwargs: Additional keyword arguments (not used).

	Returns:
		str: The generated file path for the image.
	"""
	file_path = 'service/{employee_id}/{title}-{filename}'.format(
			employee_id=str(instance.employee.id), title=str(instance.title), filename=filename
		) 
	return file_path

def cat_upload_location(instance, filename, **kwargs):
	"""
	Generates the upload path for category images.
	The path is structured as: service/<employee_id>/<name>-<filename>.

	Args:
		instance: The ModelCategory instance being saved.
		filename: The original filename of the uploaded image.
		**kwargs: Additional keyword arguments (not used).

	Returns:
		str: The generated file path for the image.
	"""
	# NOTE: This function seems very similar to `cat_upload_location` in `Category/models.py`. Consider refactoring to a common utility if they serve the same purpose.
	file_path = 'service/{employee_id}/{name}-{filename}'.format(
			employee_id=str(instance.employee.id), name=str(instance.name), filename=filename
		) 
	return file_path

class ModelCategory(models.Model):
    """
    Represents a category for services, associated with an employee.
    NOTE: This model seems redundant with `Category.models.ModelCategory`.
    Consider consolidating to avoid data duplication and maintain a single source of truth for categories.
    """
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # The employee who might have created or is associated with this category.
    name = models.CharField(max_length=100, verbose_name="Category") # The name of the category.
    img = ProcessedImageField(format='PNG', processors=[ResizeToFill(128, 128)], options={'quality': 70},default='CategoryDefaultImage.jpg', upload_to=cat_upload_location, blank=True) # Image for the category.
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="date published") # Timestamp of creation. Note: Non-snake_case.
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="date updated") # Timestamp of last update. Note: Non-snake_case.
    
    # TODO: Review if this Meta class is needed. If so, ensure 'title' is a valid field for ordering or change to 'name'.
    # class Meta:
    #     verbose_name = "Category"
    #     verbose_name_plural = "Categories"
    #     ordering = ['title']

    def __str__(self):
        return self.name

class ModelSubCategory(models.Model):
    """
    Represents a sub-category under a main ModelCategory.
    NOTE: This model seems redundant with potential hierarchical structures in `Category.models.ModelCategory`
    or a separate SubCategory model in the `Category` app. Consider consolidation.
    """
    Category = models.ForeignKey(ModelCategory, on_delete=models.CASCADE) # The parent category. Note: Non-snake_case (should be `category`).
    name = models.CharField(max_length=100, verbose_name="Under category") # The name of the sub-category. 'Under category' is Swedish for sub-category.
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="date published") # Timestamp of creation. Note: Non-snake_case.
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="date updated") # Timestamp of last update. Note: Non-snake_case.
    def __str__(self):
        return self.name

class ModelCountry(models.Model):
    """
    Represents a country. Used to categorize services or user locations.
    """
    name = models.CharField(max_length=30) # The name of the country.
    objects = models.Manager()  # Default model manager.

    def __str__(self):
        return self.name

class ModelState(models.Model):
    """
    Represents a state, region, or province within a country.
    Linked to a ModelCountry instance.
    """
    country = models.ForeignKey(ModelCountry, on_delete=models.CASCADE) # The country this state belongs to.
    name = models.CharField(max_length=30) # The name of the state.

    def __str__(self):
        return self.name


# Create your models here.
class ServicePost(models.Model):
    """
    Represents a service posting made by an employee/user on the platform.
    Includes details about the service, pricing, location, images, and status.
    """
    class PostObjects(models.Manager):
        """Custom manager for ServicePost to filter posts by status."""
        def get_queryset(self):
            # Note: This filter currently uses `StatusOptions='published'`.
            # `StatusOptions` is a tuple of choices for the `status` field.
            # This should likely filter on the `status` field itself, e.g., `super().get_queryset().filter(status='published')`.
            return super().get_queryset().filter(StatusOptions='published')

    StatusOptions= ( # Defines the possible statuses for a service post.
        ('draft','Draft'),      # Service post is a draft, not visible publicly.
        ('published','Published'),# Service post is published and visible.
    )
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # The user who created this service post.

    title = models.CharField(max_length=50, null=False, blank=False) # Title of the service post.
    stripeId = models.CharField(max_length=200,null=True, blank=True) # Stripe ID associated with this service, if applicable. Note: Non-snake_case.
    site_id = models.CharField(max_length=50, null=True, blank=True) # Site-specific identifier, likely related to the employee's site_id.
    createdAt = models.DateTimeField(null=True, blank=True,auto_now_add=True, verbose_name="date published") # Timestamp when the post was created. Note: Non-snake_case.
    updatedAt = models.DateTimeField(null=True, blank=True,auto_now=True, verbose_name="date updated") # Timestamp when the post was last updated. Note: Non-snake_case.
    slug = models.SlugField(max_length=500,blank=True, unique=True) # URL-friendly slug for the service post.
    pris = models.IntegerField() # Field 'pris' (Swedish: price). Consider renaming to 'price'.
    bedomning = models.DecimalField(default=0, decimal_places=1, max_digits=2, validators=[MaxValueValidator(5),MinValueValidator(0)]) # Field 'bedomning' (Swedish: rating/assessment). Consider renaming to 'rating'.
    beskrivning = models.TextField(max_length=500, blank=True) # Field 'beskrivning' (Swedish: description). Consider renaming to 'description'.
    status = models.CharField(max_length=10,choices=StatusOptions, # Current status of the service post (e.g., draft, published).
        default="published", verbose_name="Is published?")
    tillganligFran = models.DateTimeField(default=timezone.now) # Field 'tillganligFran' (Swedish: availableFrom). Consider renaming to 'available_from'.
    tillganligTill = models.DateTimeField(default=timezone.now) # Field 'tillganligTill' (Swedish: availableTo). Consider renaming to 'available_to'.
    image = ProcessedImageField(default='ServiceDefaultImage.jpg',format='PNG', processors=[ResizeToFill(512, 512)], options={'quality': 70}, upload_to=upload_location, blank=False, null=False) # Main image for the service.
    image2 = ProcessedImageField(format='PNG', processors=[ResizeToFill(512, 512)], options={'quality': 70}, upload_to=upload_location, blank=True, null=True) # Optional additional image.
    image3 = ProcessedImageField(format='PNG', processors=[ResizeToFill(512, 512)], options={'quality': 70}, upload_to=upload_location, blank=True, null=True) # Optional additional image.
    image4 = ProcessedImageField(format='PNG', processors=[ResizeToFill(512, 512)], options={'quality': 70}, upload_to=upload_location, blank=True, null=True) # Optional additional image.
    image5 = ProcessedImageField(format='PNG', processors=[ResizeToFill(512, 512)], options={'quality': 70}, upload_to=upload_location, blank=True, null=True) # Optional additional image.
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="post_like", blank=True) # Users who liked this service post.
    disLikes = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="post_disLikes", blank=True) # Users who disliked this service post.
    # TODO: Review or remove these commented-out fields.
    #likes = models.ManyToManyField(ModelLikes,related_name="post_like", on_delete=models.CASCADE, blank=True)
    #disLikes = models.ManyToManyField(ModelDisLikes,related_name="post_disLikes", on_delete=models.CASCADE, blank=True)
    #comments = models.ManyToManyField(ModelComments,related_name="post_comments", on_delete=models.CASCADE, blank=True)

    category = models.CharField(max_length=1024, blank=True, null=True) # Category of the service. Consider ForeignKey to ModelCategory or Category.models.ModelCategory.
    enhet = models.CharField(max_length=30, blank=True, null=True) # Field 'enhet' (Swedish: unit). Consider renaming to 'unit' (e.g., per hour, per item).
    underCategory = models.CharField(max_length=1024, blank=True, null=True) # Sub-category of the service. Consider ForeignKey to ModelSubCategory or similar. Note: Non-snake_case.
    country = models.CharField(verbose_name="Country", max_length=1024, blank=True, null=True) # Country where service is offered. Corrected verbose_name from "contry".
    state = models.CharField(verbose_name="State/County", max_length=1024, blank=True, null=True) # State/County. Changed verbose_name from "Lansting".
    city = models.CharField(verbose_name="City/Municipality", max_length=1024, blank=True, null=True) # City/Municipality. Changed verbose_name from "Kommun".
    AboutSeller = models.CharField(verbose_name="About Seller", max_length=1024, blank=True, null=True) # Information about the seller. Note: Non-snake_case. Consider renaming to `about_seller`.
    sellerName = models.CharField(verbose_name="Seller Name", max_length=1024, blank=True, null=True) # Name of the seller. Note: Non-snake_case. Consider renaming to `seller_name`.
    expiration_date = models.DateTimeField(default=datetime.now() + timedelta(days=30),auto_now=False, auto_now_add=False, null=True, blank=True) # Date when the service post expires.

    objects = models.Manager()  # Default model manager.
    postobjects = PostObjects()  # Custom manager for filtering published posts.
    
    class Meta:
        ordering = ('-updatedAt',) # Default ordering for queries, by last updated timestamp descending. Note: `updatedAt` is non-snake_case.

    def __str__(self):
        return self.title



def _createHash():
   """
   Generates a 10-character long hexadecimal string from 5 random bytes.
   This can be used for creating unique identifiers.

   Returns:
       str: A 10-character hexadecimal string.
   """
   return hexlify(os.urandom(5)).decode()


@receiver(post_delete, sender=ServicePost)
def submission_delete(sender, instance, **kwargs):
	"""
	Signal receiver that deletes the associated image file when a ServicePost instance is deleted.
	Connected to the `post_delete` signal from the `ServicePost` sender.
	"""
	instance.image.delete(False) # False ensures the model field is not saved again after deletion.


def pre_save_service_post_receiever(sender, instance, *args, **kwargs):
	"""
	Signal receiver that populates certain fields of a ServicePost instance before it's saved.
	Connected to the `pre_save` signal from the `ServicePost` sender.

	Populates:
	- `slug`: Generates a URL-friendly slug from employee email, title, and a hash if not already set.
	- `site_id`: Copies from the employee's `site_id` if not set.
	- `AboutSeller`: Copies from the employee's `about` field if not set.
	- `sellerName`: Copies from the employee's `first_name` if not set.
	"""
	if not instance.slug:
		# FIXME: Slug generation uses str(_createHash) which refers to the function object, not its return value. It should be _createHash().
		instance.slug = slugify(instance.employee.email + "-" + instance.title + "-" + str(_createHash))
	if not instance.site_id:
		instance.site_id = instance.employee.site_id
	if not instance.AboutSeller: # Note: Non-snake_case
		instance.AboutSeller = instance.employee.about
	if not instance.sellerName: # Note: Non-snake_case
		instance.sellerName = instance.employee.first_name
pre_save.connect(pre_save_service_post_receiever, sender=ServicePost)


# TODO: Review or remove these commented-out model definitions.
#class ModelLikes(models.Model):
  #  likes = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="post_like", blank=True)
 #   postNumber = models.ForeignKey(ServicePost, on_delete=models.CASCADE)
    


# TODO: Review or remove these commented-out model definitions.
#class ModelDisLikes(models.Model):
  #  disLikes = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="post_disLikes", blank=True)
 #   postNumber = models.ForeignKey(ServicePost, on_delete=models.CASCADE)



class ModelComments(models.Model):
    """
    Represents a comment made on a ServicePost.
    """
    comment = models.CharField(verbose_name="Seller name", max_length=1024, blank=True) # The content of the comment. Verbose name "Seller name" seems incorrect for a comment field.
    postNumber = models.ForeignKey(ServicePost, on_delete=models.CASCADE) # The ServicePost to which this comment is associated. Note: Non-snake_case. Consider renaming to `service_post`.

