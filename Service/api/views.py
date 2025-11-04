"""
API views for managing services, categories, comments, likes/dislikes,
and related data for the Service application.
"""
#from Service.utils import rotate_image # Assuming not used as per cleanup instruction for api_create_service_view
from django.db.models.query_utils import Q
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, OpenApiTypes, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,views

#######authontication type
from knox.auth import TokenAuthentication
#from rest_framework.authentication import TokenAuthentication # Removed as per cleanup

from Service.models import ModelComments,ServicePost,ModelCategory,ModelSubCategory,ModelCountry,ModelState
from Service.api.serializers import (
    CitySerializer,
    CountrySerializer,
    DisLikesSerializer,
    LikesSerializer,
    ServiceCategorySerializer,
    ServicePostCreateSerializer,
    ServicePostSerializer,
    ServicePostUpdateSerializer,
    StateSerializer,
    SubCategorySerializer,
    CommentsSerializer,
)

from django.conf import settings

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Standardized response messages for API views.
SUCCESS = 'success' # General success indicator.
ERROR = 'error'     # General error indicator.
DELETE_SUCCESS = 'deleted' # Indicates successful deletion of a resource.
UPDATE_SUCCESS = 'updated' # Indicates successful update of a resource.
CREATE_SUCCESS = 'created' # Indicates successful creation of a resource.

class CategoryViewSet(ListAPIView):
	"""Lists all service categories (ModelCategory instances)."""
	authentication_classes = (TokenAuthentication,) # Specifies Knox token authentication.
	permission_classes = (IsAuthenticatedOrReadOnly,) # Allows unrestricted access to this view.
	serializer_class = ServiceCategorySerializer # Serializer for ModelCategory instances.
	queryset = ModelCategory.objects.all() # Retrieves all ModelCategory objects.
	
class SubCategoryViewSet(ListAPIView):
	"""Lists all service subcategories (ModelSubCategory instances), ordered by parent category."""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticatedOrReadOnly,)
	serializer_class = SubCategorySerializer # Serializer for ModelSubCategory instances.
	queryset = ModelSubCategory.objects.all().order_by('Category') # Retrieves all subcategories, ordered by their parent category.

class CountryViewSet(ListAPIView):
	"""Lists all countries (ModelCountry instances)."""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticatedOrReadOnly,)
	serializer_class = CountrySerializer # Serializer for ModelCountry instances.
	queryset = ModelCountry.objects.all() # Retrieves all ModelCountry objects.

class StateViewSet(ListAPIView):
	"""Lists all states/regions (ModelState instances)."""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticatedOrReadOnly,)
	serializer_class = StateSerializer # Serializer for ModelState instances.
	queryset = ModelState.objects.all() # Retrieves all ModelState objects.

class CityViewSet(ListAPIView):
	"""Lists distinct city names found in ServicePost instances."""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticatedOrReadOnly,)
	serializer_class = CitySerializer # Serializer for city data (likely a custom serializer for distinct values).
	queryset = ServicePost.objects.values('city').distinct() # Retrieves unique city values from ServicePost.


