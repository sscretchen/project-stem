from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from project_stem_app.models import Subjects, Students, Courses, CustomUser, Attendance, AttendanceReport, StudentLeaveReport, StudentFeedBack, StudentResult
import datetime


def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    total_attendance = AttendanceReport.objects.filter(student_id=student_obj).count()
    present_attendance = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    absent_attendance = AttendanceReport.objects.filter(student_id=student_obj, status=False).count()
    course = Courses.objects.get(id=student_obj.course_id.id)
    subjects = Subjects.objects.filter(course_id=course).count()

    subject_name = []
    present_data = []
    absent_data = []
    subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        present_attendance_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, student_id=student_obj.id).count()
        absent_attendance_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        present_data.append(present_attendance_count)
        absent_data.append(absent_attendance_count)



    context = {
        'student_obj': student_obj,
        'total_attendance': total_attendance,
        'present_attendance': present_attendance,
        'absent_attendance': absent_attendance,
        'course': course,
        'subjects': subjects,
        'subject_data': subject_data,
        'data_name': subject_name,
        'data1': present_data,
        'data2': absent_data,
    }
    return render(request, 'student_template/home.html', context)


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


def student_leave_request(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = StudentLeaveReport.objects.filter(student_id=student_obj)
    context = {
        'student_obj': student_obj,
        'leave_data': leave_data,
    }
    return render(request, 'student_template/student_leave_request.html', context)


def save_student_leave_request(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_leave_request"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = StudentLeaveReport(
                student_id=student_obj,
                leave_date=leave_date,
                leave_message=leave_msg,
                leave_status=0
                )
            leave_report.save()
            messages.success(request, "Successfully Added Leave Request")
            return HttpResponseRedirect(reverse("student_leave_request"))
        except:
            messages.error(request, "Failed to add Leave Request. Please try again")
            return HttpResponseRedirect(reverse("student_leave_request"))


def student_feedback(request):
    student_id = Students.objects.get(admin=request.user.id)
    feedback_data = StudentFeedBack.objects.filter(student_id=student_id)
    context = {
        'student_id': student_id,
        'feedback_data': feedback_data,
    }
    return render(request, "student_template/student_feedback.html", context)


def save_student_feedback(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_msg = request.POST.get("feedback_msg")

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            feedback = StudentFeedBack(
            student_id=student_obj,
            feedback=feedback_msg,
            feedback_reply=""
            )
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Failed to send feedback. Please try again")
            return HttpResponseRedirect(reverse("student_feedback"))


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
    context = {
        'user': user,
        'student': student,
    }
    return render(request, "student_template/student_profile.html", context)


def save_student_profile_edits(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            student = Students.objects.get(admin=customuser)
            student.address = address
            student.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("student_profile"))


def view_results(request):
        student = Students.objects.get(admin=request.user.id)
        students_results = StudentResult.objects.filter(student_id=student.id)
        context = {
            'student': student,
            'students_results': students_results,
        }
        return render(request, "student_template/view_results.html", context)
