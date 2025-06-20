# Importa o DefaultRouter do DRF para registrar rotas automaticamente com base nos ViewSets
from rest_framework.routers import DefaultRouter

# Importa o ViewSet que controla as operações CRUD para o modelo Exercicio
from .views import ExercicioViewSet

# Cria uma instância do roteador padrão do DRF
router = DefaultRouter()

# Registra o ExercicioViewSet na rota raiz do router (''), ou seja, '/exercicios/' por onde for incluído
router.register('', ExercicioViewSet)

# Expõe as URLs geradas pelo router para inclusão no arquivo principal de URLs
urlpatterns = router.urls
