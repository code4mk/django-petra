import os
from collections import OrderedDict
from drf_friend.path import base_path
from drf_friend.env import getEnv
    
def load_sql(sql_file, load_from_module = False):
    if load_from_module == True:
      components = sql_file.split('.')
      path = base_path('modules', getEnv('RAW_SQL_MODULE_DIR', 'sql_quries'), *components)
      path_with_extension = path + ".sql"
    else:
      components = sql_file.split('.')
      path = base_path(getEnv('RAW_SQL_DIR', 'raw_sql'), *components)
      path_with_extension = path + ".sql"

    # Open and read the SQL file
    with open(path_with_extension, 'r') as file:
        return file.read()
      
def fetch_all_to_dictionary(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def raw_query_collection(request, results, wrap="data", type='paginate', serializer_class=None):
    """
    Paginate a raw query result and construct a Laravel-style response.

    Parameters:
    - request: The Django request object containing query parameters.
    - results: The list of results to paginate.
    - wrap: The key to wrap around the paginated results in the response.

    Query Parameters:
    - page: The page number to retrieve (default: 1).
    - per_page: The number of items per page (default: 10).

    Returns:
    An OrderedDict containing paginated results and pagination information.
    """

    # Get the page and per_page values from the request query parameters
    page = int(request.query_params.get('page', 1))
    per_page = int(request.query_params.get('per_page', 10))

    # Calculate indices for the range of items to be displayed on the current page
    from_index = (page - 1) * per_page + 1
    to_index = min(page * per_page, len(results))

    # Calculate start and end indices for slicing the paginated results
    start_index = (page - 1) * per_page
    end_index = page * per_page

    # Slice the results to get the paginated subset
    paginated_results = results[start_index:end_index]

    # Calculate the total number of pages
    total_pages = (len(results) + per_page - 1) // per_page

    # Determine the next and previous page numbers
    next_page = page + 1 if page < total_pages else None
    prev_page = page - 1 if page > 1 else None

    # Build URLs for the next and previous pages
    base_url = request.build_absolute_uri(request.path)
    next_page_url = f"{base_url}?page={next_page}&per_page={per_page}" if next_page else None
    prev_page_url = f"{base_url}?page={prev_page}&per_page={per_page}" if prev_page else None

    if serializer_class:
        # Serialize the paginated results using the provided serializer class
        the_serializer = serializer_class(data=paginated_results, many=True)
        the_serializer.is_valid()
        
        serialized_results = the_serializer.data
    else:
        serialized_results = paginated_results

    if type == 'single':
        # If a single result is expected, handle the case where the results list is empty
        if paginated_results:
            to_index = from_index
            response_data = OrderedDict([(wrap, serialized_results[0])])
        else:
            # If results list is empty, return an empty response
            response_data = OrderedDict([(wrap, {})])
    elif type == 'all':
        if paginated_results:
            to_index = from_index
            response_data = OrderedDict([(wrap, serialized_results)])
        else:
            # If results list is empty, return an empty response
            response_data = OrderedDict([(wrap, [])])
    else:
        # Construct Laravel-style response with pagination information
        response_data = OrderedDict([
            (wrap, serialized_results),
            ('per_page', len(serialized_results)),
            ('current_page', page),
            ('last_page', total_pages),
            ('next_page_url', next_page_url),
            ('prev_page_url', prev_page_url),
            ('total', len(results)),
            ('from', from_index),
            ('to', to_index),
        ])

    return response_data

def exclude_fields(representation, fields_to_exclude):
    for field in list(fields_to_exclude):
        representation.pop(field, None)
    return representation