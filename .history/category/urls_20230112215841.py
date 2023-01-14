from django.urls import path
from views import CategoryByNameViewSet

app_name = 'Category'

router = routers.DefaultRouter()
router.register('thread', ThreadViewSet)

urlpatterns = [
    path('<str:name>/', CategoryByNameViewSet.as_view(), name='Category_list_by_name'),
]