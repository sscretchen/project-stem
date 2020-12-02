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
                if module_name == "project_stem_app.staff_views" or module_name == "project_stem_app.edit_results_views":
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
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse("login_user") or module_name == "django.contrib.auth.views" or module_name == "project_stem_app.views":
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))
