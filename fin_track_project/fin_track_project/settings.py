import os
import sys
from decouple import config
from datetime import timedelta
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIR = os.path.join(BASE_DIR, 'apps') 
DB_DIR = BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, APPS_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Lista de hosts permitidos
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Configuração para CSRF e Cloudflare Tunnel
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://localhost:8000', cast=lambda v: [s.strip() for s in v.split(',')])

# Configurar X-Forwarded-For para confiar no Cloudflare
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
TRUST_X_FORWARDED_HOST = True


# Application definition

INSTALLED_APPS = [
    'user.apps.UserConfig',
    'accounts.apps.AccountsConfig',
    'transactions.apps.TransactionsConfig',
    'categories.apps.CategoriesConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files em produção
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuração do DRF e JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Configurando o User customizado
AUTH_USER_MODEL = 'user.Admin'

ROOT_URLCONF = 'fin_track_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fin_track_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Usar PostgreSQL se as variáveis estiverem definidas no .env
DB_ENGINE = config('DB_ENGINE', default='django.db.backends.sqlite3')
DB_NAME = config('DB_NAME', default=str(DB_DIR / 'db.sqlite3'))

if DB_ENGINE == 'django.db.backends.postgresql':
    # PostgreSQL - Produção/Desenvolvimento
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': DB_NAME,
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT', cast=int),
            'OPTIONS': {
                'sslmode': 'require',
            },
            'default': dj_database_url.parse(
                config('DATABASE_URL'),
                conn_max_age=600,
                ssl_require=True
            )
        }
    }
else:
    # SQLite - Desenvolvimento padrão
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(DB_DIR / 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Produção: pasta de saída
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Desenvolvimento: arquivos-fonte

# WhiteNoise - Serve static files com cache e compressão
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' if not DEBUG else 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

## Envio de e-mail homologação.
#EMAIL_HOST = config('EMAIL_HOST_HOMO')
#EMAIL_PORT = config('EMAIL_PORT_HOMO', cast=int)
#EMAIL_BACKEND = config('EMAIL_BACKEND_HOMO')
#DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL_HOMO')

## Envio de e-mail para produção (descomente para usar).
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

THOUSAND_SEPARATOR='.',
USE_THOUSAND_SEPARATOR=True

# A sessão do usuário expira após 2 semanas (em segundos)
SESSION_COOKIE_AGE = 1209600 
# Se True, desloga o usuário imediatamente assim que ele fechar o navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Verificar se está em modo produção (DEBUG=False)
if not DEBUG:
    # HTTPS e Cookies Seguros
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Segurança adicional
    SECURE_HSTS_SECONDS = 31536000  # 1 ano
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Cabeçalhos de segurança
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_SECURITY_POLICY = {
        "default-src": ("'self'",),
    }
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False