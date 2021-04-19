from pathlib import Path
from typing import List, Tuple, Dict, Any

from celery.schedules import crontab
from django.utils.translation import ugettext_lazy as _
from environ import Env

env = Env()

# APPLICATION DEFINITION
# region
BASE_DIR: Path = Path(__file__).resolve().parent.parent
SECRET_KEY: str = env.str('SECRET_KEY', '*xrqclbk2v=nsg3==anvvpr@#gtx*4p4a%*dt4w8+m#n3^1)%y')
DEBUG: bool = False
ALLOWED_HOSTS: List[str] = ['*']
ROOT_URLCONF: str = 'project.urls'
WSGI_APPLICATION: str = 'project.wsgi.application'
BUILD_DIR: Path = Path(BASE_DIR, 'crm', 'templates')
# endregion

# PROJECT APPLICATIONS
# region
DJANGO_APPS: Tuple[str, ...] = (
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

REQUIREMENTS_APPS: Tuple[str, ...] = (
    'grappelli.dashboard',
    'grappelli',
    'rest_framework'
)

PROJECT_APPS: Tuple[str, ...] = (
    'crm',
)

INSTALLED_APPS: Tuple[str, ...] = (
    *DJANGO_APPS,
    *REQUIREMENTS_APPS,
    *DJANGO_APPS,
)

# endregion


# GRAPPELLI
# region
GRAPPELLI_INDEX_DASHBOARD: str = 'dashboard.CustomIndexDashboard'
# endregion


# MIDDLEWARE
# region
MIDDLEWARE: List[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# endregion

# TEMPLATES
# region
TEMPLATES: List[Dict[str, Any]] = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        Path(BASE_DIR / 'templates'),
    ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]
    }
}]
# endregion

# DATABASE
# region
DATABASES: Dict[str, Dict[str, Any]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# endregion

# PASSWORD VALIDATION AND AUTHENTICATION
# region
EMAIL_HOST_USER: str = 'info@crm.ru'
AUTHENTICATION_FAILED_ATTEMPTS_CACHE_KEY = None
AUTHENTICATION_FAILED_ATTEMPTS_CACHE_STORE_TIMEOUT: int = 1800
AUTHENTICATION_FAILED_ATTEMPTS_LIMIT: int = 10
AUTHENTICATION_BACKENDS: List[str] = [
    'crm.utils.backends.CustomModelBackend'
]
LOGIN_URL: str = '/login'

AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
# endregion

# REST FRAMEWORK
# region
REST_FRAMEWORK: Dict[str, Any] = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}
# endregion

# STATIC FILES (CSS, JAVASCRIPT, IMAGES)
# region
STATIC_URL: str = '/static/'
STATIC_ROOT: Path = Path(BASE_DIR / 'static')

MEDIA_URL: str = '/media/'
MEDIA_ROOT: Path = Path(BASE_DIR, 'media')

STATICFILES_DIRS: List[Path] = [
    Path(BASE_DIR, 'crm/static/crm/dist')
]

STATICFILES_FINDERS: List[str] = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# endregion

# INTERNATIONALIZATION
# region
LANGUAGES: List[Tuple[str, str]] = [
    ('ru', _('Russian')),
]
LANGUAGE_CODE: str = 'ru-ru'
TIME_ZONE: str = 'Europe/Moscow'
USE_I18N: bool = True
USE_L10N: bool = True
USE_TZ: bool = True
# endregion

# CELERY
# region
CELERY_BROKER_HOST: str = env.str('CELERY_BROKER_HOST', 'localhost')
CELERY_BROKER_PORT: int = env.int('CELERY_BROKER_PORT', '6379')
BROKER_URL: str = f'redis://{CELERY_BROKER_HOST}:{CELERY_BROKER_PORT}/2'
RESULT_BACKEND: str = f'redis://{CELERY_BROKER_HOST}:{CELERY_BROKER_PORT}/3'

CELERY_TASK_SERIALIZER: str = 'json'
CELERY_RESULT_SERIALIZER: str = 'json'
CELERY_ACCEPT_CONTENT: List[str] = ['json']
CELERY_TIMEZONE: str = env.str('CELERY_TIMEZONE', TIME_ZONE)
CELERY_ENABLE_UTC: bool = True

CELERY_IMPORTS: Tuple[str, ...] = (
    'crm.tasks',
)
CELERY_BEAT_SCHEDULE: Dict[str, Dict[str, Any]] = {
    'whitelist_parsing': {
        'task': 'crm.tasks.whitelist_parsing',
        'schedule': crontab(),
    },
}
# endregion
