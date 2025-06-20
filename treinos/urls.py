# Importa funções para definir rotas e roteador padrão do DRF
from django.urls import path
from rest_framework.routers import DefaultRouter

# Importa o ViewSet responsável por Treinos
from .views import TreinoViewSet

# Cria instância do DefaultRouter para registro automático de rotas RESTful
router = DefaultRouter()

# Registra o TreinoViewSet na rota raiz deste roteador
router.register('', TreinoViewSet)

# Expõe as URLs geradas pelo roteador para inclusão no arquivo principal de URLs
urlpatterns = router.urls
