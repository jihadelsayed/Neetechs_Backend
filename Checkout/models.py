

from chat.models import Thread
from django.db import models
#from Palimago import settings
#from Service.models import ServicePost

class PostObjects(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(StatusOptions='published')

class ServiceOrder(models.Model):
    #thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    StatusOptions= (
        ('requested','Requested'),
        ('confirmed','Confirmed'),
        ('canceled','Canceled'),
        ('pend','Pend'),
        ('payed','Payed'),
    )
    ordered_at = models.DateTimeField(auto_now_add=True, verbose_name="ordered_at",null=True,blank=True)
    customerIdd = models.CharField(max_length=50)
    employedIdd = models.CharField(max_length=50)
    serviceId = models.IntegerField(null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    enhet = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50)
    date = models.CharField(max_length=500)
    status = models.CharField(max_length=10,choices=StatusOptions,
        default="requested", verbose_name="Status of service:")
    objects = models.Manager()  # default manager
    postobjects = PostObjects()  # custom manager
