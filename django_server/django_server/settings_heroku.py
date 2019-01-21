
# Settings for Heroku.

# Import base settings
from .settings import *
from decouple import config
import dj_database_url

ALLOWED_HOSTS = ['0.0.0.0',
                 'ys-mark-hearthstone.herokuapp.com',]

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'))
}