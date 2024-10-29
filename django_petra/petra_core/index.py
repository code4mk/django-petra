from rest_framework.viewsets import ViewSet as View
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from drf_friend.status import Status as MyStatus

class ViewSet(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Response(Response):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class status(MyStatus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class ModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)