from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from project_stem_app.EmailBackEnd import EmailBackEnd
from django.contrib import messages
import datetime

# Create your views here.
def index(request):
    """Main view of app"""
    return render(request, 'index.html')


def ShowLoginPage(request):
    """Login view"""
    return render(request,"login_page.html")


def login_user(request):
    """Allow users to login"""
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            return HttpResponseRedirect('admin_home')
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
    return HttpResponseRedirect("login")
