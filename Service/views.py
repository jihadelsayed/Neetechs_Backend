from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from Service.models import ServicePost
from Service.forms import CreateServicePostForm, UpdateServicePostForm

from knox_allauth.models import CustomUser


def create_service_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateServicePostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		employee = CustomUser.objects.filter(email=user.email).first()
		obj.employee = employee
		obj.save()
		form = CreateServicePostForm()

	context['form'] = form

	return render(request, "service/create_service.html", context)


def detail_service_view(request, slug):

	context = {}

	service_post = get_object_or_404(ServicePost, slug=slug)
	context['service_post'] = service_post

	return render(request, 'service/detail_service.html', context)


##### Add fiuld to edite service #######
def edit_service_view(request, slug):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	service_post = get_object_or_404(ServicePost, slug=slug)

	if service_post.employee != user:
		return HttpResponse("You are not the employee of that post.")

	if request.POST:
		form = UpdateServicePostForm(request.POST or None, request.FILES or None, instance=service_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			service_post = obj

	form = UpdateServicePostForm(
			initial = {
					"title": service_post.title,
					"pris": service_post.pris,
					"beskrivning": service_post.beskrivning,
					"status": service_post.status,
					"tillganligFran": service_post.tillganligFran,
					"tillganligTill": service_post.tillganligTill,
					"category": service_post.category,
					"underCategory": service_post.underCategory,
					"country": service_post.country,
					"state": service_post.state,
					"city": service_post.city,
					"image": service_post.image,
			}
		)

	context['form'] = form
	return render(request, 'service/edit_service.html', context)

#####################------------------_______unknowen_________--------------###############################
def get_service_queryset(query=None):
	queryset = []
	queries = query.split(" ") # python install 2019 = [python, install, 2019]
	for q in queries:
		posts = ServicePost.objects.filter(
				Q(title__icontains=q) | 
				Q(beskrivning__icontains=q)
			).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))	


