"""
Define as rotas da API REST usando DefaultRouter do Django REST Framework.

Registra os ViewSets de:
- Aluno
- Matrícula
- Cartão
- Endereco: Localizada no app core

Cada registro cria automaticamente as rotas RESTful padrão (list, create, retrieve, update, delete).

O objeto 'urlpatterns' expõe todas as URLs geradas para inclusão no arquivo principal de URLs.
"""

from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import AlunoViewSet, MatriculaViewSet, CartaoViewSet
from core.views import EnderecoViewSet

router = DefaultRouter()
router.register('alunos', AlunoViewSet, basename='aluno')
router.register('matriculas', MatriculaViewSet, basename='matricula')
router.register('cartoes', CartaoViewSet, basename='cartao')
router.register('endereco', EnderecoViewSet, basename='endereco')

urlpatterns = router.urls
