from rest_framework.exceptions import ParseError

def get_request_data(request, key, default_value=None):
    """
    Extracts data from request.data, request.FILES, and request.query_params based on the request method and content type.

    :param request: Petra request object
    :param key: The key to look for in the request data
    :param default_value: The default value to return if the key is not found
    :return: The value associated with the key, or the default value if not found
    """
    try:
        if request.method in ['POST', 'PUT', 'PATCH']:
            if request.content_type.startswith('multipart/form-data'):
                # For file uploads
                if key in request.FILES:
                    return request.FILES.get(key)
                elif key in request.data:
                    return request.data.get(key)
            elif request.content_type in ['application/json', 'application/x-www-form-urlencoded']:
                # For JSON or form-encoded data
                if key in request.data:
                    return request.data.get(key)
        elif request.method == 'GET':
            if key in request.query_params:
                return request.query_params.get(key)
        else:
            if key in request.query_params:
                return request.query_params.get(key)
              
        return default_value
    except Exception as e:
        raise ParseError(f"Error extracting request data for key '{key}': {str(e)}")

def get_all_request_data(request):
    """
    Combines all request data from query_params, request.data, and FILES into a single dictionary.
    
    :param request: Petra request object
    :return: Dictionary containing all request data
    """
    try:
        combined_data = {}
        
        # Add query parameters
        combined_data.update(request.query_params.dict())
        
        # Add request data for POST/PUT/PATCH methods
        if request.method in ['POST', 'PUT', 'PATCH']:
            if request.content_type.startswith('multipart/form-data'):
                # Add both form data and files
                combined_data.update(request.data.dict())
                combined_data.update(request.FILES.dict())
            elif request.content_type in ['application/json', 'application/x-www-form-urlencoded']:
                # Add JSON or form-encoded data
                combined_data.update(request.data)
                
        return combined_data
    except Exception as e:
        raise ParseError(f"Error extracting all request data: {str(e)}")
