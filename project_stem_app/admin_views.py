from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from project_stem_app.models import Staff, CustomUser, Courses, Subjects, Students, SessionYearModel, StudentFeedBack, StaffFeedback, StudentLeaveReport, StaffLeaveReport, Attendance, AttendanceReport
from .forms import AddStudentForm, EditStudentForm
import json


def admin_home(request):
    """Main view of admins home page"""
    student_count1 = Students.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Courses.objects.all().count()
    subject_count = Subjects.objects.all().count()

    all_courses = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    student_to_course_count = []
    for course in all_courses:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_to_course_count.append(students)

    all_subjects = Subjects.objects.all()
    subject_list = []
    student_to_subject_count = []
    for subject in all_subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        student_count = Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_to_subject_count.append(student_count)

    staff_obj = Staff.objects.all()
    present_attendance_list_staff = []
    absent_attendance_list_staff = []
    list_of_staff = []
    for staff in staff_obj:
        subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
        attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
        leave = StaffLeaveReport.objects.filter(staff_id=staff.id, leave_status=1).count()
        present_attendance_list_staff.append(attendance)
        absent_attendance_list_staff.append(leave)
        list_of_staff.append(staff.admin.username)

    students = Students.objects.all()
    present_attendance_list_students = []
    absent_attendance_list_students = []
    list_of_students = []
    for student in students:
        attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        leave = StudentLeaveReport.objects.filter(student_id=student.id, leave_status=1).count()
        present_attendance_list_students.append(attendance)
        absent_attendance_list_students.append(leave+absent)
        list_of_students.append(student.admin.username)

    context = {
        'student_count': student_count1,
        'staff_count': staff_count,
        'present_attendance_list_staff': present_attendance_list_staff,
        'absent_attendance_list_staff': absent_attendance_list_staff,
        'present_attendance_list_students': present_attendance_list_students,
        'absent_attendance_list_students': absent_attendance_list_students,
        'course_count': course_count,
        'list_of_staff': list_of_staff,
        'list_of_students': list_of_students,
        'subject_count': subject_count,
        'course_name_list': course_name_list,
        'subject_count_list': subject_count_list,
        'subject_list': subject_list,
        'student_to_course_count': student_to_course_count,
        'student_to_subject_count': student_to_subject_count,
    }
    return render(request, 'admin_template/home.html', context)


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
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request, "Failed to Add Staff. Please try again")
            return HttpResponseRedirect(reverse("add_staff"))


def add_course(request):
    return render(request, 'admin_template/add_course.html')


def save_course(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course = request.POST.get("course")
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request, "Failed to Add Course. Please try again")
            return HttpResponseRedirect(reverse("add_course"))


def add_student(request):
    form = AddStudentForm()
    context = {
        "form": form,
    }
    return render(request, 'admin_template/add_student.html', context)


def save_student(request):
    """Link to form for saving students"""
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            gender = form.cleaned_data["gender"]
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
                messages.success(request, "Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request, "Failed to Add Student. Please try again")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form = AddStudentForm(request.POST)
            return render(request, 'admin_template/add_student.html', {"form": form})


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
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request, "Failed to Add Subject. Please try again")
            return HttpResponseRedirect(reverse("add_subject"))


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


def edit_staff(request, staff_id):
    staff = Staff.objects.get(admin=staff_id)
    context ={
        'staff': staff,
        'id': staff_id,
    }
    return render(request, 'admin_template/edit_staff.html', context)


