# Importa funções para definir URLs e incluir outras rotas
from django.urls import path, include

# Importa roteador padrão do DRF para registrar ViewSets automaticamente
from rest_framework.routers import DefaultRouter

# Importa ViewSet do app cadastros para manipular alunos
from cadastros.views import AlunoViewSet

# Importa os ViewSets relacionados a planos, modalidades e suas relações
from .views import PlanoViewSet, ModalidadeViewSet, PlanoModalidadeViewSet

# Cria uma instância do roteador padrão
router = DefaultRouter()

# Registra o ViewSet do Plano na rota raiz deste router
router.register('', PlanoViewSet, basename='plano')

# Registra o ViewSet da Modalidade na rota 'modalidades'
router.register('modalidades', ModalidadeViewSet, basename='modalidade')

# Registra o ViewSet que gerencia o relacionamento PlanoModalidade na rota 'planomodalidades'
router.register('planomodalidades', PlanoModalidadeViewSet,
                basename='planomodalidade')

# Expõe as URLs geradas pelo router para serem incluídas no projeto principal
urlpatterns = router.urls
