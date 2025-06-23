from rest_framework import viewsets, mixins, serializers, status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Aluno, Matricula, Cartao
from .serializers import AlunoSerializer, MatriculaSerializer, CartaoSerializer


class AlunoViewSet(viewsets.ModelViewSet, UpdateModelMixin):
    """
    ViewSet completo para o recurso Aluno.

    Permite criar, listar, atualizar e deletar alunos.
    Na exclusão, o usuário relacionado ao aluno também é removido antes de apagar o aluno.
    """
    queryset = Aluno.objects.all().order_by('id')
    serializer_class = AlunoSerializer

    def list(self, request, *args, **kwargs):
        """Retorna lista paginada dos alunos."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Sobrescreve a exclusão para apagar o usuário relacionado antes de deletar o aluno.
        """
        aluno = self.get_object()
        user = aluno.user
        if user:
            user.delete()  # Apaga usuário associado primeiro
        self.perform_destroy(aluno)  # Depois apaga o aluno
        return Response(status=status.HTTP_204_NO_CONTENT)


class MatriculaViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para o recurso Matrícula.

    Permite criar, listar, atualizar e deletar matrículas.
    """
    queryset = Matricula.objects.all().order_by('id')
    serializer_class = MatriculaSerializer

    def list(self, request, *args, **kwargs):
        """Retorna lista paginada das matrículas."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CartaoViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """
    ViewSet customizado para Cartão.

    Permite listar, criar, atualizar e deletar cartões,
    com regras específicas de permissão:
    - Apenas usuários autenticados acessam
    - Superusuários podem ver e manipular todos os cartões
    - Usuários comuns só podem mexer nos seus próprios cartões
    """
    permission_classes = [IsAuthenticated]
    queryset = Cartao.objects.all().order_by('id')
    serializer_class = CartaoSerializer

    def get_queryset(self):
        """Retorna cartões conforme o perfil do usuário."""
        if self.request.user.is_superuser:
            return Cartao.objects.all()
        return Cartao.objects.filter(aluno=self.request.user.aluno)

    def perform_create(self, serializer):
        """
        Controla a criação do cartão:

        - Superusuários precisam informar o 'aluno' no corpo da requisição.
        - Usuários comuns criam cartão vinculado a si mesmos.
        """
        if self.request.user.is_superuser:
            aluno_id = self.request.data.get('aluno')
            if not aluno_id:
                raise serializers.ValidationError(
                    {'aluno': 'Campo aluno é obrigatório para criar cartão.'})
            try:
                aluno = Aluno.objects.get(pk=aluno_id)
            except Aluno.DoesNotExist:
                raise serializers.ValidationError(
                    {'aluno': 'Aluno não encontrado.'})
        else:
            aluno = self.request.user.aluno

        serializer.save(aluno=aluno)

    def perform_destroy(self, instance):
        """
        Impede que usuário comum delete cartão de outro aluno.
        Superusuário tem permissão total.
        """
        if not self.request.user.is_superuser and instance.aluno != self.request.user.aluno:
            raise PermissionDenied(
                "Você não pode deletar o cartão de outro aluno.")
        instance.delete()

    def perform_update(self, serializer):
        """
        Controla atualização do cartão, com as mesmas regras de permissão da exclusão.
        """
        instance = self.get_object()
        if not self.request.user.is_superuser and instance.aluno != self.request.user.aluno:
            raise PermissionDenied(
                "Você não pode atualizar o cartão de outro aluno.")
        serializer.save()
