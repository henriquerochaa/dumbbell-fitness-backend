from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Treino
from .serializers import TreinoSerializer
from cadastros.models import Aluno


class TreinoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar CRUD de Treino.

    Apenas usuários autenticados podem acessar.
    Filtra os treinos para retornar somente os do aluno logado.
    """
    queryset = Treino.objects.all().order_by('id')
    serializer_class = TreinoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retorna os treinos pertencentes ao usuário autenticado.
        """
        user = self.request.user
        return self.queryset.filter(aluno__user=user)

    def perform_create(self, serializer):
        """
        Associa o treino ao aluno do usuário autenticado no momento da criação.
        """
        try:
            aluno = Aluno.objects.get(user=self.request.user)
            serializer.save(aluno=aluno)
        except Aluno.DoesNotExist:
            raise ValidationError("Usuário não possui aluno associado.")

    def list(self, request, *args, **kwargs):
        """
        Retorna a lista de treinos do aluno autenticado.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
