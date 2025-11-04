from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from Service.models import ServicePost
from knox_allauth.models import CustomUser
from .models import ServiceOrder

from django.conf import settings


class ServiceOrderSerializer(serializers.ModelSerializer):
	"""
	Serializes ServiceOrder instances, enriching the output with related
	service name, employee name, and customer name via SerializerMethodFields.
	"""
	servicename = serializers.SerializerMethodField()
	employedname = serializers.SerializerMethodField()
	customername = serializers.SerializerMethodField()
	# Explicitly defines the format and optionality for the 'ordered_at' field.
	# This ensures consistent datetime representation and allows the field to be absent during partial updates or creation.
	ordered_at = serializers.DateTimeField(required=False, allow_null=True,format='%Y-%m-%d %I:%M %p')

	class Meta:
		model = ServiceOrder
		# Specifies the fields to be included in the serialized representation.
		# This includes standard model fields and the custom method fields defined above.
		fields = ['quantity','pk','status','serviceId','employedIdd','ordered_at','customerIdd','servicename','employedname','customername','price','enhet','date']

	@extend_schema_field(serializers.CharField())
	def get_servicename(self, obj):
		"""Retrieves the title of the ordered service."""
		# Consider renaming Servicenam to service_name for Python naming conventions.
		Servicenam = ServicePost.objects.get(pk=obj.serviceId).title
		return Servicenam

	@extend_schema_field(serializers.CharField())
	def get_employedname(self, obj):
		"""Retrieves the first name of the employee/provider associated with the order."""
		# Consider renaming Employednam to employee_name.
		Employednam = CustomUser.objects.get(site_id=obj.employedIdd).first_name
		return Employednam

	@extend_schema_field(serializers.CharField())
	def get_customername(self, obj):
		"""Retrieves the first name of the customer who placed the order."""
		# Consider renaming Customernam to customer_name.
		Customernam = CustomUser.objects.get(site_id=obj.customerIdd).first_name
		return Customernam


# TODO: This serializer is commented out. Review its purpose and either implement/use it or remove it.
#class OrderSerializer(serializers.ModelSerializer):

#	class Meta:
#		model = ServiceOrder
#		fields = ['pk','status','serviceId','employedId','ordered_at','customerId','price','enhet','enhet']

