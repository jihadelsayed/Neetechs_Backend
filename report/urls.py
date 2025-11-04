"""Report API URLs versioned under /api/v1/report/."""
from django.urls import path

from .views import ListReportAPIView, ReportAPIView

app_name = "report"

urlpatterns = [
    path("post/", ReportAPIView.as_view(), name="post"),
    path("list/", ListReportAPIView.as_view(), name="list"),
]
