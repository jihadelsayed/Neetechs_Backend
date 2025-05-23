#from Service.utils import rotate_image
from django.db.models.query_utils import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,views

#######authontication type
from knox.auth import TokenAuthentication
#from rest_framework.authentication import TokenAuthentication

from Service.models import ModelComments,ServicePost,ModelCategory,ModelSubCategory,ModelCountry,ModelState
from Service.api.serializers import LikesSerializer,DisLikesSerializer, CommentsSerializer,ServicePostSerializer, ServicePostUpdateSerializer, ServicePostCreateSerializer,CategorySerializer,SubCategorySerializer,CountrySerializer,StateSerializer,CitySerializer

from django.conf import settings

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

class CategoryViewSet(ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)
	serializer_class = CategorySerializer
	queryset = ModelCategory.objects.all()
	
class SubCategoryViewSet(ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)
	serializer_class = SubCategorySerializer
	queryset = ModelSubCategory.objects.all().order_by('Category')

class CountryViewSet(ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)
	serializer_class = CountrySerializer
	queryset = ModelCountry.objects.all()

class StateViewSet(ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)
	serializer_class = StateSerializer
	queryset = ModelState.objects.all()

class CityViewSet(ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)
	serializer_class = CitySerializer
	queryset = ServicePost.objects.values('city').distinct()


class LikesViewSet(ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)
	serializer_class = LikesSerializer
#	queryset = ModelLikes.objects.all()
	queryset = ServicePost.objects.all()
	
class PostLikesAPIView(views.APIView):
	def post(self, request):
		data= request.data
		serializer = LikesSerializer(data=data)
		if serializer.is_valid() and int(request.user.id) == int(request.data['userid']):
			postNumber = int(data['postNumber'])
			likeType = data['likeType']
			LikeDisLike = int(data['LikeDisLike'])
			#ModelLikes.objects.get_or_create(postNumber_id=postNumber)
			#ModelDisLikes.objects.get_or_create(postNumber_id=postNumber)
			userid = int(data['userid'])
			#postLikes = ModelLikes.objects.get(postNumber_id=postNumber)
			postLikes = ServicePost.objects.get(id=postNumber)
			postDisLikes = ServicePost.objects.get(id=postNumber)
			ServicePos = ServicePost.objects.get(id=postNumber)
			if LikeDisLike == 1:
				if likeType == "add one like":
					ServicePos.likeType = "add one like"
					ServicePos.save()
					postLikes.likes.add(userid)
					postDisLikes.disLikes.remove(userid)
					return Response({"Success": "you have add your like"},status=201)
				if likeType == "remove one like":
					ServicePos.likeType = "remove one like"
					postLikes.likes.remove(userid)
					return Response({"Success": "you have remove your like"},status=201)
			if LikeDisLike == 0:
				if likeType == "add one dislike":
					ServicePos.likeType = "add one dislike"
					postDisLikes.disLikes.add(userid)
					postLikes.likes.remove(userid)
					return Response({"Success": "you have add your dislike"},status=201)
				if likeType == "remove one dislike":
					ServicePos.likeType = "remove one dislike"
					postDisLikes.disLikes.remove(userid)
					return Response({"Success": "you have remove your dislike"},status=201)
			#serializer.save()
			
			return Response(serializer.data,status=201)
		return Response(serializer.errors,status=400)
	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticatedOrReadOnly]

class DisLikesViewSet(ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)
	serializer_class = DisLikesSerializer
	queryset = ServicePost.objects.all()

class CommentsViewSet(ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)
	serializer_class = CommentsSerializer
	queryset = ModelComments.objects.all()




@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
def api_create_service_view(request):

	if request.method == 'POST':
		#data['stripeId'] = request.user.pk
	#	data['expiration_date'] = timezone.now() + 2592000
	#	product = stripe.Product.create(
     #       name=data['title'],
           # id=data['pk'],
      #  )
	#	price = stripe.Price.create(
     #       product=product.id,
     #       unit_amount=data['pris'],
     #       currency='sek',
      #  )
	#	data['stripeId'] = product.id
		"""

		if 'image' in data:
			data['image'] = rotate_image(data['image'])
		if 'image2' in data:
			data['image2'] = rotate_image(data['image2'])
		if 'image3' in data:
			data['image3'] = rotate_image(data['image3'])
			
		if 'image4' in data:
			data['image4'] = rotate_image(data['image4'])
		if 'image5' in data:
			data['image5'] = rotate_image(data['image5'])
		"""
		if request.data['image'] is None:
			return Response("no image", status=status.HTTP_400_BAD_REQUEST)
		request.data['employee'] = request.user.pk
		serializer = ServicePostCreateSerializer(data=request.data)
		print(serializer.is_valid)
		data = {}
		if serializer.is_valid():
			"""
			checkout_session = stripe.checkout.Session.create(
                mode='payment',
                success_url= 'https://www.neetechs.com/CheckoutSuccess',
                cancel_url= 'https://www.neetechs.com/CheckoutUnsuccess',
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'sek',
                            'unit_amount': data['pris'],
                            'product_data': {
                                'id': "prod_JdSsKlpWeoTwLD",
                               # 'id': data['stripeId'],
                               # 'images': data['image'],
                            },
                        },
                        'quantity': 1,
                    },
                ],

            )"""
			service_post = serializer.save()
			data['response'] = CREATE_SUCCESS
			data['pk'] = service_post.pk
			data['title'] = service_post.title
			data['createdAt'] = service_post.createdAt
			data['updatedAt'] = service_post.updatedAt
			data['pris'] = service_post.pris
			data['bedomning'] = service_post.bedomning
			data['beskrivning'] = service_post.beskrivning
			data['status'] = service_post.status
			data['tillganligFran'] = service_post.tillganligFran
			data['tillganligTill'] = service_post.tillganligTill
			data['category'] = service_post.category
			data['underCategory'] = service_post.underCategory
			data['country'] = service_post.country
			data['state'] = service_post.state
			data['city'] = service_post.city

			data['slug'] = service_post.slug
			#data['buy'] = checkout_session.id
		#	image_url = str(request.build_absolute_uri(service_post.image.url))
		#	if "?" in image_url:
		#		image_url = image_url[:image_url.rfind("?")]
		#	data['image'] = image_url
		#	data['image2'] = image_url
		#	data['image3'] = image_url
		#	data['image4'] = image_url
		#	data['image5'] = image_url
		#	data['username'] = service_post.employee.username
		#	data['stripeId'] = service_post.stripeId
			#serializer.validated_data

			return Response(data=data, status=status.HTTP_201_CREATED)
		print(serializer.errors)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Response: https://gist.github.com/mitchtabian/93f287bd1370e7a1ad3c9588b0b22e3d
