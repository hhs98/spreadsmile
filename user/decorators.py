from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from .models import Organization


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            group_names = set(request.user.groups.values_list('name', flat=True))
            if 'admins' in group_names:
                return redirect('admin', pk=request.user.id)
            if 'organizations' in group_names:
                try:
                    return redirect('back', pk=request.user.organization.id)
                except Organization.DoesNotExist:
                    return redirect('home')
            return redirect('home')
        return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []
    allowed_set = frozenset(allowed_roles)

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            user_groups = set(request.user.groups.values_list('name', flat=True))
            if user_groups & allowed_set:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden(
                'You are not authorized to view this page.'
            )

        return wrapper_func

    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group_names = set(request.user.groups.values_list('name', flat=True))
        if 'organizations' in group_names:
            try:
                return redirect('back', pk=request.user.organization.id)
            except Organization.DoesNotExist:
                return HttpResponseForbidden(
                    'Organization profile is missing for this account.'
                )
        if 'admins' in group_names:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden(
            'You are not authorized to view this page.'
        )

    return wrapper_function
