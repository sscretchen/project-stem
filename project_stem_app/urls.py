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
    path('edit_staff/<str:staff_id>', edit_staff, name="edit_staff"),
    path('save_staff_edits', save_staff_edits, name="save_staff_edits"),
    path('add_student', add_student, name="add_student"),
    path('save_student', save_student, name="save_student"),
    path('edit_student/<str:student_id>', edit_student, name="edit_student"),
    path('save_student_edits', save_student_edits, name="save_student_edits"),
    path('add_course', add_course, name="add_course"),
    path('save_course', save_course, name="save_course"),
    path('add_subject', add_subject, name="add_subject"),
    path('save_subject', save_subject, name="save_subject"),
    path('manage_staff', manage_staff, name="manage_staff"),
    path('manage_students', manage_students, name="manage_students"),
    path('manage_courses', manage_courses, name="manage_courses"),
    path('manage_subjects', manage_subjects, name="manage_subjects"),
    # Custom page URLs
]
