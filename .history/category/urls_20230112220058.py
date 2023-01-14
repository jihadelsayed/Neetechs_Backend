from django.urls import path
from views import CategoryByNameViewSet

app_name = 'Category'


urlpatterns = [
    path('<str:name>/', CategoryByNameViewSet.as_view(), name='Category_list_by_name'),
]