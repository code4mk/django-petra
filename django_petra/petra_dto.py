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
            
            # Format the error response
            formatted_errors = {
                'success': False,
                'errors': {}
            }

            for field, error_list in form.errors.items():
                # Convert to array format
                formatted_errors['errors'][field] = [
                    f"The {field} {error_list[0]}"  # Format error message
                ]
            
            raise ValidationError(formatted_errors)
        return wrapper
    return decorator



