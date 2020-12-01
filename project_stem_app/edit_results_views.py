from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View
from project_stem_app.forms import EditResultForm
from project_stem_app.models import Students, Subjects, StudentResult



class EditResult(View):
    def get(self, request, *args, **kwargs):
        staff_id = request.user.id
        edit_result_form = EditResultForm(staff_id=staff_id)
        context = {
            'staff_id': staff_id,
            'form': edit_result_form,
        }
        return render(request, "staff_template/edit_student_result.html", context)

    def post(self, request, *args, **kwargs):
        form = EditResultForm(request.POST, staff_id=request.user.id)
        if form.is_valid():
            student_admin_id = form.cleaned_data['student_ids']
            assignment_marks = form.cleaned_data['assignment_marks']
            exam_marks = form.cleaned_data['exam_marks']
            subject_id = form.cleaned_data['subject_id']

            student_obj = Students.objects.get(admin=student_admin_id)
            subject_obj = Subjects.objects.get(id=subject_id)
            result = StudentResult.objects.get(subject_id=subject_obj, student_id=student_obj)
            result.subject_assignment=assignment_marks
            result.subject_exam=exam_marks
            result.save()
            messages.success(request, "Successfully Updated Results")
            return HttpResponseRedirect(reverse("edit_student_result"))
        else:
            messages.error(request, "Failed to update results")
            form = EditResultForm(request.POST, staff_id=request.user.id)
            context = {
                'form': form,
            }
            return render(request, "staff_template/edit_student_result.html", context)
