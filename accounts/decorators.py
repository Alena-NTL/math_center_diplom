from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps


def admin_required(view_func):
    """Доступ только для администраторов."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin_role:
            raise PermissionDenied('Доступ только для администраторов')
        return view_func(request, *args, **kwargs)
    return wrapper


def teacher_required(view_func):
    """Доступ для преподавателей и администраторов."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ('admin', 'teacher'):
            raise PermissionDenied('Доступ только для преподавателей')
        return view_func(request, *args, **kwargs)
    return wrapper
