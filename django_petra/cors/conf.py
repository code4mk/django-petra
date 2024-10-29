import importlib
from drf_friend.path import base_module_name

the_base_module_name = base_module_name()

# Import CORS settings dynamically
cors_module = importlib.import_module(f"{the_base_module_name}.friend_config.cors")
ALLOWED_METHODS = cors_module.ALLOWED_METHODS
ALLOWED_ORIGINS = cors_module.ALLOWED_ORIGINS
ALLOWED_ORIGINS_PATTERNS = cors_module.ALLOWED_ORIGINS_PATTERNS
ALLOWED_HEADERS = cors_module.ALLOWED_HEADERS
EXPOSED_HEADERS = cors_module.EXPOSED_HEADERS
MAX_AGE = cors_module.MAX_AGE
SUPPORTS_CREDENTIALS = cors_module.SUPPORTS_CREDENTIALS
CORS_ALLOW_ALL_ORIGINS = cors_module.CORS_ALLOW_ALL_ORIGINS

class Settings:
    """
    Shadow Django's settings with a little logic
    """

    @property
    def CORS_ALLOW_HEADERS(self):
        return ALLOWED_HEADERS

    @property
    def CORS_ALLOW_METHODS(self):
        return ALLOWED_METHODS

    @property
    def CORS_ALLOW_CREDENTIALS(self):
        return SUPPORTS_CREDENTIALS

    @property
    def CORS_ALLOW_PRIVATE_NETWORK(self):
        return False

    @property
    def CORS_PREFLIGHT_MAX_AGE(self):
        return MAX_AGE

    @property
    def CORS_ALLOW_ALL_ORIGINS(self):
        return CORS_ALLOW_ALL_ORIGINS

    @property
    def CORS_ALLOWED_ORIGINS(self):
        return tuple(ALLOWED_ORIGINS)

    @property
    def CORS_ALLOWED_ORIGIN_REGEXES(self):
        return ALLOWED_ORIGINS_PATTERNS

    @property
    def CORS_EXPOSE_HEADERS(self):
        return EXPOSED_HEADERS

    @property
    def CORS_URLS_REGEX(self):
        return r"^.*$"

conf = Settings()
