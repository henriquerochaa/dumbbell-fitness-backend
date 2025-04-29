from rest_framework import generics

from .models import Exercicio
from .serializers import ExercicioSerializer


class ExercicioListCreateView(generics.ListCreateAPIView):
    """
    Cria e lista os dados do exercicio.
    """
    queryset = Exercicio.objects.all()
    serializer_class = ExercicioSerializer


class ExercicioRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Atualiza e deleta os dados do exercicio.
    """
    queryset = Exercicio.objects.all()
    serializer_class = ExercicioSerializer
