"""Django ModelForms for creating and updating ServicePost instances."""
from django import forms

from Service.models import ServicePost


class CreateServicePostForm(forms.ModelForm):
	"""A form for creating new `ServicePost` objects."""

	class Meta:
		# Configures the form to use the ServicePost model and specifies the fields to include.
		model = ServicePost
		fields = ['title', 'pris', 'image', 'beskrivning', 'status', 'tillganligFran', 'tillganligTill', 'category', 'underCategory', 'country', 'state', 'city'] # Note: Some field names like 'pris', 'beskrivning' are based on the model's Swedish field names.



class UpdateServicePostForm(forms.ModelForm):
	"""A form for updating existing `ServicePost` objects."""

	class Meta:
		# Configures the form to use the ServicePost model and specifies the fields to include for updates.
		model = ServicePost
		fields = ['title', 'pris', 'image', 'beskrivning', 'status', 'tillganligFran', 'tillganligTill', 'category', 'underCategory', 'country', 'state', 'city']

	def save(self, commit=True):
		"""Custom save method to update the ServicePost instance."""
		# NOTE: This custom save method manually reassigns all fields from cleaned_data.
		# Much of this is redundant with the default ModelForm.save() behavior.
		# Consider simplifying this by calling super().save(commit=False) first,
		# then making specific modifications if needed, or removing this method
		# entirely if no special save logic beyond updating model fields is required.
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

		if self.cleaned_data['image']: # Only update image if a new one was provided.
			service_post.image = self.cleaned_data['image']

		if commit:
			service_post.save()
		return service_post