"""API URL patterns for the Service app.

Defines routes for service posts, categories, locations, likes, comments, etc.,
via DRF views.
"""
from django.urls import path
from Service.api.views import(
	api_detail_service_view,
	api_update_service_view,
	api_delete_service_view,
	api_create_service_view,
	api_is_employee_of_servicepost,
	ApiServiceListView,
	servicesListAPIView,
	CategoryViewSet,
	SubCategoryViewSet,
	CountryViewSet,
	StateViewSet,
	LikesViewSet,
	PostLikesAPIView,
	DisLikesViewSet,
	CommentsViewSet,
	CityViewSet
)

app_name = 'Service' # Application namespace for these API URLs. # Note: This is the same as in Service/urls.py; ensure they are included under different project-level namespaces if both are used.

urlpatterns = [
	# Lists all service categories via API.
	path('Category/', CategoryViewSet.as_view(), name="Category"),
	# Lists all service subcategories via API.
	path('SubCategory/', SubCategoryViewSet.as_view(), name="SubCategory"),
	# Lists all countries via API.
	path('Country/', CountryViewSet.as_view(), name="Country"),
	# Lists all states/regions via API.
	path('State/', StateViewSet.as_view(), name="State"),
	# Lists distinct city names from service posts via API.
	path('City/', CityViewSet.as_view(), name="City"),
	# Lists likes for all service posts via API.
	path('Likes/', LikesViewSet.as_view(), name="Likes"),
	# Handles liking or disliking a service post via API.
	path('LikeDisLike/', PostLikesAPIView.as_view(), name="Like"),

	# Lists dislikes for all service posts via API.
	path('DisLikes/', DisLikesViewSet.as_view(), name="DisLikes"),
	# Lists all comments for service posts via API.
	path('Comments/', CommentsViewSet.as_view(), name="Comments"),
	# Retrieves details of a specific service post by slug via API.
	path('<slug>/', api_detail_service_view, name="detail"),
	# Updates a specific service post by slug via API.
	path('<slug>/update', api_update_service_view, name="update"),
	# Deletes a specific service post by slug via API.
	path('<slug>/delete', api_delete_service_view, name="delete"),
	# Creates a new service post via API.
	path('create', api_create_service_view, name="create"),
	# Lists service posts, often with specific filtering (e.g., active/premium) via API.
	path('list', ApiServiceListView.as_view(), name="list"),
	# General listing/filtering endpoint for service posts via API.
	path('', servicesListAPIView.as_view(), name="filter"),
	# Checks if the authenticated user is the employee (owner) of a service post by slug via API.
	path('<slug>/is_employee', api_is_employee_of_servicepost, name="is_employee"),
]