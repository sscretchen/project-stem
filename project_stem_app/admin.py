from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)
# admin.site.register(AdminHOD)
# admin.site.register(Staff)
# admin.site.register(Courses)
# admin.site.register(Subjects)
# admin.site.register(Students)
# admin.site.register(Attendance)
# admin.site.register(AttendanceReport)
# admin.site.register(StudentLeaveReport)
# admin.site.register(StaffLeaveReport)
# admin.site.register(StudentFeedBack)
# admin.site.register(StaffFeedback)
# admin.site.register(StudentNotification)
# admin.site.register(StaffNotification)
