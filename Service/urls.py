from django.urls import path
from Service.views import(

	create_service_view,
	detail_service_view,
	edit_service_view,

)

app_name = 'Service'

urlpatterns = [
	path('create/', create_service_view, name="create"),
	path('<slug>/', detail_service_view, name="detail"),
	path('<slug>/edit', edit_service_view, name="edit"),
]