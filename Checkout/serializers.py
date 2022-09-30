from rest_framework import serializers
from Service.models import ServicePost
from knox_allauth.models import CustomUser
from .models import ServiceOrder

from django.conf import settings



class ServiceOrderSerializer(serializers.ModelSerializer):
	servicename = serializers.SerializerMethodField()
	employedname = serializers.SerializerMethodField()
	customername = serializers.SerializerMethodField()
	ordered_at = serializers.DateTimeField(required=False, allow_null=True,format='%Y-%m-%d %I:%M %p')

	class Meta:
		model = ServiceOrder
		fields = ['quantity','pk','status','serviceId','employedIdd','ordered_at','customerIdd','servicename','employedname','customername','price','enhet','date']

	def get_servicename(self, obj):
		Servicenam = ServicePost.objects.get(pk=obj.serviceId).title #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
		#print(Servicenam)
		return Servicenam

	def get_employedname(self, obj):
		Employednam = CustomUser.objects.get(site_id=obj.employedIdd).first_name #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
		#print(Employednam)
		return Employednam

	def get_customername(self, obj):
		Customernam = CustomUser.objects.get(site_id=obj.customerIdd).first_name #.last().created_at.strftime("%Y-%m-%d %I:%M %p")
		#print(Customernam)
		return Customernam #SubCategorySerializer(SubCategorys, many=True).data



#class OrderSerializer(serializers.ModelSerializer):

#	class Meta:
#		model = ServiceOrder
#		fields = ['pk','status','serviceId','employedId','ordered_at','customerId','price','enhet','enhet']


