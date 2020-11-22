from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from project_stem_app.models import Subjects, Students, Courses, CustomUser, Attendance, AttendanceReport
import datetime


def student_home(request):
    return render(request, 'student_template/home.html')


def student_attendance_view(request):
    student = Students.objects.get(admin=request.user.id)
    course = Courses.objects.get(id=student.course_id.id)
    subjects = Subjects.objects.filter(course_id=course)
    context = {
        'student': student,
        'course': course,
        'subjects': subjects,
    }
    return render(request, "student_template/student_attendance_view.html", context)


def student_attendance_report(request):
    subject_id = request. POST.get("subject")
    start_date = request. POST.get("start_date")
    end_date = request. POST.get("end_date")
    parse_start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    parse_end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    subject_obj = Subjects.objects.get(id=subject_id)
    user_obj = CustomUser.objects.get(id=request.user.id)
    stud_obj = Students.objects.get(admin=user_obj)
    attendance = Attendance.objects.filter(attendance_date__range=(parse_start, parse_end), subject_id=subject_obj)
    attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=stud_obj)
    context = {
        'attendance_reports': attendance_reports,
    }

    return render(request, "student_template/student_attendance_report.html", context)
