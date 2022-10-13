from django.db import models

from Neetechs import settings


# Create your models here.
class Erfarenhet(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Added_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Added at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    company = models.CharField(max_length=100)    
    name = models.CharField(max_length=100)
    plats = models.CharField(max_length=100)
    content = models.TextField()
    started_at = models.CharField(max_length=100,verbose_name="started at")
    ended_at = models.CharField(max_length=100,verbose_name="ended at")
    objects = models.Manager()  # default manager

    class Meta:
        verbose_name = "Erfarenhet"
        verbose_name_plural = "Erfarenhets"
        ordering = ['name']

    def __str__(self):
        return self.name

class Studier(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Added_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Added at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    plats = models.CharField(max_length=100)
    objects = models.Manager()  # default manager

    content = models.TextField()
    started_at = models.CharField(max_length=100,verbose_name="started at")
    ended_at = models.CharField(max_length=100,verbose_name="ended at")

    class Meta:
        verbose_name = "Studier"
        verbose_name_plural = "Studiers"
        ordering = ['name']

    def __str__(self):
        return self.name

class Kompetenser_intyg(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Added_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Added at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    name = models.CharField(max_length=100)
    objects = models.Manager()  # default manager

    class Meta:
        verbose_name = "Kompetenser eller intyg"
        verbose_name_plural = "Kompetensers och intygs"
        ordering = ['name']

    def __str__(self):
        return self.name


class Intressen(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Added_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Added at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    name = models.CharField(max_length=100)
    objects = models.Manager()  # default manager

    class Meta:
        verbose_name = "Intressen"
        verbose_name_plural = "Intressens"
        ordering = ['name']

    def __str__(self):
        return self.name