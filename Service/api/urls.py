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

app_name = 'Service'

urlpatterns = [
	path('Category/', CategoryViewSet.as_view(), name="Category"),
	path('SubCategory/', SubCategoryViewSet.as_view(), name="SubCategory"),
	path('Country/', CountryViewSet.as_view(), name="Country"),
	path('State/', StateViewSet.as_view(), name="State"),
	path('City/', CityViewSet.as_view(), name="City"),
	path('Likes/', LikesViewSet.as_view(), name="Likes"),
	path('LikeDisLike/', PostLikesAPIView.as_view(), name="Like"),

	path('DisLikes/', DisLikesViewSet.as_view(), name="DisLikes"),
	path('Comments/', CommentsViewSet.as_view(), name="Comments"),
	path('<slug>/', api_detail_service_view, name="detail"),
	path('<slug>/update', api_update_service_view, name="update"),
	path('<slug>/delete', api_delete_service_view, name="delete"),
	path('create', api_create_service_view, name="create"),
	path('list', ApiServiceListView.as_view(), name="list"),
	path('', servicesListAPIView.as_view(), name="filter"),
	path('<slug>/is_employee', api_is_employee_of_servicepost, name="is_employee"),
]