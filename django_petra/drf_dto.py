from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

def drf_dto(form_class):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            if request.content_type == 'application/json':
                # Handle JSON data
                form = form_class(request.data)
            else:
                # Handle form data
                form = form_class(request.POST)

            if form.is_valid():
                return view_func(self, request, form, *args, **kwargs)
            else:
                errors = form.errors
                raise ValidationError(errors)

        return wrapper

    return decorator



