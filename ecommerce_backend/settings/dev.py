from .base import *

DEBUG = True
ALLOWED_HOSTS += ['127.0.0.1', 'localhost', '0.0.0.0']

SECURE_SSL_REDIRECT = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES['default']['OPTIONS']['sslmode'] = 'disable'
