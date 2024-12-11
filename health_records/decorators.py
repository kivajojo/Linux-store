from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from functools import wraps
from django.http import HttpResponseForbidden
from .models import HealthRecord

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, '需要管理员权限')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def user_record_access(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        record_id = kwargs.get('record_id')
        if record_id:
            record = HealthRecord.objects.get(id=record_id)
            if not request.user.is_staff and record.user != request.user:
                messages.error(request, '无权访问此记录')
                return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def user_owns_record(view_func):
    def wrapper(request, record_id, *args, **kwargs):
        record = get_object_or_404(HealthRecord, id=record_id)
        if record.user != request.user:
            return HttpResponseForbidden("您没有权限访问此记录")
        return view_func(request, record_id, *args, **kwargs)
    return wrapper