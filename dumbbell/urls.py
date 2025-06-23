# =============================================================================
# ARQUIVO: dumbbell/urls.py
# DESCRIÇÃO: Configuração das URLs principais do projeto Dumbbell Fitness
# FUNÇÃO: Define todas as rotas da aplicação, incluindo API, admin e autenticação
# =============================================================================

# Importações do Django para gerenciamento de URLs
from django.contrib import admin
from django.urls import path, include

# Importação específica para autenticação via token
# Esta view permite obter um token de autenticação usando username e password
from rest_framework.authtoken.views import obtain_auth_token

# Importa os routers de cada app (que já têm as rotas registradas)
# Cada router contém as URLs específicas de cada funcionalidade
from cadastros.urls import router as cadastros_router
from exercicios.urls import router as exercicios_router
from planos.urls import router as planos_router
from treinos.urls import router as treinos_router

# Lista principal de padrões de URL do projeto
urlpatterns = [
    # =====================================================================
    # ROTAS DA API REST - Versionada em /api/v1/
    # =====================================================================
    
    # Rotas para gerenciamento de cadastros (alunos, endereços, matrículas, cartões)
    # Endpoints: /api/v1/cadastros/alunos/, /api/v1/cadastros/endereco/, etc.
    path('api/v1/cadastros/', include(cadastros_router.urls)),
    
    # Rotas para gerenciamento de exercícios físicos
    # Endpoints: /api/v1/exercicios/
    path('api/v1/exercicios/', include(exercicios_router.urls)),
    
    # Rotas para gerenciamento de planos de treino
    # Endpoints: /api/v1/planos/, /api/v1/planos/<id>/, /api/v1/planos/auth/login/, /api/v1/planos/auth/user/
    path('api/v1/planos/', include('planos.urls')),
    
    # Rotas para gerenciamento de treinos dos alunos
    # Endpoints: /api/v1/treinos/
    path('api/v1/treinos/', include(treinos_router.urls)),

    # =====================================================================
    # ROTAS ADMINISTRATIVAS
    # =====================================================================
    
    # Interface administrativa padrão do Django
    # Acesso: /admin/ (requer superusuário)
    path('admin/', admin.site.urls),

    # =====================================================================
    # ROTAS DE AUTENTICAÇÃO
    # =====================================================================
    
    # Interface de login/logout via browsable API do DRF
    # Acesso: /auth/ (interface visual para autenticação)
    path('auth/', include('rest_framework.urls')),

    # Endpoint para obter token de autenticação via username e password
    # Método: POST
    # Dados: {"username": "usuario", "password": "senha"}
    # Retorna: {"token": "seu_token_aqui"}
    # Acesso: /api-token-auth/
    path('api-token-auth/', obtain_auth_token),
]
