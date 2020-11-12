from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from project_stem_app.models import Staff, CustomUser


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
