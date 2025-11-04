"""URL patterns for the Profile app with flattened, English-friendly paths."""
from django.urls import path

from .views import (
    CertificationCreateView,
    CertificationDetailView,
    CertificationListView,
    ExperienceCreateView,
    ExperienceDetailView,
    ExperienceListView,
    InterestCreateView,
    InterestDetailView,
    InterestListView,
    ProfileCollectionView,
    ProfileDetailView,
    ProfileListView,
    ProfileSummaryView,
    StudyCreateView,
    StudyDetailView,
    StudyListView,
)

app_name = "profile"

urlpatterns = [
    path("", ProfileListView.as_view(), name="list"),
    path("records/", ProfileCollectionView.as_view(), name="records"),
    path("<str:site_id>/", ProfileDetailView.as_view(), name="detail"),
    path("<str:site_id>/info/", ProfileSummaryView.as_view(), name="info"),
    path("experience/", ExperienceListView.as_view(), name="experience-list"),
    path("experience/create/", ExperienceCreateView.as_view(), name="experience-create"),
    path("experience/<int:id>/", ExperienceDetailView.as_view(), name="experience-detail"),
    path("studies/", StudyListView.as_view(), name="studies-list"),
    path("studies/create/", StudyCreateView.as_view(), name="studies-create"),
    path("studies/<int:id>/", StudyDetailView.as_view(), name="studies-detail"),
    path("interests/", InterestListView.as_view(), name="interests-list"),
    path("interests/create/", InterestCreateView.as_view(), name="interests-create"),
    path("interests/<int:id>/", InterestDetailView.as_view(), name="interests-detail"),
    path("certifications/", CertificationListView.as_view(), name="certifications-list"),
    path("certifications/create/", CertificationCreateView.as_view(), name="certifications-create"),
    path("certifications/<int:id>/", CertificationDetailView.as_view(), name="certifications-detail"),
]
