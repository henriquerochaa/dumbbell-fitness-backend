# =============================================================================
# ARQUIVO: dumbbell/settings.py
# DESCRIÇÃO: Configurações principais do projeto Dumbbell Fitness
# FUNÇÃO: Define todas as configurações do Django, banco de dados, apps, etc.
# =============================================================================

# Importações necessárias para o projeto
import os
from pathlib import Path
from dotenv import load_dotenv  # Lê variáveis de ambiente do arquivo .env
import dj_database_url          # Facilita a configuração do banco via URL

# Carrega as variáveis do arquivo .env para o ambiente
# Isso permite configurar SECRET_KEY, DATABASE_URL, etc. sem expor no código
load_dotenv()

# =============================================================================
# CONFIGURAÇÕES BÁSICAS DO DJANGO
# =============================================================================

# Diretório base do projeto (2 níveis acima desse arquivo settings.py)
# Usado para construir caminhos absolutos para outros arquivos
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta do Django, pega do .env (não exponha no código!)
# Esta chave é usada para criptografia de sessões, tokens, etc.
SECRET_KEY = os.getenv('SECRET_KEY')

# Debug modo: True ou False conforme a variável .env (padrão True se não setada)
# Em produção deve ser False para segurança
DEBUG = True

# Hosts permitidos — aqui tá liberado geral com '*', cuidado em produção!
# Lista de domínios que podem acessar a aplicação
ALLOWED_HOSTS = ['*']

# =============================================================================
# APPS INSTALADOS
# =============================================================================

# Apps instalados no projeto — Django + libs + apps próprios
INSTALLED_APPS = [
    # Apps padrão do Django
    'django.contrib.admin',          # Interface administrativa
    'django.contrib.auth',           # Sistema de autenticação e autorização
    'django.contrib.contenttypes',   # Framework para tipos de conteúdo genérico
    'django.contrib.sessions',       # Gerenciamento de sessões
    'django.contrib.messages',       # Sistema de mensagens flash
    'django.contrib.staticfiles',    # Gerenciamento de arquivos estáticos
    
    # Apps de terceiros
    'django_filters',                # Filtros avançados para Django REST Framework
    'corsheaders',                   # CORS para permitir requisições de outros domínios
    'rest_framework',                # Django REST Framework — API REST
    'rest_framework.authtoken',      # Autenticação por token no DRF
    
    # Apps customizados do projeto
    'core',                         # Funcionalidades compartilhadas (endereços, etc.)
    'cadastros',                    # Gerenciamento de alunos, matrículas, cartões
    'exercicios',                   # Cadastro e controle de exercícios físicos
    'planos',                      # Planos de treino e modalidades
    'treinos'                      # Criação e controle de treinos dos alunos
]

# =============================================================================
# MIDDLEWARE
# =============================================================================

# Middleware — camadas que processam requests/responses
# São executados na ordem definida aqui
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Middleware CORS (deve vir primeiro)
    'django.middleware.security.SecurityMiddleware',         # Segurança básica do Django
    'whitenoise.middleware.WhiteNoiseMiddleware',            # Serve arquivos estáticos em produção
    'django.contrib.sessions.middleware.SessionMiddleware',  # Controla sessões de usuário
    'django.middleware.common.CommonMiddleware',             # Middleware comum (normaliza URLs)
    'django.middleware.csrf.CsrfViewMiddleware',             # Proteção contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Autenticação do usuário
    'django.contrib.messages.middleware.MessageMiddleware',  # Mensagens de feedback
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Proteção contra clickjacking
]

# =============================================================================
# CONFIGURAÇÕES DE TEMPLATES E WSGI
# =============================================================================

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

# =============================================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# =============================================================================

# Configuração do banco de dados via URL no .env, com conexão persistente e SSL
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),  # URL do banco no .env
        conn_max_age=600,                   # Mantém conexão aberta por 10 minutos
        ssl_require=True,                   # Exige conexão segura (SSL)
    )
}

# =============================================================================
# VALIDAÇÃO DE SENHAS
# =============================================================================

# Validadores de senha para segurança dos usuários
AUTH_PASSWORD_VALIDATORS = [
    # Senha diferente de atributos do usuário (nome, email, etc.)
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    # Comprimento mínimo da senha
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    # Senhas comuns proibidas (123456, password, etc.)
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    # Proíbe senhas que são só números
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =============================================================================
# INTERNACIONALIZAÇÃO E FUSO HORÁRIO
# =============================================================================

# Configurações de idioma e fuso horário
LANGUAGE_CODE = 'pt-br'               # Português Brasil
TIME_ZONE = 'America/Sao_Paulo'      # Fuso horário de São Paulo
USE_I18N = True                      # Suporte a tradução (internacionalização)
USE_TZ = True                        # Usa timezone aware (datas com fuso horário)

# =============================================================================
# ARQUIVOS ESTÁTICOS E MÍDIA
# =============================================================================

# Configuração de arquivos estáticos (CSS, JS, imagens)
STATIC_URL = '/static/'  # URL base para estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Pasta onde estáticos são coletados na produção

# Configuração de arquivos de mídia (upload de usuários, fotos, etc)
MEDIA_URL = '/media/'  # URL base para mídias
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Pasta onde arquivos de mídia ficam salvos

# Armazenamento de arquivos estáticos otimizado (compressão e cache)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =============================================================================
# CONFIGURAÇÕES GERAIS
# =============================================================================

# Tipo padrão de campo para chaves primárias (PK) novas
# BigAutoField é para PK grande (recomendado para projetos grandes)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# DJANGO REST FRAMEWORK (DRF)
# =============================================================================

# Configuração do Django REST Framework (DRF)
REST_FRAMEWORK = {
    # Como a autenticação acontece
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',    # Token no header Authorization
        'rest_framework.authentication.SessionAuthentication',  # Sessão do Django (para admin)
    ),
    # Permissões padrão para acessar a API
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',           # Exige usuário autenticado
        'rest_framework.permissions.DjangoModelPermissions',    # Respeita permissões dos models Django
    )
}

# =============================================================================
# CONFIGURAÇÕES CORS
# =============================================================================

# Configuração CORS (Cross-Origin Resource Sharing)
# Permite que qualquer frontend na web faça requisições para a API
# ⚠️ ATENÇÃO: Esta configuração permite acesso de qualquer origem
# Use apenas se você realmente precisa de acesso público à API

# Permite requisições de qualquer origem (domínio)
CORS_ALLOW_ALL_ORIGINS = True

# Configurações adicionais de CORS para maior compatibilidade
CORS_ALLOW_CREDENTIALS = True  # Permite envio de cookies e headers de autenticação

# Headers permitidos nas requisições CORS
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Métodos HTTP permitidos nas requisições CORS
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Configuração alternativa (mais restritiva) - descomente se quiser limitar origens específicas
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000',      # Frontend rodando localmente
#     'https://seu-dominio.com',    # Seu domínio de produção
#     'https://www.seu-dominio.com', # Versão www do seu domínio
# ]
