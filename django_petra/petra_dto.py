from functools import wraps
from rest_framework.exceptions import ValidationError

def petra_dto(form_class):
    """
    Decorator that validates incoming request data using a form class.
    Handles both JSON and form-encoded data.
    
    Args:
        form_class: Django Form class to validate the request data
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            if request.content_type == 'application/json':
                form = form_class(request.data)
            else:
                form = form_class(request.POST)

            if form.is_valid():
                return view_func(self, request, form, *args, **kwargs)
            
            raise ValidationError(form.errors)
        return wrapper
    return decorator