class LikesViewSet(ListAPIView):
	"""
	Lists likes for all ServicePost instances.
	NOTE: This view uses ServicePost as its queryset and LikesSerializer.
	This implies LikesSerializer is designed to work with ServicePost,
	likely to show users who liked a post or the count of likes.
	ModelLikes seems to have been removed or is not used here.
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticatedOrReadOnly,)
	serializer_class = LikesSerializer # Serializer for handling 'likes' field of ServicePost.
	queryset = ServicePost.objects.all() # Operates on all ServicePost instances.
	
class PostLikesAPIView(views.APIView):
	"""
	Handles toggling likes/dislikes on a ServicePost.
	This view allows an authenticated user to add or remove a like or dislike
	from a specific service post.
	"""
	# Expected request.data fields:
	# - userid (int): ID of the user performing the action.
	# - postNumber (int): ID of the ServicePost to like/dislike.
	# - likeType (str): "add one like", "remove one like", "add one dislike", "remove one dislike".
	# - LikeDisLike (int): 1 for like operations, 0 for dislike operations.
	@extend_schema(
		request=LikesSerializer,
		responses={200: OpenApiResponse(OpenApiTypes.OBJECT)},
	)
	def post(self, request):
		data= request.data
		serializer = LikesSerializer(data=data) # Uses LikesSerializer, likely for initial validation of 'userid' if it's part of that serializer.
		
		# Authorization check: Ensures the action is performed by the authenticated user.
		if serializer.is_valid() and int(request.user.id) == int(request.data['userid']):
			postNumber = int(data['postNumber']) # ID of the target ServicePost.
			likeType = data['likeType'] # Specific action to perform.
			LikeDisLike = int(data['LikeDisLike']) # Determines if it's a like (1) or dislike (0) operation.
			
			userid = int(data['userid'])
			try:
				service_post_instance = ServicePost.objects.get(id=postNumber)
			except ServicePost.DoesNotExist:
				return Response({"error": "ServicePost not found."}, status=status.HTTP_404_NOT_FOUND)

			# Logic for handling like operations
			if LikeDisLike == 1: # Like operations
				if likeType == "add one like":
					service_post_instance.likeType = "add one like" # Potentially for tracking last action type on the post.
					service_post_instance.save(update_fields=['likeType'])
					service_post_instance.likes.add(userid) # Add user to likes.
					service_post_instance.disLikes.remove(userid) # Remove user from dislikes if present.
					return Response({"Success": "You have added your like."},status=status.HTTP_201_CREATED)
				if likeType == "remove one like":
					service_post_instance.likeType = "remove one like"
					service_post_instance.save(update_fields=['likeType'])
					service_post_instance.likes.remove(userid) # Remove user from likes.
					return Response({"Success": "You have removed your like."},status=status.HTTP_200_OK)
			
			# Logic for handling dislike operations
			if LikeDisLike == 0: # Dislike operations
				if likeType == "add one dislike":
					service_post_instance.likeType = "add one dislike"
					service_post_instance.save(update_fields=['likeType'])
					service_post_instance.disLikes.add(userid) # Add user to dislikes.
					service_post_instance.likes.remove(userid) # Remove user from likes if present.
					return Response({"Success": "You have added your dislike."},status=status.HTTP_201_CREATED)
				if likeType == "remove one dislike":
					service_post_instance.likeType = "remove one dislike"
					service_post_instance.save(update_fields=['likeType'])
					service_post_instance.disLikes.remove(userid) # Remove user from dislikes.
					return Response({"Success": "You have removed your dislike."},status=status.HTTP_200_OK)
			
			# Fallback if likeType doesn't match expected values, though the conditions above should cover valid cases.
			# Consider returning a more specific error if likeType is invalid.
			return Response(serializer.data,status=status.HTTP_200_OK) # Or status based on actual operation.
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

	authentication_classes = (TokenAuthentication,)
	permission_classes = [IsAuthenticatedOrReadOnly] # Allows read (GET, HEAD, OPTIONS) by anyone, write by authenticated users.

class DisLikesViewSet(ListAPIView):
	"""
	Lists dislikes for all ServicePost instances.
	NOTE: Similar to LikesViewSet, this uses ServicePost as its queryset
	and DisLikesSerializer, implying DisLikesSerializer handles the 'disLikes' field.
	ModelDisLikes seems to have been removed or is not used here.
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticatedOrReadOnly,)
	serializer_class = DisLikesSerializer # Serializer for handling 'disLikes' field of ServicePost.
	queryset = ServicePost.objects.all() # Operates on all ServicePost instances.

class CommentsViewSet(ListAPIView):
	"""Lists all comments (ModelComments instances)."""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticatedOrReadOnly,)
	serializer_class = CommentsSerializer # Serializer for ModelComments instances.
	queryset = ModelComments.objects.all() # Retrieves all ModelComments objects.




