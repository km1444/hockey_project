import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'dr=o^v+7-*f*n&uk_(!gto0#*q%^ucv6&l_qikog&mu-w4ewzo'

DEBUG = True

ALLOWED_HOSTS = [
    '158.160.41.209',
    '127.0.0.1',
    'localhost',
    'testserver',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rating.apps.RatingConfig',
    'debug_toolbar',
    'core.apps.CoreConfig',
    'api.apps.ApiConfig',
    'users.apps.UsersConfig',
    'sorl.thumbnail',
    'miscellaneous.apps.MiscellaneousConfig',
    'goalkeeper_app.apps.GoalkeeperAppConfig',
    'coach_app.apps.CoachAppConfig',
    'liga2_seasons_app.apps.Liga2SeasonsAppConfig',
    'liga2_teams_app.apps.Liga2TeamsAppConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'hockey.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.year.year',
                'core.context_processors.all_seasons.all_seasons',
                'core.context_processors.all_team.all_team',
                'core.context_processors.all_team_liga2.all_team',
            ],
        },
    },
]

WSGI_APPLICATION = 'hockey.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
        # 'default': {
        #     'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        #     'NAME': os.getenv('DB_NAME'),
        #     'USER': os.getenv('POSTGRES_USER'),
        #     'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        #     'HOST': os.getenv('DB_HOST'),
        #     'PORT': os.getenv('DB_PORT')
        # }
    }
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

INTERNAL_IPS = [
    '127.0.0.1',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'rating:index'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
