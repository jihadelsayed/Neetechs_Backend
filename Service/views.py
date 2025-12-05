from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from Service.models import ServicePost
"""
Contains Django views for creating, displaying, and editing service posts,
as well as search functionality. These views typically render HTML templates.
"""
from Service.forms import CreateServicePostForm, UpdateServicePostForm

from accounts.models import User


def create_service_view(request):
	"""
	Handles the creation of a new ServicePost instance via a form.

	If the user is not authenticated, they are redirected to a 'must_authenticate' URL.
	On a POST request with valid form data, a new ServicePost is created,
	with the `employee` field set to the currently authenticated user.
	A new, empty form is then prepared for the context.

	Args:
		request: The HttpRequest object.

	Context:
		form (CreateServicePostForm): The form instance for creating a service post.

	Returns:
		HttpResponse: Renders the 'service/create_service.html' template with the context.
	"""
	context = {}
	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateServicePostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		# Associate the post with the currently authenticated user.
		employee = User.objects.filter(email=user.email).first()
		obj.employee = employee
		obj.save()
		form = CreateServicePostForm() # Reset form after successful save.

	context['form'] = form
	return render(request, "service/create_service.html", context)


def detail_service_view(request, slug):
	"""
	Displays the details for a single ServicePost identified by its slug.

	Retrieves a ServicePost instance using the provided slug or returns a 404 error
	if no such post exists.

	Args:
		request: The HttpRequest object.
		slug (str): The slug of the ServicePost to display.

	Context:
		service_post (ServicePost): The retrieved service post instance.

	Returns:
		HttpResponse: Renders the 'service/detail_service.html' template with the context.
	"""
	context = {}
	service_post = get_object_or_404(ServicePost, slug=slug)
	context['service_post'] = service_post
	return render(request, 'service/detail_service.html', context)


def edit_service_view(request, slug):
	"""
	Allows an authenticated user to edit their own ServicePost.

	Checks for user authentication and ownership of the post. If checks fail,
	it redirects or returns an error response.
	Handles GET requests by populating the form with the existing post's data.
	Handles POST requests by processing the submitted form for updates.
	A success message is added to the context upon successful update.

	Args:
		request: The HttpRequest object.
		slug (str): The slug of the ServicePost to be edited.

	Context:
		form (UpdateServicePostForm): The form instance for editing the service post.
		success_message (str, optional): A message indicating successful update.

	Returns:
		HttpResponse: Renders the 'service/edit_service.html' template with the context,
		              or redirects/returns an error if checks fail.
	"""
	context = {}
	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	service_post = get_object_or_404(ServicePost, slug=slug)

	# Ownership check
	if service_post.employee != user:
		return HttpResponse("You are not the employee of that post.")

	if request.POST:
		form = UpdateServicePostForm(request.POST or None, request.FILES or None, instance=service_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			service_post = obj # Update service_post to reflect changes in the form initialization below.
	
	# Populate form with initial data for GET request or after POST if form was invalid (to show errors) or successful (to show updated data).
	form = UpdateServicePostForm(
			initial = {
					"title": service_post.title,
					"pris": service_post.pris,
					"beskrivning": service_post.beskrivning, # Field 'beskrivning' (Swedish: description)
					"status": service_post.status,
					"tillganligFran": service_post.tillganligFran, # Field 'tillganligFran' (Swedish: availableFrom)
					"tillganligTill": service_post.tillganligTill, # Field 'tillganligTill' (Swedish: availableTo)
					"category": service_post.category,
					"underCategory": service_post.underCategory, # Field 'underCategory' (Swedish: subCategory)
					"country": service_post.country,
					"state": service_post.state,
					"city": service_post.city,
					"image": service_post.image,
			}
		)

	context['form'] = form
	return render(request, 'service/edit_service.html', context)


def get_service_queryset(query=None):
	"""
	Performs a search for ServicePost objects based on a query string.

	The query string is split into words, and a Q object is constructed
	to search for matches (case-insensitive) in the 'title' or 'beskrivning'
	(description) fields of the ServicePost model for each word.
	The results are a list of unique ServicePost objects that match any of the query words.

	Args:
		query (str, optional): The search query string. Defaults to None.

	Returns:
		list: A list of unique ServicePost instances matching the query.
		      Returns an empty list if the query is None or empty.
	"""
	queryset = []
	if query: # Ensure query is not None or empty before splitting
		queries = query.split(" ") # Example: "python install 2019" -> ["python", "install", "2019"]
		for q in queries:
			posts = ServicePost.objects.filter(
					Q(title__icontains=q) | 
					Q(beskrivning__icontains=q) # 'beskrivning' is Swedish for description
				).distinct()

			for post in posts:
				queryset.append(post)
	# Return a list of unique posts by converting to a set and back to a list.
	return list(set(queryset))	


