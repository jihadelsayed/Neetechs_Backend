from django.urls import path

from .views import ReportAPIView,ListReportAPIView


urlpatterns = [
    path('api/report/post', ReportAPIView.as_view()),
    path('api/report/list', ListReportAPIView.as_view()),
    

]