from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from project_stem_app.EmailBackEnd import EmailBackEnd
from django.contrib import messages
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
