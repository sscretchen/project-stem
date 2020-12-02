from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from project_stem_app.EmailBackEnd import EmailBackEnd
from django.contrib import messages
from project_stem_app.models import CustomUser, Courses, SessionYearModel, Staff, Students
import requests
import datetime
import json


# Create your views here.
def ShowLoginPage(request):
    """Login view"""
    return render(request,"login_page.html")


def login_user(request):
    """Allow users to login"""
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        captcha_token = request.POST.get("g-recaptcha-response")
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        captcha_secret = "6LdRjvUZAAAAAJfNvq2yS5F5ijo8QEO1anHTiL5f"
        captcha_data = {"secret": captcha_secret, "response": captcha_token}
        captcha_response = requests.post(url=captcha_url, data=captcha_data)
        captcha_json = json.loads(captcha_response.text)
        if captcha_json['success'] == False:
            messages.error(request,"Captcha Validation Failed")
            return HttpResponseRedirect("/")

        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect('admin_home')
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request,"Invalid login details")
            return HttpResponseRedirect("/")


def UserDetails(request):
    if request.user != None:
        return HttpResponse("User : " + request.user.email + " usertype : " + str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def admin_signup(request):
    return render(request,"admin_signup.html")


def student_signup(request):
    courses = Courses.objects.all()
    session_years = SessionYearModel.object.all()
    context = {
        'courses': courses,
        'session_years': session_years,
    }
    return render(request,"student_signup.html", context)


def staff_signup(request):
    return render(request,"staff_signup.html")


def do_admin_signup(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    try:
        user = CustomUser.objects.create_user(username=username, password=password, email=email, user_type=1)
        user.save()
        messages.success(request, "Successfully Added Admin User")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request, "Failed to create user")
        return HttpResponseRedirect(reverse("show_login"))


def do_staff_signup(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")

    try:
        user = CustomUser.objects.create_user(username=username, password=password, email=email, user_type=2)
        user.staff.address = address
        user.save()
        messages.success(request, "Successfully Added Staff User")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request, "Failed to create user")
        return HttpResponseRedirect(reverse("show_login"))


def do_student_signup(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    session_year_id = request.POST.get("session_year")
    course_id = request.POST.get("course")
    gender = request.POST.get("gender")

    profile_pic = request.FILES['profile_pic']
    file_system = FileSystemStorage()
    filename = file_system.save(profile_pic.name, profile_pic)
    profile_pic_url = file_system.url(filename)

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
        session_year = SessionYearModel.object.get(id=session_year_id)
        user.students.session_year_id = session_year
        user.students.gender = gender
        user.students.profile_pic = profile_pic_url
        user.save()
        messages.success(request, "Successfully Added Student User")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request, "Failed to create user")
        return HttpResponseRedirect(reverse("show_login"))
