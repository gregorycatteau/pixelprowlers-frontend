from .base import *
from decouple import Config, RepositoryEnv
import os

env_path = os.path.join(BASE_DIR, 'env/.env.test')
print(f"Chargement de : {env_path}")
config = Config(RepositoryEnv(env_path))

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT'),
    }
}

