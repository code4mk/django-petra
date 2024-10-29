from django.utils import timezone
from drf_friend.project.models import APILogs

class APILoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = timezone.now()
        response = self.get_response(request)
        end_time = timezone.now()
        api_call_time = (end_time - start_time).total_seconds()

        # Log API request and response to the database
        if 'hello-drf-friend/api/show-api-logs/' not in request.path :
            self.log_api(request, response, api_call_time)

        return response

    def log_api(self, request, response, api_call_time):

        log_entry = APILogs(
            url=request.build_absolute_uri(),
            method=request.method,
            request_headers=str(request.headers),
            request_body=str(request.body),
            status_code=response.status_code,
            response_content=str(response.content),
            api_call_time=api_call_time,
            server_execution_time=0.0,  # Placeholder for server execution time
            client_ip=request.META.get('REMOTE_ADDR', ''),
        )
        log_entry.save()
        print("yes")
