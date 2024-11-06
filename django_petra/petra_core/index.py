from rest_framework.viewsets import ViewSet as View
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from django_petra.status import Status as MyStatus
from django_petra.petra_core.permissions import Permissions

class ViewSet(View, Permissions):
    def __init__(self, *args, **kwargs):
        View.__init__(self, *args, **kwargs)
        Permissions.__init__(self)

class Response(Response):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class status(MyStatus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class ModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)