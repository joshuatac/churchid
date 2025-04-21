from django.urls import path
from . import views


urlpatterns = [
    path("register/<str:option>/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("success/", views.success, name="success"),
    
    
    path("account/activation/<str:id>/", views.account_activation, name="account-activation"),
]
