from rest_framework import generics

from .models import Plano, Modalidade, PlanoModalidade
from .serializers import PlanoSerializer, ModalidadeSerializer, PlanoModalidadeSerializer


class PlanoListCreateView(generics.ListCreateAPIView):
    """
    Cria e lista os dados de plano
    """
    queryset = Plano.objects.all()
    serializer_class = PlanoSerializer


class PlanoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Atualiza e deleta dados de plano
    """
    queryset = Plano.objects.all()
    serializer_class = PlanoSerializer


class ModalidadeListCreateView(generics.ListCreateAPIView):
    """
    Cria e lista os dados de modalidade
    """
    queryset = Modalidade.objects.all()
    serializer_class = ModalidadeSerializer


class ModalidadeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Atualiza e deleta dados de modalidade
    """
    queryset = Modalidade.objects.all()
    serializer_class = ModalidadeSerializer

class PlanoModalidadeListCreateView(generics.ListCreateAPIView):
    """
    Cria e lista os dados da relação plano/modalidade
    """
    queryset = PlanoModalidade.objects.all()
    serializer_class = PlanoModalidadeSerializer

class PlanoModalidadeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Atualiza e deleta dados de plano/modalidade
    """
    queryset = PlanoModalidade.objects.all()
    serializer_class = PlanoModalidadeSerializer
