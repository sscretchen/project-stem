from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.urls import reverse


class LoginMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        module_name = view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if module_name == "project_stem_app.admin_views":
                    pass
                elif module_name == "project_stem_app.views" or module_name == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if module_name == "project_stem_app.staff_views":
                    pass
                elif module_name == "project_stem_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type == "3":
                if module_name == "project_stem_app.student_views" or module_name == "django.views.static":
                    pass
                elif module_name == "project_stem_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("login"))

        else:
            if request.path == reverse("login") or request.path == reverse("login_user"):
                pass
            else:
                return HttpResponseRedirect(reverse("login"))