# Url: https://<your-domain>/api/service/<slug>/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_detail_service_view(request, slug):

	try:
		service_post = ServicePost.objects.get(slug=slug)
	except ServicePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	serializer = ServicePostSerializer(service_post)
	return Response(serializer.data)


# Response: https://gist.github.com/mitchtabian/32507e93c530aa5949bc08d795ba66df
# Url: https://<your-domain>/api/service/<slug>/update
# Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_service_view(request, slug):

	try:
		service_post = ServicePost.objects.get(slug=slug)
	except ServicePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if service_post.employee != user:
		return Response({'response':"You don't have permission to edit that."}) 
		
	if request.method == 'PUT':
		serializer = ServicePostUpdateSerializer(service_post, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = UPDATE_SUCCESS
			data['pk'] = service_post.pk
			data['title'] = service_post.title
			data['createdAt'] = service_post.createdAt
			data['updatedAt'] = service_post.updatedAt
			data['pris'] = service_post.pris
			data['bedomning'] = service_post.bedomning
			data['beskrivning'] = service_post.beskrivning
			data['status'] = service_post.status
			data['tillganligFran'] = service_post.tillganligFran
			data['category'] = service_post.category
			data['underCategory'] = service_post.underCategory
			data['country'] = service_post.country
			data['tillganligTill'] = service_post.tillganligTill
			data['state'] = service_post.state
			data['city'] = service_post.city
			data['slug'] = service_post.slug
			data['date_updated'] = service_post.date_updated
			image_url = str(request.build_absolute_uri(service_post.image.url))
			if "?" in image_url:
				image_url = image_url[:image_url.rfind("?")]
			data['image'] = image_url
			data['image2'] = image_url
			data['image3'] = image_url
			data['image4'] = image_url
			data['image5'] = image_url
			data['username'] = service_post.employee.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_is_employee_of_servicepost(request, slug):
	try:
		service_post = ServicePost.objects.get(slug=slug)
	except ServicePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	data = {}
	user = request.user
	if service_post.employee != user:
		data['response'] = "You don't have permission to edit that."
		return Response(data=data)
	data['response'] = "You have permission to edit that."
	return Response(data=data)


# Response: https://gist.github.com/mitchtabian/a97be3f8b71c75d588e23b414898ae5c
# Url: https://<your-domain>/api/service/<slug>/delete
# Headers: Authorization: Token <token>
@api_view(['DELETE',])
@permission_classes((IsAuthenticated, ))
def api_delete_service_view(request, slug):

	try:
		service_post = ServicePost.objects.get(slug=slug)
	except ServicePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if service_post.employee != user:
		return Response({'response':"You don't have permission to delete that."}) 

	if request.method == 'DELETE':
		operation = service_post.delete()
		data = {}
		if operation:
			data['response'] = DELETE_SUCCESS
		return Response(data=data)



# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: 
#		1) list: https://<your-domain>/api/service/list
#		2) pagination: http://<your-domain>/api/service/list?page=2
#		3) search: http://<your-domain>/api/service/list?search=mitch
#		4) ordering: http://<your-domain>/api/service/list?ordering=-date_updated
#		4) search + pagination + ordering: <your-domain>/api/service/list?search=mitch&page=2&ordering=-date_updated
# Headers: Authorization: Token <token>
class ApiServiceListView(ListAPIView):
	queryset = ServicePost.objects.filter(Q(expiration_date__gte=timezone.now()) | Q(employee__subscription_type="premiumplanMonthly") | Q(employee__subscription_type="PremiumPlanYearly"))
	serializer_class = ServicePostSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('title', 'beskrivning', 'slug','employee__username')

class servicesListAPIView(ListAPIView):
    queryset = ServicePost.objects.filter(Q(expiration_date__gte=timezone.now()) | Q(employee__subscription_type="premiumplanMonthly") | Q(employee__subscription_type="PremiumPlanYearly"))
    serializer_class = ServicePostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [AllowAny]
    #permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    OrderingFilter = ('title')
    filterset_fields = ['title', 'site_id', 'beskrivning','slug', 'city','state','country','underCategory','category','status','beskrivning','bedomning','updatedAt','pris','tillganligFran','tillganligTill']
    search_fields = ['title', 'site_id', 'beskrivning','slug', 'city','state','country','underCategory','category','beskrivning',]