@api_view(['GET','POST'])
@permission_classes((IsAuthenticated,))
def api_create_service_view(request):
	"""
	Handles the creation of a new ServicePost.

	Method: POST (also allows GET for form rendering, though not explicitly used in typical API scenarios).
	Permissions: IsAuthenticated.
	Request Data (POST): FormData containing fields for ServicePostCreateSerializer.
	                     `employee` field is automatically set to the authenticated user.
	                     `image` field is mandatory.
	Logic:
	    - If POST and form is valid:
	        - Saves the ServicePost instance.
	        - Manually constructs a dictionary `data` with selected fields from the saved instance.
	        - Returns this `data` dictionary.
	    - If POST and form is invalid, returns serializer errors.
	    - If GET (or POST fails before validation), returns an empty dictionary (no form in context for API).
	Response (POST Success):
	    - HTTP 201 CREATED with a manually constructed dictionary of the created service post.
	      # Note: Response data is manually constructed. This could be simplified by returning serializer.data directly if it matches the desired output.
	Response (POST Error):
	    - HTTP 400 BAD REQUEST with serializer errors or "no image" message.
	"""
	if request.method == 'POST':
		# Ensure 'image' is present, otherwise return an error.
		if request.data.get('image') is None: # Use .get for safer access
			return Response({"error": "No image provided."}, status=status.HTTP_400_BAD_REQUEST)
		
		# Ensure request.data is mutable for adding 'employee' if necessary, though serializer should handle this.
		if not hasattr(request.data, '_mutable') or not request.data._mutable:
			request.data = request.data.copy()
		
		request.data['employee'] = request.user.pk # Set the employee to the authenticated user.
		serializer = ServicePostCreateSerializer(data=request.data)
		
		if serializer.is_valid():
			service_post = serializer.save()
			# Manually construct response data.
			data = {
				'response': CREATE_SUCCESS,
				'pk': service_post.pk,
				'title': service_post.title,
				'createdAt': service_post.createdAt.strftime('%Y-%m-%d %I:%M %p') if service_post.createdAt else None, # Format datetime
				'updatedAt': service_post.updatedAt.strftime('%Y-%m-%d %I:%M %p') if service_post.updatedAt else None, # Format datetime
				'pris': service_post.pris,
				'bedomning': service_post.bedomning,
				'beskrivning': service_post.beskrivning,
				'status': service_post.status,
				'tillganligFran': service_post.tillganligFran.strftime('%Y-%m-%d %I:%M %p') if service_post.tillganligFran else None,
				'tillganligTill': service_post.tillganligTill.strftime('%Y-%m-%d %I:%M %p') if service_post.tillganligTill else None,
				'category': service_post.category,
				'underCategory': service_post.underCategory,
				'country': service_post.country,
				'state': service_post.state,
				'city': service_post.city,
				'slug': service_post.slug,
				# Consider adding image URLs if needed in response, similar to api_update_service_view.
			}
			return Response(data=data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	# For GET requests, typically an API might return a form or instructions,
	# but this view seems primarily for POST. Returning empty for GET.
	return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED) # Or handle GET appropriately


@api_view(['GET', ])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def api_detail_service_view(request, slug):
	"""
	Retrieves and returns the details of a specific ServicePost.

	Method: GET
	Path Parameter: slug (str) - The slug of the service post.
	Permissions: IsAuthenticatedOrReadOnly (anyone can view).
	Response:
	    - HTTP 200 OK with serialized ServicePost data.
	    - HTTP 404 NOT FOUND if the post does not exist.
	"""
	try:
		service_post = ServicePost.objects.get(slug=slug)
	except ServicePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	serializer = ServicePostSerializer(service_post)
	return Response(serializer.data)


