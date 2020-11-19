from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Subjects, SessionYearModel, Students, AttendanceReport, Attendance, StaffLeaveReport, Staff, StaffFeedback
from django.core import serializers
import json


def staff_home(request):
    return render(request, 'staff_template/home.html')


def take_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.object.all()
    context = {
        'subjects': subjects,
        'session_years': session_years,
    }
    return render(request, 'staff_template/take_attendance.html', context)


@csrf_exempt
def get_students(request):
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year")
    subject = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.object.get(id=session_year)
    students = Students.objects.filter(
        course_id=subject.course_id,
        session_year_id=session_model
    )
    list_data = []

    for student in students:
        data_small = {"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_attendance(request):
    student_ids = request.POST.get("student_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")
    subject_model = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.object.get(id=session_year_id)
    json_student = json.loads(student_ids)

    try:
        attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date, session_year_id=session_model)
        attendance.save()

        for stud in json_student:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERROR")


def update_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_year_id = SessionYearModel.object.all()
    context = {
        'subjects': subjects,
        'session_year_id': session_year_id,
    }
    return render(request, 'staff_template/update_attendance.html', context)


@csrf_exempt
def get_attendance_dates(request):
    subject = request.POST.get("subject")
    session_year_id = request.POST.get("session_year_id")
    subject_obj = Subjects.objects.get(id=subject)
    session_year_obj = SessionYearModel.object.get(id=session_year_id)
    attendance = Attendance.objects.filter(subject_id=subject_obj, session_year_id=session_year_obj)
    attendance_obj = []
    for attendance_single in attendance:
        data = {
            'id': attendance_single.id,
            'attendance_date': str(attendance_single.attendance_date),
            'session_year_id': attendance_single.session_year_id.id
        }
        attendance_obj.append(data)
    return JsonResponse(json.dumps(attendance_obj), safe=False)


@csrf_exempt
def get_student_attendance(request):
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []

    for student in attendance_data:
        data_small = {
            "id":student.student_id.admin.id,
            "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,
            "status":student.status
            }
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


@csrf_exempt
def save_attendance_updates(request):
    student_ids = request.POST.get("student_ids")
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)
    json_student = json.loads(student_ids)

    try:
        for stud in json_student:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status = stud['status']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERROR")


def staff_leave_request(request):
    staff_obj = Staff.objects.get(admin=request.user.id)
    leave_data = StaffLeaveReport.objects.filter(staff_id=staff_obj)
    context = {
        'staff_obj': staff_obj,
        'leave_data': leave_data,
    }
    return render(request, 'staff_template/staff_leave_request.html', context)


def save_staff_leave_request(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_leave_request"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")

        staff_obj = Staff.objects.get(admin=request.user.id)
        try:
            leave_report = StaffLeaveReport(
                staff_id=staff_obj,
                leave_date=leave_date,
                leave_message=leave_msg,
                leave_status=0
                )
            leave_report.save()
            messages.success(request, "Successfully Added Leave Request")
            return HttpResponseRedirect(reverse("staff_leave_request"))
        except:
            messages.error(request, "Failed to add Leave Request. Please try again")
            return HttpResponseRedirect(reverse("staff_leave_request"))


def staff_feedback(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    feedback_data = StaffFeedback.objects.filter(staff_id=staff_id)
    context = {
        'staff_id': staff_id,
        'feedback_data': feedback_data,
    }
    return render(request, "staff_template/staff_feedback.html", context)


def save_staff_feedback(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_feedback"))
    else:
        feedback_msg = request.POST.get("feedback_msg")

        staff_obj = Staff.objects.get(admin=request.user.id)
        try:
            feedback = StaffFeedback(
            staff_id=staff_obj,
            feedback=feedback_msg,
            feedback_reply=""
            )
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request, "Failed to send feedback. Please try again")
            return HttpResponseRedirect(reverse("staff_feedback"))
