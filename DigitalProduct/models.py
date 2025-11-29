from django.db import models
from django.utils.text import slugify
from django.conf import settings

from Neetechs.settings.storage import ProductsStorage, UploadsStorage


class DigitalProductCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        verbose_name_plural = "Digital product categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class DigitalProduct(models.Model):
    category = models.ForeignKey(
        DigitalProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)

    stripe_price_id = models.CharField(
        max_length=120,
        blank=True,
        help_text="Stripe Price ID for this product.",
    )

    thumbnail = models.ImageField(
        storage=UploadsStorage(),
        upload_to="digital_products/thumbnails/",
        blank=True,
        null=True,
    )

    file = models.FileField(
        storage=ProductsStorage(),
        upload_to="digital_products/files/",
        blank=True,
        null=True,
    )

    version = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            idx = 1
            while DigitalProduct.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                idx += 1
                slug = f"{base}-{idx}"
            self.slug = slug
        super().save(*args, **kwargs)


class DigitalProductBundle(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)

    products = models.ManyToManyField(
        DigitalProduct,
        related_name="bundles",
        blank=True,
    )

    stripe_price_id = models.CharField(
        max_length=120,
        blank=True,
        help_text="Stripe Price ID for the whole bundle.",
    )

    thumbnail = models.ImageField(
        storage=UploadsStorage(),
        upload_to="digital_products/bundles/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            idx = 1
            while DigitalProductBundle.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                idx += 1
                slug = f"{base}-{idx}"
            self.slug = slug
        super().save(*args, **kwargs)


class DigitalProductPurchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(DigitalProduct, on_delete=models.CASCADE)
    version = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    stripe_payment_intent = models.CharField(
        max_length=120, blank=True, help_text="Stripe payment intent ID"
    )

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user} -> {self.product} (v{self.version})"


class DigitalProductBundlePurchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bundle = models.ForeignKey(DigitalProductBundle, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    stripe_payment_intent = models.CharField(
        max_length=120, blank=True, help_text="Stripe payment intent ID"
    )

    class Meta:
        unique_together = ("user", "bundle")

    def __str__(self):
        return f"{self.user} -> bundle {self.bundle}"
