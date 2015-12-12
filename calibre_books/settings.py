import os
import dj_database_url


def env_list(variable, default=''):
    return os.environ.get(variable, default).split()


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = bool(os.environ.get('DEBUG', False))

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = env_list('ALLOWED_HOSTS')

INTERNAL_IPS = env_list('INTERNAL_IPS', '127.0.0.1')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'calibre_books.core',
    'calibre_books.calibre',

    # External apps
    'bootstrap3',
    'raven.contrib.django.raven_compat',
    'haystack',
    'social.apps.django_app.default',
    'django_gravatar',
]

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'sslify.middleware.SSLifyMiddleware',
    'calibre_books.core.middleware.SocialAuthExceptionMiddleware',
]

if DEBUG:
    MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware']

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "social.apps.django_app.context_processors.backends",
    "social.apps.django_app.context_processors.login_redirect",
    "calibre_books.core.context_processors.github_corner_url",
    "calibre_books.core.context_processors.google_analytics",
)

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'templates')
]

ROOT_URLCONF = 'calibre_books.urls'

WSGI_APPLICATION = 'calibre_books.wsgi.application'


SQLITE_DB_URL = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

DATABASES = {
    'default': dj_database_url.config(default=SQLITE_DB_URL),
    'calibre': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'metadata.db'),
    }
}

DATABASE_ROUTERS = ['calibre_books.calibre.db_router.DbRouter']

LOGIN_URL = '/login'
LOGIN_ERROR_URL = LOGIN_URL
LOGIN_REDIRECT_URL = '/'

DEBUG_TOOLBAR_PATCH_SETTINGS = False

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'calibre_books', 'static'),
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SSLIFY_DISABLE = bool(os.environ.get('SSLIFY_DISABLE', False))

DROPBOX_CONSUMER_KEY = os.environ.get('DROPBOX_CONSUMER_KEY')
DROPBOX_CONSUMER_SECRET = os.environ.get('DROPBOX_CONSUMER_SECRET')
DROPBOX_ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN')
DROPBOX_ACCESS_TOKEN_SECRET = os.environ.get('DROPBOX_ACCESS_TOKEN_SECRET')
DROPBOX_ACCESS_TYPE = 'dropbox'
DROPBOX_CALIBRE_DIR = os.environ.get('DROPBOX_CALIBRE_DIR', 'CalibreLibrary')

SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('GOOGLE_SECRET')
SOCIAL_AUTH_GOOGLE_OAUTH2_USE_DEPRECATED_API = True

SOCIAL_AUTH_GITHUB_ORG_KEY = os.environ.get('GITHUB_KEY')
SOCIAL_AUTH_GITHUB_ORG_SECRET = os.environ.get('GITHUB_SECRET')
SOCIAL_AUTH_GITHUB_ORG_SCOPE = ['user:email', 'read:org']

SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = env_list('GOOGLE_WHITELISTED_DOMAINS')
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = env_list('GOOGLE_WHITELISTED_EMAILS')
SOCIAL_AUTH_GITHUB_ORG_NAME = os.environ.get('GITHUB_ORG_NAME', '')

AUTHENTICATION_BACKENDS = []

if SOCIAL_AUTH_GOOGLE_OAUTH2_KEY:
    AUTHENTICATION_BACKENDS += ['social.backends.google.GoogleOAuth2']

if SOCIAL_AUTH_GITHUB_ORG_KEY:
    AUTHENTICATION_BACKENDS += ['social.backends.github.GithubOrganizationOAuth2']

AUTHENTICATION_BACKENDS += ['django.contrib.auth.backends.ModelBackend']

RAVEN_CONFIG = {'dsn': os.environ.get('SENTRY_DSN', '')}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry']
    },
    'handlers': {
        'sentry': {
            'level': 'INFO',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'calibre_books': {
            'level': 'INFO',
            'handlers': ['sentry'],
            'propagate': False
        }
    }
}

MEMCACHE_SERVERS = os.environ.get('MEMCACHE_SERVERS')

if MEMCACHE_SERVERS:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': MEMCACHE_SERVERS,
        }
    }

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}

GITHUB_CORNER_URL = os.environ.get('GITHUB_CORNER_URL')

GOOGLE_ANALYTICS = os.environ.get('GOOGLE_ANALYTICS')

DEFAULT_BOOKSHELF = os.environ.get('DEFAULT_BOOKSHELF')

# :address@domain.com: bookshelf:email@address.com bookshelf2:@domain.com
BOOKSHELVES_USERS = env_list('BOOKSHELVES_USERS')

PAGINATE_BY = int(os.environ.get('PAGINATE_BY', 54))
