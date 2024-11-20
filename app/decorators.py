from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def department_required(department):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')  # Redirect to login if not authenticated
            
            if hasattr(request.user, 'profile') and request.user.profile.department == department:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have access to this department.")
        return _wrapped_view
    return decorator
