from pathlib import Path
from importlib import import_module
from django.urls import path, include
from .path import modules_path

def bind_modules_app():
    the_modules_path = Path(modules_path()).resolve()
    
    # Initialize an empty list to store installed apps
    INSTALLED_APPS = [
        # third party apps
        'rest_framework',
        'rest_framework.authtoken',
        'celery',
    ]
    
    INSTALLED_APPS.append('django_petra.project')
    INSTALLED_APPS.append('django_petra.cors')

    # Loop through each module directory
    for module_dir in the_modules_path.iterdir():
        if module_dir.is_dir():
            # Construct the path to the urls.py file in the module directory
            module_urls_path = module_dir / 'urls.py'
            
            # Get the name of the module
            module_name = module_dir.name
            
            # Check if the urls.py file exists
            if module_urls_path.exists():
                # Append the module to INSTALLED_APPS
                INSTALLED_APPS.append(f'modules.{module_name}')

    # Return the INSTALLED_APPS list
    return INSTALLED_APPS

def bind_modules_urls():
    the_modules_path = Path(modules_path()).resolve()
    
    # Initialize an empty list to store urlpatterns
    urlpatterns = []
    urlpatterns.append(path(f'hello-django-petra/', include(('django_petra.project.urls', 'django_petra.project'))))

    # Loop through each module directory
    for module_dir in the_modules_path.iterdir():
        if module_dir.is_dir():
            # Get the name of the module
            module_name = module_dir.name
            
            # Construct the path to the urls.py file in the module directory
            module_urls_path = module_dir / 'urls.py'
            
            # Check if the urls.py file exists
            if module_urls_path.exists():
                # Construct the import path for the module's urls
                module_urls = f'modules.{module_name}.urls'
                
                # Append a path to urlpatterns, including the module's urls
                urlpatterns.append(path(f'api/v1/{module_name}/', include((module_urls, module_name))))

    # Return the urlpatterns list
    return urlpatterns

def show_modules_url():
    from django_petra.router import Router, Route
    the_modules_path = Path(modules_path()).resolve()
    
    # Initialize an empty list to store urlpatterns
    the_routes = []
    # urlpatterns.append(path(f'hello-django-petra/', include(('django_petra.project.urls', 'django_petra.project'))))

    # Loop through each module directory
    for module_dir in the_modules_path.iterdir():
        if module_dir.is_dir():
            # Get the name of the module
            module_name = module_dir.name
            
            # Construct the path to the urls.py file in the module directory
            module_urls_path = module_dir / 'urls.py'
            
            # Check if the urls.py file exists
            if module_urls_path.exists():
                # Construct the import path for the module's urls
                module_urls = f'modules.{module_name}.urls'
                
                 # Dynamically import the module's urls
                urls_module = import_module(module_urls)
                
                # Get the routes from the imported module
                module_routes = getattr(urls_module, 'routes', [])
                
                generate_routes = [(route) for route in Route(module_routes).show_lists()]
                
                # Append a path to urlpatterns, including the module's urls
                the_routes.extend(generate_routes)

    # Return the urlpatterns list
    return the_routes

from django_petra.initialize import init_django_petra

def initialize():
    init_django_petra()
    


