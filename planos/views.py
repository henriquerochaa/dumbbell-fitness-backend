# Importa classes para views genéricas e viewsets do DRF
from rest_framework import generics, viewsets

# Importa os modelos que serão manipulados nas views
from .models import Plano, Modalidade, PlanoModalidade

# Importa os serializers responsáveis pela conversão dos dados
from .serializers import PlanoSerializer, ModalidadeSerializer, PlanoModalidadeSerializer


class PlanoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD no modelo Plano.

    Permite criar, listar, atualizar e deletar registros de planos.
    """
    queryset = Plano.objects.all().order_by('id')
    serializer_class = PlanoSerializer


class ModalidadeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD no modelo Modalidade.

    Permite criar, listar, atualizar e deletar registros de modalidades.
    """
    queryset = Modalidade.objects.all().order_by('id')
    serializer_class = ModalidadeSerializer


class PlanoModalidadeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD no modelo PlanoModalidade.

    Permite criar, listar, atualizar e deletar registros que relacionam planos e modalidades.
    """
    queryset = PlanoModalidade.objects.all().order_by('id')
    serializer_class = PlanoModalidadeSerializer
