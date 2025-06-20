from django.contrib import admin
from django.urls import path, include
# Rota para gerar token de autenticação
from rest_framework.authtoken.views import obtain_auth_token

# Importa os routers de cada app (que já têm as rotas registradas)
from cadastros.urls import router as cadastros_router
from exercicios.urls import router as exercicios_router
from planos.urls import router as planos_router
from treinos.urls import router as treinos_router

urlpatterns = [

    # Inclui as rotas da API para cada app, versionadas no prefixo /api/v1/
    path('api/v1/cadastros/', include(cadastros_router.urls)),
    path('api/v1/exercicios/', include(exercicios_router.urls)),
    path('api/v1/planos/', include(planos_router.urls)),
    path('api/v1/treinos/', include(treinos_router.urls)),

    # Admin padrão do Django
    path('admin/', admin.site.urls),

    # Login e logout via browsable API do DRF
    path('auth/', include('rest_framework.urls')),

    # Endpoint para obter token de autenticação via username e password
    path('api-token-auth/', obtain_auth_token),
]
