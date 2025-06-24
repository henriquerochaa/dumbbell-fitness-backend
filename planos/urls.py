# Importa funções para definir URLs e incluir outras rotas
from django.urls import path, include

# Importa roteador padrão do DRF para registrar ViewSets automaticamente
from rest_framework.routers import DefaultRouter

# Importa ViewSet do app cadastros para manipular alunos
from cadastros.views import AlunoViewSet

# Importa os ViewSets relacionados a planos, modalidades e suas relações
from .views import (
    PlanoViewSet, 
    ModalidadeViewSet, 
    PlanoModalidadeViewSet,
    planos_list,
    plano_detail,
    CustomAuthToken,
    user_info
)

# Cria uma instância do roteador padrão
router = DefaultRouter()

# Registra o ViewSet do Plano na rota raiz deste router
router.register('', PlanoViewSet, basename='plano')

# Registra o ViewSet da Modalidade na rota 'modalidades'
router.register('modalidades', ModalidadeViewSet, basename='modalidade')

# Registra o ViewSet que gerencia o relacionamento PlanoModalidade na rota 'planomodalidades'
router.register('planomodalidades', PlanoModalidadeViewSet,
                basename='planomodalidade')

# Define as URLs específicas para as views customizadas
urlpatterns = [
    # Rotas para autenticação
    path('auth/login/', CustomAuthToken.as_view(), name='auth-login'),  # Login com token
    path('auth/user/', user_info, name='user-info'),  # Informações do usuário logado
    
    # Rotas customizadas para planos (mais específicas)
    path('list/', planos_list, name='planos-list'),  # Lista todos os planos (sem auth)
    path('detail/<int:pk>/', plano_detail, name='plano-detail'),  # Detalhes de um plano (com auth)
    
    # Inclui as rotas do router (ViewSets) - deve vir por último
    path('', include(router.urls)),
]
