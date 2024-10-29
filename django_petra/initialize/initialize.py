import os
import django
import importlib
from django.conf import settings
from drf_friend.core import bind_modules_app, bind_modules_urls
from drf_friend.path import base_module_name

def init_cors_middleware():
    cors_middleware_class = 'drf_friend.cors.middleware.CorsMiddleware'
    settings.MIDDLEWARE.insert(0, cors_middleware_class)
    
def init_all_modules():
  settings.INSTALLED_APPS.extend(bind_modules_app())
  
def init_module_urls():
  the_django_setup()
  the_base_module_name = base_module_name()
  the_urls = importlib.import_module(f"{the_base_module_name}.urls")
  urlpatterns = the_urls.urlpatterns
  urlpatterns.extend(bind_modules_urls())
  
def the_django_setup():
  the_base_module_name = base_module_name()
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{the_base_module_name}.settings')
  django.setup()