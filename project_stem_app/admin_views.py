from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from project_stem_app.models import Staff, CustomUser, Courses, Subjects, Students


def admin_home(request):
    """Main view of admins home page"""
    return render(request, 'admin_template/home.html')


def add_staff(request):
    """Main view of admins home page"""
    return render(request, 'admin_template/add_staff.html')


def save_staff(request):
    """Link to form for saving staff"""
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.create_user(
                username = username,
                password = password,
                email = email,
                last_name = last_name,
                first_name = first_name,
                user_type = 2
                )
            user.staff.address = address
            user.save()
            messages.success(request, "Successfully Added Staff")
            return HttpResponseRedirect("add_staff")
        except:
            messages.error(request, "Failed to Add Staff. Please try again")
            return HttpResponseRedirect("add_staff")


def add_course(request):
    return render(request, 'admin_template/add_course.html')


def save_course(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        course = request.POST.get("course")
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Successfully Added Course")
            return HttpResponseRedirect("add_course")
        except:
            messages.error(request, "Failed to Add Course. Please try again")
            return HttpResponseRedirect("add_course")


def add_student(request):
    courses = Courses.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'admin_template/add_student.html', context)


def save_student(request):
    """Link to form for saving students"""
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        session_start = request.POST.get("session_start")
        session_end = request.POST.get("session_end")
        course_id = request.POST.get("course")
        gender = request.POST.get("gender")
        try:
            user = CustomUser.objects.create_user(
                username = username,
                password = password,
                email = email,
                last_name = last_name,
                first_name = first_name,
                user_type = 3
                )
            course_obj = Courses.objects.get(id=course_id)
            user.students.address = address
            user.students.course_id = course_obj
            user.students.session_start_year= session_start
            user.students.session_end_year = session_end
            user.students.gender = gender
            user.students.profile_pic = ""
            user.save()
            messages.success(request, "Successfully Added Student")
            return HttpResponseRedirect("add_student")
        except:
            messages.error(request, "Failed to Add Student. Please try again")
            return HttpResponseRedirect("add_student")


def add_subject(request):
    courses = Courses.objects.all()
    staff = CustomUser.objects.filter(user_type=2)
    context = {
        'courses': courses,
        'staff': staff,
    }
    return render(request, 'admin_template/add_subject.html', context)


def save_subject(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course")
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subjects(
                subject_name = subject_name,
                course_id = course,
                staff_id = staff
                )
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect("add_subject")
        except:
            messages.error(request, "Failed to Add Subject. Please try again")
            return HttpResponseRedirect("add_subject")


def manage_staff(request):
    staff = Staff.objects.all()
    context = {
        'staff': staff,
    }
    return render(request, 'admin_template/manage_staff.html', context)


def manage_students(request):
    students = Students.objects.all()
    context = {
        'students': students,
    }
    return render(request, 'admin_template/manage_students.html', context)


def manage_courses(request):
    courses = Courses.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'admin_template/manage_courses.html', context)
    subjects

def manage_subjects(request):
    subjects = Subjects.objects.all()
    staff = Staff.objects.all()
    courses = Courses.objects.all()
    context = {
        'subjects': subjects,
        'courses': courses,
        'staff': staff,
    }
    return render(request, 'admin_template/manage_subjects.html', context)
