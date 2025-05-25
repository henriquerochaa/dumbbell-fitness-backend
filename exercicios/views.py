from rest_framework import viewsets

from .models import Exercicio
from .serializers import ExercicioSerializer


class ExercicioViewSet(viewsets.ModelViewSet):
    """
    Cria, Lista, Atualiza e Deleta os dados de exercicio
    """

    queryset = Exercicio.objects.all().order_by('id')
    serializer_class = ExercicioSerializer