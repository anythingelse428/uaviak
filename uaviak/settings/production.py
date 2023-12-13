from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "PdSgVkYp3s6v9y$B&E)H@McQfThWmZq4t7w!z%C*F-JaNdRgUkXn2r5u8x/A?D(G"
# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["10.173.73.115", "uaviak.ru"]
CSRF_TRUSTED_ORIGINS = [
    "https://uaviak.ru", "http://uaviak.ru",
    "https://10.173.73.115", "http://10.173.73.115"
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'uaviak',
        'USER': 'postgres',
        'PASSWORD': 'ENIfmXDcOtb5',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

try:
    from .local import *
except ImportError:
    pass