@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_service_view(request, slug):
	"""
	Updates an existing ServicePost.

	Method: PUT (expects all required fields for update, or use PATCH for partial updates).
	Path Parameter: slug (str) - The slug of the service post to update.
	Permissions: IsAuthenticated (only the employee who created the post can update it).
	Request Data: FormData containing fields for ServicePostUpdateSerializer.
	Logic:
	    - Checks if the authenticated user is the owner of the post.
	    - If valid, updates the ServicePost instance.
	    - Manually constructs a dictionary for the response.
	Response:
	    - HTTP 200 OK with a manually constructed dictionary of the updated service post.
	      # Note: Response data is manually constructed. This could be simplified by returning serializer.data.
	    - HTTP 400 BAD REQUEST with serializer errors.
	    - HTTP 403 FORBIDDEN if the user is not the owner.
	    - HTTP 404 NOT FOUND if the post does not exist.
	"""
	try:
		service_post = ServicePost.objects.get(slug=slug)
	except ServicePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if service_post.employee != user: # Ownership check.
		return Response({'response':"You don't have permission to edit that."}, status=status.HTTP_403_FORBIDDEN) 
		
	if request.method == 'PUT':
		# Using partial=True makes this effectively a PATCH operation,
		# even though the method is PUT. For true PUT, partial=False.
		serializer = ServicePostUpdateSerializer(service_post, data=request.data, partial=True)
		if serializer.is_valid():
			updated_service_post = serializer.save()
			# Manually construct response data.
			data = {
				'response': UPDATE_SUCCESS,
				'pk': updated_service_post.pk,
				'title': updated_service_post.title,
				'createdAt': updated_service_post.createdAt.strftime('%Y-%m-%d %I:%M %p') if updated_service_post.createdAt else None,
				'updatedAt': updated_service_post.updatedAt.strftime('%Y-%m-%d %I:%M %p') if updated_service_post.updatedAt else None,
				'pris': updated_service_post.pris,
				'bedomning': updated_service_post.bedomning,
				'beskrivning': updated_service_post.beskrivning,
				'status': updated_service_post.status,
				'tillganligFran': updated_service_post.tillganligFran.strftime('%Y-%m-%d %I:%M %p') if updated_service_post.tillganligFran else None,
				'category': updated_service_post.category,
				'underCategory': updated_service_post.underCategory,
				'country': updated_service_post.country,
				'tillganligTill': updated_service_post.tillganligTill.strftime('%Y-%m-%d %I:%M %p') if updated_service_post.tillganligTill else None,
				'state': updated_service_post.state,
				'city': updated_service_post.city,
				'slug': updated_service_post.slug,
				'date_updated': updated_service_post.updatedAt.strftime('%Y-%m-%d %I:%M %p') if updated_service_post.updatedAt else None, # 'date_updated' seems redundant with 'updatedAt'.
				'image': request.build_absolute_uri(updated_service_post.image.url) if updated_service_post.image else None,
				'image2': request.build_absolute_uri(updated_service_post.image2.url) if updated_service_post.image2 else None,
				'image3': request.build_absolute_uri(updated_service_post.image3.url) if updated_service_post.image3 else None,
				'image4': request.build_absolute_uri(updated_service_post.image4.url) if updated_service_post.image4 else None,
				'image5': request.build_absolute_uri(updated_service_post.image5.url) if updated_service_post.image5 else None,
				'username': updated_service_post.employee.username,
			}
			# Clean image URLs by removing query parameters, if any.
			for img_key in ['image', 'image2', 'image3', 'image4', 'image5']:
				if data[img_key] and "?" in data[img_key]:
					data[img_key] = data[img_key][:data[img_key].rfind("?")]
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@extend_schema(
    request=None,
    responses={200: OpenApiResponse(OpenApiTypes.OBJECT)},
)
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_is_employee_of_servicepost(request, slug):
	"""
	Checks if the authenticated user is the employee (owner) of a specific ServicePost.
	This is an ownership check endpoint.

	Method: GET
	Path Parameter: slug (str) - The slug of the service post.
	Permissions: IsAuthenticated.
	Response:
	    - HTTP 200 OK with {'response': "You have permission to edit that."} if user is owner.
	    - HTTP 200 OK with {'response': "You don't have permission to edit that."} if user is not owner.
	      (Consider returning HTTP 403 FORBIDDEN for "don't have permission" case for consistency).
	    - HTTP 404 NOT FOUND if the post does not exist.
	"""
	try:
		service_post = ServicePost.objects.get(slug=slug)
	except ServicePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	data = {}
	user = request.user
	if service_post.employee == user: # Ownership check.
		data['response'] = "You have permission to edit that."
	else:
		data['response'] = "You don't have permission to edit that."
		# Consider returning Response(data, status=status.HTTP_403_FORBIDDEN) here.
	return Response(data=data)


