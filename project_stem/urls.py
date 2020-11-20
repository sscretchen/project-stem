"""project_stem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from project_stem import settings
from project_stem_app import views, admin_views, staff_views, student_views

urlpatterns = [
    # path('', include('project_stem_app.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # Authentication URLS
    path('', views.ShowLoginPage, name="show_login"),
    path('login_user', views.login_user, name="login_user"),
    path('user_details', views.UserDetails, name="user_details"),
    path('logout_user', views.logout_user, name="logout_user"),

    # Admin URLs
    path('admin_home', admin_views.admin_home, name="admin_home"),
    path('add_staff', admin_views.add_staff, name="add_staff"),
    path('save_staff', admin_views.save_staff, name="save_staff"),
    path('edit_staff/<str:staff_id>', admin_views.edit_staff, name="edit_staff"),
    path('save_staff_edits', admin_views.save_staff_edits, name="save_staff_edits"),
    path('add_student', admin_views.add_student, name="add_student"),
    path('save_student', admin_views.save_student, name="save_student"),
    path('edit_student/<str:student_id>', admin_views.edit_student, name="edit_student"),
    path('save_student_edits', admin_views.save_student_edits, name="save_student_edits"),
    path('add_course', admin_views.add_course, name="add_course"),
    path('save_course', admin_views.save_course, name="save_course"),
    path('manage_staff', admin_views.manage_staff, name="manage_staff"),
    path('manage_students', admin_views.manage_students, name="manage_students"),
    path('manage_courses', admin_views.manage_courses, name="manage_courses"),
    path('manage_subjects', admin_views.manage_subjects, name="manage_subjects"),
    path('add_subject', admin_views.add_subject, name="add_subject"),
    path('save_subject', admin_views.save_subject, name="save_subject"),
    path('edit_subject/<str:subject_id>', admin_views.edit_subject, name="edit_subject"),
    path('save_subject_edits', admin_views.save_subject_edits, name="save_subject_edits"),
    path('edit_course/<str:course_id>', admin_views.edit_course, name="edit_course"),
    path('save_course_edits', admin_views.save_course_edits, name="save_course_edits"),
    path('manage_session', admin_views.manage_session, name="manage_session"),
    path('save_session_year', admin_views.save_session_year, name="save_session_year"),

    # Staff URLs
    path('staff_home', staff_views.staff_home, name="staff_home"),
    path('take_attendance', staff_views.take_attendance, name="take_attendance"),
    path('update_attendance', staff_views.update_attendance, name="update_attendance"),
    path('get_students', staff_views.get_students, name="get_students"),
    path('save_attendance', staff_views.save_attendance, name="save_attendance"),
    path('save_attendance_updates', staff_views.save_attendance_updates, name="save_attendance_updates"),
    path('get_attendance_dates', staff_views.get_attendance_dates, name="get_attendance_dates"),
    path('get_student_attendance', staff_views.get_student_attendance, name="get_student_attendance"),
    path('staff_leave_request', staff_views.staff_leave_request, name="staff_leave_request"),
    path('save_staff_leave_request', staff_views.save_staff_leave_request, name="save_staff_leave_request"),
    path('staff_feedback', staff_views.staff_feedback, name="staff_feedback"),
    path('save_staff_feedback', staff_views.save_staff_feedback, name="save_staff_feedback"),

    # Student URLs
    path('student_home', student_views.student_home, name="student_home"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
