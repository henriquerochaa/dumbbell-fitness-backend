from rest_framework import generics

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Aluno, Matricula
from .serializers import AlunoSerializer, MatriculaSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    """
    Cria, Lista, Atualiza e delte os dados do aluno
    """
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MatriculaViewSet(viewsets.ModelViewSet):
    """
    Cria, Lista, Atualiza e delte os dados do aluno
    """
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
