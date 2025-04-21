from django.urls import path
from . import views


urlpatterns = [
    
    path("donations/", views.member_donations, name="donations"),
    path("donate/", views.donate, name="donate"),
    path("prayers/", views.prayer_requests, name="prayers"),
    path("events/<str:type>/", views.events, name="events"),
    path("announcements/", views.announcements, name="announcements"),
    path("posts/<str:type>/", views.posts, name="posts"),
]
