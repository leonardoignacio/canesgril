"""
Django settings for canesgril project.

Generated by 'django-admin startproject' using Django 5.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url #Se for converter URL em dicionário
load_dotenv() # Vaiaveis de ambiente do arquivo .env


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#DEBUG=True
#ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['.railway.app', 'canesgril-production.up.railway.app', 'localhost', '104.18.11.246', '66.33.22.120', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'funcionario',
    'churras',
    'usuarios',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Adicione esta linha
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'canesgril.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'canesgril.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
#DATABASES = {'default': dj_database_url.parse(os.environ.get('DATABASE_URL'), conn_max_age=600, ssl_require=True,)}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('dbname', 'postgres'),
        'USER': os.environ.get('user', 'postgres'),
        'PASSWORD': os.environ.get('password'),
        'HOST': os.environ.get('host'),
        'PORT': os.environ.get('port'),
        'OPTIONS': {
            'sslmode': 'require',
        },
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

# A URL onde os arquivos estáticos serão acessíveis no navegador
STATIC_URL = '/static/'
# O diretório onde 'collectstatic' junta os arquivos estáticos na produção.
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Diretórios adicionais onde o Django vai procurar por arquivos estáticos
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # Mantido, útil para estrutura de projeto.
# Whitenoise é a escolha ideal para Railway.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Configurações do Supabase Storage via django-storages ---
# Variáveis de ambiente que serão lidas do ambiente do Railway.
'''AWS_S3_ENDPOINT_URL = os.environ.get('SUPABASE_STORAGE_URL')
AWS_ACCESS_KEY_ID = os.environ.get('SUPABASE_STORAGE_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('SUPABASE_STORAGE_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('SUPABASE_STORAGE_BUCKET')
AWS_DEFAULT_ACL = 'public-read' # Se seu bucket é público no Supabase
AWS_S3_FILE_OVERWRITE = False # Não sobrescrever arquivos com o mesmo nome
AWS_QUERYSTRING_AUTH = False # Evita adicionar credenciais na URL da imagem
'''

AWS_S3_ENDPOINT_URL = os.environ.get('SUPABASE_STORAGE_URL')
AWS_ACCESS_KEY_ID = os.environ.get('SUPABASE_STORAGE_ACCESS_KEY') # Onde o "Access key ID" vai
AWS_SECRET_ACCESS_KEY = os.environ.get('SUPABASE_STORAGE_SECRET_KEY') # Onde o "Secret access key" vai
AWS_STORAGE_BUCKET_NAME = os.environ.get('SUPABASE_STORAGE_BUCKET')

AWS_DEFAULT_ACL = 'public-read' # Se seu bucket é público no Supabase
AWS_S3_FILE_OVERWRITE = False # Não sobrescrever arquivos com o mesmo nome
AWS_QUERYSTRING_AUTH = False # Importante: Não adiciona credenciais na URL da imagem, bom para CDN.


AWS_LOCATION = 'media-uploads'


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'




# --- Define o Backend de Armazenamento Padrão crucial para usar o Supabase Storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Força o uso de cookies CSRF apenas em conexões HTTPS
CSRF_COOKIE_SECURE = True

# Força o uso de cookies de sessão apenas em conexões HTTPS
SESSION_COOKIE_SECURE = True

# Adicione o domínio base do Railway e qualquer domínio personalizado
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',             # Para cobrir seu domínio Railway padrão
    'https://canesgril-production.up.railway.app', # O domínio exato do seu ambiente de produção
    # 'https://seusitepersonalizado.com',  # Se você tiver um domínio personalizado
    # 'https://www.seusitepersonalizado.com', # E a versão com www
]

