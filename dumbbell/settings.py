import os
from pathlib import Path
from dotenv import load_dotenv  # Lê variáveis de ambiente do arquivo .env
import dj_database_url          # Facilita a configuração do banco via URL

load_dotenv()  # Carrega as variáveis do .env para o ambiente

# Diretório base do projeto (2 níveis acima desse arquivo settings.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta do Django, pega do .env (não exponha no código!)
SECRET_KEY = os.getenv('SECRET_KEY')

# Debug modo: True ou False conforme a variável .env (padrão True se não setada)
DEBUG = True

# Hosts permitidos — aqui tá liberado geral com '*', cuidado em produção!
ALLOWED_HOSTS = ['*']

# Apps instalados no projeto — Django + libs + apps próprios
INSTALLED_APPS = [
    'django.contrib.admin',          # Admin site padrão
    'django.contrib.auth',           # Sistema de autenticação
    'django.contrib.contenttypes',   # Conteúdo genérico do Django
    'django.contrib.sessions',       # Gerenciamento de sessões
    'django.contrib.messages',       # Sistema de mensagens
    'django.contrib.staticfiles',    # Gerenciamento de arquivos estáticos
    'django_filters',                # Filtros para Django REST Framework
    'corsheaders',                   # CORS para permitir requisições de outros domínios
    'rest_framework',                # DRF — API REST
    'rest_framework.authtoken',      # Autenticação por token no DRF
    'core',                         # App custom do projeto
    'cadastros',                    # Outro app custom
    'exercicios',                   # Outro app custom
    'planos',                      # Outro app custom
    'treinos'                      # Outro app custom
]

# Middleware — camadas que processam requests/responses
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Middleware CORS
    'django.middleware.security.SecurityMiddleware',         # Segurança básica
    # Serve arquivos estáticos em produção
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Controla sessões
    # Middleware comum (ex: normaliza URLs)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',             # Proteção CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Autenticação do usuário
    'django.contrib.messages.middleware.MessageMiddleware',  # Mensagens de feedback
    # Proteção contra clickjacking
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Arquivo principal de rotas do projeto
ROOT_URLCONF = 'dumbbell.urls'

# Configuração dos templates Django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],           # Pastas extras para templates, vazio no seu caso
        'APP_DIRS': True,    # Busca templates dentro dos apps
        'OPTIONS': {
            'context_processors': [  # Variáveis que ficam disponíveis nos templates
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Ponto de entrada WSGI para deploy (servidor)
WSGI_APPLICATION = 'dumbbell.wsgi.application'

# Configuração do banco de dados via URL no .env, com conexão persistente e SSL
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),  # URL do banco no .env
        conn_max_age=600,                   # Mantém conexão aberta por 10 minutos
        ssl_require=True,                   # Exige conexão segura
    )
}

# Validadores de senha para segurança dos usuários
AUTH_PASSWORD_VALIDATORS = [
    # Senha diferente de atributos do usuário
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    # Comprimento mínimo
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    # Senhas comuns proibidas
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    # Proíbe só números
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização e fuso horário
LANGUAGE_CODE = 'pt-br'               # Português Brasil
TIME_ZONE = 'America/Sao_Paulo'      # Fuso horário de São Paulo
USE_I18N = True                      # Suporte a tradução
USE_TZ = True                        # Usa timezone aware

# Configuração de arquivos estáticos (CSS, JS, imagens)
# URL base para estáticos
STATIC_URL = '/static/'
# Pasta onde estáticos são coletados na produção
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuração de arquivos de mídia (upload de usuários, fotos, etc)
# URL base para mídias
MEDIA_URL = '/media/'
# Pasta onde arquivos de mídia ficam salvos
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Armazenamento de arquivos estáticos otimizado (compressão e cache)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Tipo padrão de campo para chaves primárias (PK) novas — BigAutoField é para PK grande
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração do Django REST Framework (DRF)
REST_FRAMEWORK = {
    # Como a autenticação acontece
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',    # Token no header
        'rest_framework.authentication.SessionAuthentication',  # Sessão do Django
    ),
    # Permissões padrão para acessar a API
    'DEFAULT_PERMISSION_CLASSES': (
        # Exige usuário autenticado
        'rest_framework.permissions.IsAuthenticated',
        # Respeita permissões dos models Django
        'rest_framework.permissions.DjangoModelPermissions',
    )
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]
