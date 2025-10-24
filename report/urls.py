from django.urls import path

from .views import ReportAPIView,ListReportAPIView


urlpatterns = [
    path('post', ReportAPIView.as_view()),
    path('list', ListReportAPIView.as_view()),
    

]