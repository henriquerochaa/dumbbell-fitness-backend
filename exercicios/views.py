from rest_framework import viewsets

from .models import Exercicio
from .serializers import ExercicioSerializer


class ExercicioViewSet(viewsets.ModelViewSet):
    """
    Cria, Lista, Atualiza e Deleta os dados de exercicio
    """

    queryset = Exercicio.objects.all()
    serializer_class = ExercicioSerializer