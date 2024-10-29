from django_petra.initialize.initialize import (
  init_cors_middleware,
  init_all_modules,
  init_module_urls,
)

def init_django_petra():
  init_cors_middleware()
  init_all_modules()
  init_module_urls()