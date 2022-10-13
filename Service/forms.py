from django import forms

from Service.models import ServicePost


class CreateServicePostForm(forms.ModelForm):

	class Meta:
		model = ServicePost
		fields = ['title', 'pris', 'image', 'beskrivning', 'status', 'tillganligFran', 'tillganligTill', 'category', 'underCategory', 'country', 'state', 'city']



class UpdateServicePostForm(forms.ModelForm):

	class Meta:
		model = ServicePost
		fields = ['title', 'pris', 'image', 'beskrivning', 'status', 'tillganligFran', 'tillganligTill', 'category', 'underCategory', 'country', 'state', 'city']

	def save(self, commit=True):
		service_post = self.instance
		service_post.title = self.cleaned_data['title']
		service_post.beskrivning = self.cleaned_data['beskrivning']
		service_post.status = self.cleaned_data['status']
		service_post.tillganligFran = self.cleaned_data['tillganligFran']
		service_post.tillganligTill = self.cleaned_data['tillganligTill']
		service_post.category = self.cleaned_data['category']
		service_post.underCategory = self.cleaned_data['underCategory']
		service_post.country = self.cleaned_data['country']
		service_post.state = self.cleaned_data['state']
		service_post.city = self.cleaned_data['city']

		if self.cleaned_data['image']:
			service_post.image = self.cleaned_data['image']

		if commit:
			service_post.save()
		return service_post