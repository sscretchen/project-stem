from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('login', ShowLoginPage, name="login"),
    path('login_user', login_user, name="login_user"),
    path('user_details', UserDetails, name="user_details"),
    path('logout_user', logout_user, name="logout_user"),
]
