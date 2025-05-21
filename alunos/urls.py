from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlunoViewSet, MatriculaViewSet, CartaoViewSet

router = DefaultRouter()
router.register('alunos', AlunoViewSet, basename='aluno')
router.register('matriculas', MatriculaViewSet, basename='matricula')
router.register('cartoes', CartaoViewSet, basename='cartao')
urlpatterns = router.urls


