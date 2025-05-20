from rest_framework import viewsets

from .models import Treino
from .serializers import TreinoSerializer


class TreinoViewSet(viewsets.ModelViewSet):
    """
    Cria, Lista, Atualiza, Deleta os dados do treino
    """

    queryset = Treino.objects.all()
    serializer_class = TreinoSerializer