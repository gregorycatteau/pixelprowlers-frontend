from pathlib import Path
from decouple import config
from corsheaders.defaults import default_headers

# Répertoire racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Sécurité
SECRET_KEY = config('SECRET_KEY', default='super-secret-key')

# Applications installées
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps tierces
    'rest_framework',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',
    

    # Apps internes
    'designengine',
    'blog',
    'feedback',
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Doit être en haut
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL principales
ROOT_URLCONF = 'config.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# Auth
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalisation
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# Fichiers statiques et médias
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",  # ✅ Pour Nuxt DevTools
]
CORS_ALLOW_CREDENTIALS = True

# (Optionnel) expose le header CSRF au front
from corsheaders.defaults import default_headers
CORS_EXPOSE_HEADERS = list(default_headers) + [
    'X-CSRFToken',
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    "access-control-allow-origin",
    "access-control-allow-credentials",
    "access-control-request-headers",
    "access-control-request-method",
    "origin",
    "authorization",
    "x-requested-with",
    "upgrade",  # WebSocket
    "sec-websocket-key",
]

# CKEditor : configuration de l'éditeur WYSIWYG
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Format', 'Bold', 'Italic', 'Underline', 'Blockquote'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['Image', 'Table'],
            ['RemoveFormat', 'Source'],
        ],
        'height': 400,
        'width': 'auto',
        'language': 'fr',
    }
}

