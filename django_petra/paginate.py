from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict

class LaravelStylePagination(PageNumberPagination):
    page_size = 10
    
    def get_paginated_response(self, data, wrap):
        data =  (OrderedDict([
            ('per_page', self.page_size),
            ('current_page', self.page.number),
            ('last_page', self.page.paginator.num_pages),
            ('next_page_url', self.get_next_link() or None),
            ('prev_page_url', self.get_previous_link() or None),
            ('total', self.page.paginator.count),
            ('from', self.page.start_index()),
            ('to', self.page.end_index()),
            (wrap, data),
        ]))
        return data

        
def paginate(request, queryset, serializer_class, per_page=2, wrap='data'):
    # Create an instance of the custom pagination class
    paginator = LaravelStylePagination()
    paginator.page_size = per_page

    # Paginate the queryset
    page = paginator.paginate_queryset(queryset, request)

    # Serialize the paginated data using the provided serializer class
    serializer = serializer_class(page, many=True)

    # Return the paginated data along with pagination metadata
    return paginator.get_paginated_response(serializer.data, wrap)
