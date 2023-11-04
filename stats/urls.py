from django.urls import path
from .views import (home,TeamListView,TeamDetailView,about_page,contact_page)

urlpatterns = [
    path("", TeamListView.as_view(), name="home"),
    path(
        "<int:pk>/", TeamDetailView.as_view(),
        name="team-details"
    ),
    path("about/", about_page, name="about"),
    path("contact/", contact_page, name="contact")
]