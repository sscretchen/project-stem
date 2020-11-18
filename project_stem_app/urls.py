from django.urls import path
from .views import *
from .admin_views import *
from .staff_views import *
from .student_views import *

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
    path('manage_staff', manage_staff, name="manage_staff"),
    path('manage_students', manage_students, name="manage_students"),
    path('manage_courses', manage_courses, name="manage_courses"),
    path('manage_subjects', manage_subjects, name="manage_subjects"),
    path('add_subject', add_subject, name="add_subject"),
    path('save_subject', save_subject, name="save_subject"),
    path('edit_subject/<str:subject_id>', edit_subject, name="edit_subject"),
    path('save_subject_edits', save_subject_edits, name="save_subject_edits"),
    path('edit_course/<str:course_id>', edit_course, name="edit_course"),
    path('save_course_edits', save_course_edits, name="save_course_edits"),
    path('manage_session', manage_session, name="manage_session"),
    path('save_session_year', save_session_year, name="save_session_year"),

    # Staff URLs
    path('staff_home', staff_home, name="staff_home"),
    path('take_attendance', take_attendance, name="take_attendance"),
    path('update_attendance', update_attendance, name="update_attendance"),
    path('get_students', get_students, name="get_students"),
    path('save_attendance', save_attendance, name="save_attendance"),
    path('save_attendance_updates', save_attendance_updates, name="save_attendance_updates"),
    path('get_attendance_dates', get_attendance_dates, name="get_attendance_dates"),
    path('get_student_attendance', get_student_attendance, name="get_student_attendance"),

    # Student URLs
    path('student_home', student_home, name="student_home"),

    # Custom page URLs
]
