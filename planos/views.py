from rest_framework import generics, viewsets

from .models import Plano, Modalidade, PlanoModalidade
from .serializers import PlanoSerializer, ModalidadeSerializer, PlanoModalidadeSerializer


class PlanoViewSet(viewsets.ModelViewSet):
    """
    Cria, Lista, Atualiza e Deleta os dados de plano
    """
    queryset = Plano.objects.all()
    serializer_class = PlanoSerializer


class ModalidadeViewSet(viewsets.ModelViewSet):
    """
    Cria, Lista, Atualiza e Deleta os dados de modalidade
    """
    queryset = Modalidade.objects.all()
    serializer_class = ModalidadeSerializer

class PlanoModalidadeViewSet(viewsets.ModelViewSet):
    """
    Cria, Lista, Atualiza e Deleta os dados de plano/modalidade
    """
    queryset = PlanoModalidade.objects.all()
    serializer_class = PlanoModalidadeSerializer

