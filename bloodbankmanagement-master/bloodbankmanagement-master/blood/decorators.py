# decorators.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def admin_or_staff_required(view_func):
    """
    Decorator to allow access only to superusers or staff members.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")
    return login_required(login_url='adminlogin')(_wrapped_view)
