from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members, name= "members" ),
    path('members/add/', views.add_member, name= "add-member" ),
    path('profile/<str:type>/<str:id>/', views.profile, name= "profile" ),
    path('profile_edit/<str:type>/<str:id>/', views.profile_edit, name= "profile-edit" ),
    path("delete_user/<str:id>/", views.delete_user, name="delete-user")
]

