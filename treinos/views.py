from rest_framework import generics

from .models import Treino
from .serializers import TreinoSerializer


class TreinoListCreateView(generics.ListCreateAPIView):
    """
    Cria e lista os dados do treino
    """
    queryset = Treino.objects.all()
    serializer_class = TreinoSerializer


class TreinoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Atualiza e deleta os dados do treino
    """
    queryset = Treino.objects.all()
    serializer_class = TreinoSerializer
