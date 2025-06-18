from .base import *
from decouple import Config, RepositoryEnv
import os

env_path = os.path.join(BASE_DIR, 'env/.env.development')
config = Config(RepositoryEnv(env_path))


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST', default='localhost'),
        'PORT': config('POSTGRES_PORT', default='5432'),
    }
}

