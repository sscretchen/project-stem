from django.urls import path
from .views import *
from .admin_views import *

urlpatterns = [
    path('', index, name="index"),
    # Authentication URLS
    path('login', ShowLoginPage, name="login"),
    path('login_user', login_user, name="login_user"),
    path('user_details', UserDetails, name="user_details"),
    path('logout_user', logout_user, name="logout_user"),
    # Admin URLs
    path('admin_home', admin_home, name="admin_home"),
    path('add_staff', add_staff, name="add_staff"),
    path('save_staff', save_staff, name="save_staff"),
]
