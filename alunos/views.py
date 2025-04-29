from rest_framework import generics

from .models import Aluno, Matricula
from .serializers import AlunoSerializer, MatriculaSerializer


class AlunoListCreateView(generics.ListCreateAPIView):
    """
    Cria e lista os dados do aluno
    """
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer


class AlunoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Atualiza e deleta os dados do aluno
    """
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer


class MatriculaListCreateView(generics.ListCreateAPIView):
    """
    Cria e lista as matriculas
    """
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer


class MatriculaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Atualiza e deleta os matriculas
    """
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer


