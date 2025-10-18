# ecommerce_backend/settings.py

import os
from pathlib import Path
# import dj_database_url # Ya no es estrictamente necesario para la configuración de DB
from dotenv import load_dotenv

# ==============================================================================
# 0. CONFIGURACIÓN BÁSICA Y VARIABLES DE ENTORNO (¡CRÍTICO!)
# ==============================================================================

# Cargar variables de entorno desde .env para desarrollo local
# ¡Asegúrate de que .env NO esté en tu control de versiones (añadir a .gitignore)!
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY: ¡Debe ser una cadena larga, aleatoria y secreta!
# NUNCA hardcodees esto en producción. Siempre desde una variable de entorno.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("La variable de entorno DJANGO_SECRET_KEY no está configurada. ¡CRÍTICO!")

# DEBUG: Siempre False en producción. True solo para desarrollo.
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# ALLOWED_HOSTS: Lista de dominios/IPs que tu aplicación puede servir.
# En producción, debe contener los dominios de tu sitio.
ALLOWED_HOSTS_STR = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STR if host.strip()]
if DEBUG:
    ALLOWED_HOSTS += ['127.0.0.1', 'localhost', '0.0.0.0'] # Para desarrollo


# ==============================================================================
# 1. APLICACIONES INSTALADAS
# ==============================================================================

INSTALLED_APPS = [
    # Core Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Terceros (¡Asegúrate de instalar estas con pip! e.g., pip install djangorestframework django-cors-headers django-filter psycopg2-binary)
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django_filters",
    "csp", # Necesario para las directivas CSP avanzadas

    # App principal
    "tienda", # Tu aplicación
]


# ==============================================================================
# 2. MIDDLEWARE
# ==============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware', # Middleware para Content Security Policy
]


# ==============================================================================
# 3. CONFIGURACIÓN DE URLS Y WSGI
# ==============================================================================

ROOT_URLCONF = 'ecommerce_backend.urls'
WSGI_APPLICATION = 'ecommerce_backend.wsgi.application'


# ==============================================================================
# 4. PLANTILLAS
# ==============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'autoescape': True,
        },
    },
]


# ==============================================================================
# 5. BASE DE DATOS (AHORA CON CONFIGURACIÓN EXPLÍCITA DE POSTGRESQL)
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'ecommerce_db'),
        'USER': os.getenv('POSTGRES_USER', 'ecommerce_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'ecommerce_pass'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require' if not DEBUG else 'disable', # Obliga SSL en producción
        },
    }
}
# Advertencia si no se usa PostgreSQL en producción (aunque la config ya lo fuerza)
if not DEBUG and DATABASES['default']['ENGINE'] != 'django.db.backends.postgresql':
    raise ValueError("La configuración de la base de datos no es PostgreSQL en producción. ¡CRÍTICO!")


# ==============================================================================
# 6. AUTENTICACIÓN Y CONTRASEÑAS (SEGURIDAD CRÍTICA)
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]


# ==============================================================================
# 7. INTERNACIONALIZACIÓN
# ==============================================================================

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# 8. ARCHIVOS ESTÁTICOS (STATIC FILES) Y MEDIA
# ==============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'


# ==============================================================================
# 9. SEGURIDAD ADICIONAL (¡CONFIGURACIONES EXTREMAS!)
# ==============================================================================

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
SESSION_SAVE_EVERY_REQUEST = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_CONTENT_TYPE_NOSNIFF = True

# Content Security Policy (CSP)
# Necesitarás 'django-csp' en INSTALLED_APPS y MIDDLEWARE
# CSP_DEFAULT_SRC = ("'self'",)
# CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'") if DEBUG else ("'self'",)
# CSP_STYLE_SRC = ("'self'", "'unsafe-inline'") if DEBUG else ("'self'",)
# CSP_IMG_SRC = ("'self'", 'data:')
# CSP_FONT_SRC = ("'self'",)
# CSP_OBJECT_SRC = ("'none'",)
# CSP_BASE_URI = ("'self'",)
# CSP_FRAME_ANCESTORS = ("'self'",)
# CSP_FORM_ACTION = ("'self'",)
# CSP_CONNECT_SRC = ("'self'",)
# CSP_REPORT_URI = os.environ.get('CSP_REPORT_URI', None)

# Nueva configuración para django-csp 4.0+
CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'default-src': ("'self'",),
        'script-src': ("'self'", "'unsafe-inline'", "'unsafe-eval'"),
        'style-src': ("'self'", "'unsafe-inline'"),
        'img-src': ("'self'", 'data:'),
        'font-src': ("'self'",),
        'connect-src': ("'self'",),
        'form-action': ("'self'",),
        'frame-ancestors': ("'self'",),
        'object-src': ("'none'",),
        'base-uri': ("'self'",),
        # Si tienes otras directivas personalizadas, añádelas aquí.
        # Por ejemplo, para permitir scripts de Google Analytics:
        # 'script-src': ("'self'", "'unsafe-inline'", "'unsafe-eval'", 'https://www.googletagmanager.com', 'https://www.google-analytics.com'),
    }
}

ADMIN_URL = os.environ.get('DJANGO_ADMIN_URL', 'admin/')
LOGIN_URL = f'/{ADMIN_URL}login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# ==============================================================================
# 10. CONFIGURACIONES DE DRF Y CORS (SEGURIDAD PARA APIs)
# ==============================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
CORS_ALLOW_METHODS = [
    'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization', 'content-type',
    'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with',
]
CORS_ALLOW_CREDENTIALS = True


# ==============================================================================
# 11. REGISTRO (LOGGING)
# ==============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO' if DEBUG else 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'simple' if DEBUG else 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO' if DEBUG else 'WARNING',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'CRITICAL',
            'propagate': False,
        },
        'tienda': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

if not (BASE_DIR / 'logs').exists():
    os.makedirs(BASE_DIR / 'logs', exist_ok=True)


# ==============================================================================
# 12. OTRAS CONFIGURACIONES
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SERVER_EMAIL = os.environ.get('DJANGO_SERVER_EMAIL', 'security@yourdomain.com')
ADMINS_STR = os.environ.get('DJANGO_ADMINS', 'Admin:admin@yourdomain.com').split(';')
ADMINS = [tuple(a.split(':')) for a in ADMINS_STR if a]
MANAGERS = ADMINS

EMAIL_BACKEND = os.environ.get('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST')
EMAIL_PORT = os.environ.get('DJANGO_EMAIL_PORT', '587')
EMAIL_USE_TLS = os.environ.get('DJANGO_EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL', SERVER_EMAIL)

if not DEBUG:
    SITE_ID = 1
    TEMPLATES[0]['OPTIONS']['debug'] = False