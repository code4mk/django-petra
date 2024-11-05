from collections import OrderedDict
from math import ceil
from django.core.paginator import Paginator
from rest_framework.response import Response
from urllib.parse import urlparse

def paginate(request, queryset, serializer_class, per_page=10, wrap='data', additional_data=None):
    # Get per_page from query params if present, otherwise use default
    per_page = int(request.query_params.get('per_page', per_page))
    page = int(request.query_params.get('page', 1))
    total = queryset.count()
    last_page = ceil(total / per_page)
    offset = (page - 1) * per_page

    paginated_queryset = queryset[offset:offset + per_page]
    serializer = serializer_class(paginated_queryset, many=True)
    data = serializer.data

    full_path = str(request.build_absolute_uri())
    parsed_url = urlparse(full_path)
    path_without_query = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

    first_page_url = f"{path_without_query}?page=1&per_page={per_page}"
    last_page_url = f"{path_without_query}?page={last_page}&per_page={per_page}"
    next_page_url = f"{path_without_query}?page={page + 1}&per_page={per_page}" if page < last_page else None
    prev_page_url = f"{path_without_query}?page={page - 1}&per_page={per_page}" if page > 1 else None

    # Convert all URLs to strings explicitly
    response_data = OrderedDict([
        (wrap, data),
        ('total', total),
        ('per_page', int(per_page)),  # ensure integer
        ('current_page', int(page)),   # ensure integer
        ('last_page', int(last_page)), # ensure integer
        ('first_page_url', str(first_page_url)),
        ('last_page_url', str(last_page_url)),
        ('next_page_url', str(next_page_url) if next_page_url else None),
        ('prev_page_url', str(prev_page_url) if prev_page_url else None),
    ])

    # Merge additional_data if provided
    if additional_data:
        response_data['additional_data'] = additional_data

    return response_data