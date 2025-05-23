"""URL patterns for the main views of the Service app, handling creation,
detail display, and editing of service posts using Django templates.
"""
from django.urls import path
from Service.views import(

	create_service_view,
	detail_service_view,
	edit_service_view,

)

app_name = 'Service' # Application namespace for these URLs.

urlpatterns = [
	# Route for creating a new service post via a form.
	path('create/', create_service_view, name="create"),
	# Route for displaying the details of a specific service post, identified by its slug.
	path('<slug>/', detail_service_view, name="detail"),
	# Route for editing an existing service post, identified by its slug.
	path('<slug>/edit', edit_service_view, name="edit"),
]