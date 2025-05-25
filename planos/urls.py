from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cadastros.views import AlunoViewSet
from .views import PlanoViewSet, ModalidadeViewSet, PlanoModalidadeViewSet


router = DefaultRouter()
router.register('', PlanoViewSet, basename='plano')
router.register('modalidades', ModalidadeViewSet, basename='modalidade')
router.register('planomodalidades', PlanoModalidadeViewSet, basename='planomodalidade')

urlpatterns = router.urls