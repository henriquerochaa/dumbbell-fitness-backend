# Importa o módulo viewsets do DRF, que facilita criar CRUDs completos com pouco código
from rest_framework import viewsets

# Importa o modelo Exercicio para manipulação de dados
from .models import Exercicio

# Importa o serializer que transforma dados do modelo em JSON e vice-versa
from .serializers import ExercicioSerializer


class ExercicioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar operações CRUD no modelo Exercicio.

    Permite criar, listar, atualizar e deletar registros de exercícios,
    utilizando o serializer ExercicioSerializer para conversão dos dados.
    """

    queryset = Exercicio.objects.all().order_by('id')
    serializer_class = ExercicioSerializer
