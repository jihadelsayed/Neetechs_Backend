from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,AllowAny
from knox.auth import TokenAuthentication

from Category.models import ModelCategory
from Category.serializers import CategorySerializer
from rest_framework.generics import ListAPIView

# Create your views here.
class CategoryByNameViewSet(ListAPIView):
    """
    API view to list categories, with an option to filter by a specific category name.
    The category name is expected to be passed as a URL keyword argument.

    Authentication: Uses TokenAuthentication.
    Permissions: IsAuthenticatedOrReadOnly (allows read access to anyone, write access to authenticated users).
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = ModelCategory.objects.all()
    def get_queryset(self):
        """
        Overrides the default queryset to filter categories by the 'name'
        URL keyword argument if it is provided. Otherwise, returns all categories.
        """
        name = self.kwargs.get('name', None)
        if name:
            return ModelCategory.objects.filter(name=name)
        return super().get_queryset()
    
class CategoryViewSet(ListAPIView):
	"""
	API view to list all categories.
	This view is publicly accessible for reading.

	Authentication: Uses TokenAuthentication.
	Permissions: AllowAny (anyone can access this endpoint for read operations).
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)
	serializer_class = CategorySerializer
	queryset = ModelCategory.objects.all()