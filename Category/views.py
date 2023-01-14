from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,AllowAny
from knox.auth import TokenAuthentication

from Category.models import ModelCategory
from Category.serializers import CategorySerializer
from rest_framework.generics import ListAPIView

# Create your views here.
class CategoryByNameViewSet(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = ModelCategory.objects.all()
    def get_queryset(self):
        name = self.kwargs.get('name', None)
        if name:
            return ModelCategory.objects.filter(name=name)
        return super().get_queryset()
    
class CategoryViewSet(ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)
	serializer_class = CategorySerializer
	queryset = ModelCategory.objects.all()