def save_staff_edits(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            staff_model = Staff.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()
            messages.success(request, "Edits saved successfully")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id": staff_id}))
        except:
            messages.error(request, "Edits were unsuccessful")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id": staff_id}))


def edit_student(request, student_id):
    request.session['student_id'] = student_id
    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields['email'].initial = student.admin.email
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['username'].initial = student.admin.username
    form.fields['address'].initial = student.address
    form.fields['course'].initial = student.course_id.id
    form.fields['gender'].initial = student.gender
    form.fields['session_year_id'].initial = student.session_year_id.id
    context ={
        'form': form,
        'id': student_id,
        'username': student.admin.username
    }
    return render(request, 'admin_template/edit_student.html', context)


def save_student_edits(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        student_id = request.session.get("student_id")
        if student_id == None:
            return HttpResponseRedirect(reverse("manage_students"))
        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            gender = form.cleaned_data["gender"]

            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                file_system = FileSystemStorage()
                filename = file_system.save(profile_pic.name, profile_pic)
                profile_pic_url = file_system.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                student = Students.objects.get(admin=student_id)
                student.address = address
                session_year = SessionYearModel.object.get(id=session_year_id)
                student.session_year_id = session_year
                student.gender = gender
                course = Courses.objects.get(id=course_id)
                student.course_id = course
                if profile_pic_url != None:
                    student.profile_pic = profile_pic_url
                student.save()
                del request.session['student_id']

                messages.success(request, "Edits saved successfully")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))
            except:
                messages.error(request, "Edits were unsuccessful")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": student_id}))
        else:
            form = EditStudentForm(request.POST)
            student = Students.objects.get(admin=student_id)
            return render(request, 'admin_template/edit_student.html', {"username": student.admin.username})


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staff = CustomUser.objects.filter(user_type=2)
    context = {
        'subject': subject,
        'courses': courses,
        'staff': staff,
        'id': subject_id,
    }
    return render(request, 'admin_template/edit_subject.html', context)


def save_subject_edits(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        staff_id = request.POST.get("staff")
        course_id = request. POST.get("course")

        try:
            subject = Subjects.objects.get(id=subject_id)
            staff = CustomUser.objects.get(id=staff_id)
            course = Courses.objects.get(id=course_id)
            subject.subject_name = subject_name
            subject.staff_id = staff
            subject.course_id = course
            subject.save()
            messages.success(request, "Edits saved successfully")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id": subject_id}))
        except:
            messages.error(request, "Edits were unsuccessful")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id": subject_id}))


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    context = {
        'course': course,
        'id': course_id
    }
    return render(request, 'admin_template/edit_course.html', context)


def save_course_edits(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course_name")

        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request, "Edits saved successfully")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id": course_id}))
        except:
            messages.error(request, "Edits were unsuccessful")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id": course_id}))


def manage_session(request):
    return render(request, "admin_template/manage_session.html")


def save_session_year(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_session", kwargs={"course_id": course_id}))
    else:
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_end")

        try:
            session_year = SessionYearModel(
                session_start_year=session_start_year,
                session_end_year=session_end_year
            )
            session_year.save()
            messages.success(request, "Session added successfully")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to add session")
            return HttpResponseRedirect(reverse("manage_session"))


@csrf_exempt
def check_for_email(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_for_username(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def staff_feedback_response(request):
    feedback = StaffFeedback.objects.all()
    context = {
        'feedback': feedback,
    }
    return render(request, 'admin_template/staff_feedback_response.html', context)


def student_feedback_response(request):
    feedback = StudentFeedBack.objects.all()
    context = {
        'feedback': feedback,
    }
    return render(request, 'admin_template/student_feedback_response.html', context)


@csrf_exempt
def student_feedback_response_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:
        feedback = StudentFeedBack.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse(True)
    except:
        return HttpResponse(False)


@csrf_exempt
def staff_feedback_response_replied(request)        :
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:
        feedback = StaffFeedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse(True)
    except:
        return HttpResponse(False)


def student_leave(request):
    leave = StudentLeaveReport.objects.all()
    context = {
        'leave': leave,
    }
    return render(request, "admin_template/student_leave.html", context)


def approve_student_leave(request, leave_id):
    leave = StudentLeaveReport.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave"))


def deny_student_leave(request, leave_id):
    leave = StudentLeaveReport.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave"))


def staff_leave(request):
    leave = StaffLeaveReport.objects.all()
    context = {
        'leave': leave,
    }
    return render(request, "admin_template/staff_leave.html", context)


def approve_staff_leave(request, leave_id):
    leave = StaffLeaveReport.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave"))


def deny_staff_leave(request, leave_id):
    leave = StaffLeaveReport.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave"))


def admin_attendance_view(request):
    subjects = Subjects.objects.all()
    session_year_id = SessionYearModel.object.all()
    context = {
        'subjects': subjects,
        'session_year_id': session_year_id,
    }
    return render(request, "admin_template/admin_attendance_view.html", context)


@csrf_exempt
def admin_get_attendance_dates(request):
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
def admin_get_attendance_student(request):
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


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        'user': user,
    }
    return render(request, "admin_template/admin_profile.html", context)


def save_profile_edits(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
