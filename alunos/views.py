from rest_framework import generics

from rest_framework import viewsets, mixins
from rest_framework.response import Response

from .models import Aluno, Matricula, Cartao
from .serializers import AlunoSerializer, MatriculaSerializer, CartaoSerializer


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


class CartaoViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Cartao.objects.all()
    serializer_class = CartaoSerializer

    def get_queryset(self):
        aluno_id = self.request.query_params.get('aluno')
        if aluno_id:
            return Cartao.objects.filter(aluno_id=aluno_id)
        return Cartao.objects.none()

    def perform_create(self, serializer):
        aluno_id = self.request.data.get('aluno')
        if not aluno_id:
            # Pode lançar erro ou usar o aluno do user, se fizer sentido
            raise serializers.ValidationError({'aluno': 'Campo aluno é obrigatório para criar cartão.'})

        # Aqui você pode verificar se o aluno_id é válido no banco
        from .models import Aluno
        try:
            aluno = Aluno.objects.get(pk=aluno_id)
        except Aluno.DoesNotExist:
            raise serializers.ValidationError({'aluno': 'Aluno não encontrado.'})

        serializer.save(aluno=aluno)