@api_view(['DELETE',])
@permission_classes((IsAuthenticated, ))
def api_delete_service_view(request, slug):
	"""
	Deletes a specific ServicePost.

	Method: DELETE
	Path Parameter: slug (str) - The slug of the service post to delete.
	Permissions: IsAuthenticated (only the employee who created the post can delete it).
	Response:
	    - HTTP 200 OK with {'response': DELETE_SUCCESS} if successful.
	    - HTTP 403 FORBIDDEN if the user is not the owner.
	    - HTTP 404 NOT FOUND if the post does not exist.
	    - HTTP 500 INTERNAL SERVER ERROR if deletion operation fails.
	"""
	try:
		service_post = ServicePost.objects.get(slug=slug)
	except ServicePost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if service_post.employee != user: # Ownership check.
		return Response({'response':"You don't have permission to delete that."}, status=status.HTTP_403_FORBIDDEN) 

	if request.method == 'DELETE':
		operation = service_post.delete()
		data = {}
		if operation: # Check if deletion was successful (operation returns number of objects deleted).
			data['response'] = DELETE_SUCCESS
			return Response(data=data, status=status.HTTP_200_OK)
		else:
			# This case might indicate an issue with the delete operation itself.
			data['response'] = ERROR 
			return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ApiServiceListView(ListAPIView):
	"""
	Lists ServicePost instances that are either not expired or belong to users
	with specific premium subscription types ('premiumplanMonthly', 'PremiumPlanYearly').
	Supports pagination, searching, and ordering.

	Authentication: TokenAuthentication
	Permissions: IsAuthenticatedOrReadOnly (public read access, authenticated writes if added later)
	Pagination: PageNumberPagination
	Filtering: SearchFilter (on title, beskrivning, slug, employee__username), OrderingFilter.
	"""
	# Queryset filters services that are active (not expired) OR posted by premium users.
	queryset = ServicePost.objects.filter(Q(expiration_date__gte=timezone.now()) | Q(employee__subscription_type="premiumplanMonthly") | Q(employee__subscription_type="PremiumPlanYearly"))
	serializer_class = ServicePostSerializer # Serializer for ServicePost instances.
	authentication_classes = (TokenAuthentication,) # Uses Knox token authentication.
	permission_classes = (IsAuthenticatedOrReadOnly,) # Allows unrestricted access.
	pagination_class = PageNumberPagination # Enables pagination for the list.
	filter_backends = (SearchFilter, OrderingFilter) # Enables search and ordering.
	search_fields = ('title', 'beskrivning', 'slug','employee__username') # Fields available for searching.
	# ordering_fields should be specified for OrderingFilter, e.g., ordering_fields = ['updatedAt', 'title']

class servicesListAPIView(ListAPIView):
    """
    Lists ServicePost instances with extensive filtering capabilities.
    Similar to ApiServiceListView, it filters by expiration date or employee subscription type.
    Provides more detailed field-level filtering via DjangoFilterBackend.

    Authentication: TokenAuthentication
    Permissions: IsAuthenticatedOrReadOnly (public read access, authenticated writes if added later)
    Filtering: DjangoFilterBackend (on many fields), SearchFilter, OrderingFilter.
    """
    queryset = ServicePost.objects.filter(Q(expiration_date__gte=timezone.now()) | Q(employee__subscription_type="premiumplanMonthly") | Q(employee__subscription_type="PremiumPlanYearly"))
    serializer_class = ServicePostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    OrderingFilter = ('title')
    filterset_fields = ['title', 'site_id', 'beskrivning','slug', 'city','state','country','underCategory','category','status','beskrivning','bedomning','updatedAt','pris','tillganligFran','tillganligTill']
    # Fields available for searching via SearchFilter.
    search_fields = ['title', 'site_id', 'beskrivning','slug', 'city','state','country','underCategory','category','beskrivning',]

# Removed commented-out lines related to '#from Service.utils import rotate_image' and '#from rest_framework.authentication import TokenAuthentication'
# Removed commented-out '#	queryset = ModelLikes.objects.all()'
# Removed commented-out Stripe and image rotation logic from api_create_service_view
# Removed print statements from api_create_service_view
