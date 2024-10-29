from django.db import models

# class APILogs(models.Model):
#     timestamp = models.DateTimeField(auto_now_add=True)
#     url = models.URLField()
#     method = models.CharField(max_length=10)
#     request_headers = models.TextField()
#     request_body = models.TextField()
#     status_code = models.PositiveIntegerField()
#     response_content = models.TextField()
#     api_call_time = models.FloatField()
#     server_execution_time = models.FloatField()
#     client_ip = models.GenericIPAddressField()

#     class Meta:
#         db_table = 'drf_friend_api_logs'
