# =============================================================================
# ARQUIVO: cadastros/urls.py
# DESCRIÇÃO: Configuração de URLs para o app cadastros do projeto Dumbbell Fitness
# FUNÇÃO: Define as rotas da API REST para alunos, matrículas, cartões e endereços
# =============================================================================

"""
Define as rotas da API REST usando DefaultRouter do Django REST Framework.

Este arquivo configura automaticamente todas as URLs RESTful para os ViewSets
definidos no app cadastros. O DefaultRouter gera automaticamente as seguintes
rotas para cada ViewSet:

- GET / - Lista todos os recursos
- POST / - Cria novo recurso
- GET /{id}/ - Obtém recurso específico
- PUT /{id}/ - Atualiza recurso específico
- PATCH /{id}/ - Atualiza parcialmente recurso específico
- DELETE /{id}/ - Remove recurso específico

ViewSets registrados:
- AlunoViewSet: gerenciamento de alunos
- MatriculaViewSet: gerenciamento de matrículas
- CartaoViewSet: gerenciamento de cartões
- EnderecoViewSet: gerenciamento de endereços (do app core)

O objeto 'urlpatterns' expõe todas as URLs geradas para inclusão no arquivo principal de URLs.
"""

# Importa o DefaultRouter do DRF para gerar URLs automaticamente
from rest_framework.routers import DefaultRouter, SimpleRouter

# Importa os ViewSets definidos neste app
from .views import AlunoViewSet, MatriculaViewSet, CartaoViewSet

# Importa o ViewSet de endereço do app core
from core.views import EnderecoViewSet

# Cria uma instância do DefaultRouter
# O DefaultRouter gera automaticamente todas as URLs RESTful
router = DefaultRouter()

# Registra os ViewSets no router
# Cada registro cria automaticamente as rotas RESTful padrão
# O parâmetro 'basename' é usado para gerar nomes únicos para as URLs

# ViewSet para gerenciamento de alunos
# URLs geradas: /api/v1/cadastros/alunos/
router.register('alunos', AlunoViewSet, basename='aluno')

# ViewSet para gerenciamento de matrículas
# URLs geradas: /api/v1/cadastros/matriculas/
router.register('matriculas', MatriculaViewSet, basename='matricula')

# ViewSet para gerenciamento de cartões
# URLs geradas: /api/v1/cadastros/cartoes/
router.register('cartoes', CartaoViewSet, basename='cartao')

# ViewSet para gerenciamento de endereços (do app core)
# URLs geradas: /api/v1/cadastros/endereco/
router.register('endereco', EnderecoViewSet, basename='endereco')

# Lista de padrões de URL gerados pelo router
# Esta lista é incluída no arquivo principal de URLs do projeto
urlpatterns = router.urls
