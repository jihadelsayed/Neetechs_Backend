

from django.db import models

from chat.models import Thread

#from Service.models import ServicePost

class PostObjects(models.Manager):
    """
    Custom manager for ServiceOrder objects.
    Intended to provide a way to filter ServiceOrder instances,
    though its current filtering logic needs review.
    """
    def get_queryset(self):
        # Note: This filter currently uses `StatusOptions='published'`.
        # `StatusOptions` is a tuple of choices for the `status` field, and 'published' is not among them.
        # This should likely filter on the `status` field, e.g., `self.model.status == 'confirmed'` (or another valid status).
        return super().get_queryset().filter(StatusOptions='published')

class ServiceOrder(models.Model):
    """
    Represents an order for a service within the platform.
    It captures details about the customer, employee (provider), service, price, and status of the order.
    """
    # TODO: Review if this ForeignKey to Thread model is needed.
    #thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    StatusOptions= ( # Defines the possible statuses for a service order.
        ('requested','Requested'),
        ('confirmed','Confirmed'),
        ('canceled','Canceled'),
        ('pend','Pend'), # Represents a pending status, awaiting further action.
        ('payed','Payed'), # Indicates the order has been paid.
    )
    ordered_at = models.DateTimeField(auto_now_add=True, verbose_name="ordered_at",null=True,blank=True) # Timestamp when the order was created.
    customerIdd = models.CharField(max_length=50) # Identifier for the customer who placed the order. # Note: Field name might have a typo, consider renaming to customerId.
    employedIdd = models.CharField(max_length=50) # Identifier for the employee/provider fulfilling the order. # Note: Field name might have a typo, consider renaming to employeeId.
    serviceId = models.IntegerField(null=True,blank=True) # Identifier for the specific service being ordered.
    price = models.IntegerField(null=True,blank=True) # The price of the service for this order.
    enhet = models.CharField(max_length=50) # Describes the unit for the service (e.g., hours, items). Consider renaming if 'enhet' is non-English or unclear.
    quantity = models.CharField(max_length=50) # The quantity of the service ordered (e.g., number of hours, number of items).
    date = models.CharField(max_length=500) # Likely the requested date or scheduled date for the service. Consider using DateField or DateTimeField for better type safety.
    status = models.CharField(max_length=10,choices=StatusOptions, # The current status of the service order.
        default="requested", verbose_name="Status of service:")
    objects = models.Manager()  # Default Django model manager.
    postobjects = PostObjects()  # Custom manager instance; its current filter logic needs review.
