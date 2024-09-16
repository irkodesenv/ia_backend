from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('KEY_SEGURANCA_PROJETO_DJANGO')

DEBUG = config('DEBUG', default=False, cast=bool)

API_OPENIA_KEY = config('API_OPENIA_IRKO')

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'accounts.apps.AccountsConfig',
    'agente.apps.AgenteConfig',
    'empresa.apps.EmpresaConfig',
    'chat.apps.ChatConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'central.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
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

WSGI_APPLICATION = 'central.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'templates/static/'

MEDIA_ROOT = BASE_DIR / 'upload/media'
MEDIA_URL = '/upload/media/'

# Determina se o cookie CSRF deve ser enviado apenas por conexões HTTPS seguras
CSRF_COOKIE_SECURE = config('COOKIE_SECURE', default=True, cast=bool)

# Define se o cookie CSRF deve ser acessível apenas pelo servidor e não deve ser acessível via JavaScript no navegador ( Permitir React )
CSRF_COOKIE_HTTPONLY = False

# Permite que cookies e credenciais sejam enviados com as solicitações entre diferentes origens (CORS).
CORS_ALLOW_CREDENTIALS = True

# Permite qualquer origem
CORS_ALLOW_ALL_ORIGINS = False  


CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',  # URL do frontend React
    'http://127.0.0.1:3000'
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # URL do frontend React
    'http://127.0.0.1:3000'
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'