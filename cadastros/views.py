from rest_framework import generics

from rest_framework import viewsets, mixins
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.exceptions import PermissionDenied

from .models import Aluno, Matricula, Cartao
from .serializers import AlunoSerializer, MatriculaSerializer, CartaoSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    """
    Cria, Lista, Atualiza e delte os dados do aluno
    """
    queryset = Aluno.objects.all().order_by('id')
    serializer_class = AlunoSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        aluno = self.get_object()
        user = aluno.user
        if user:
            user.delete()  # apaga o usuário primeiro
        self.perform_destroy(aluno)  # só depois apaga o aluno
        return Response(status=status.HTTP_204_NO_CONTENT)


class MatriculaViewSet(viewsets.ModelViewSet):
    """
    Cria, Lista, Atualiza e delte os dados do aluno
    """
    queryset = Matricula.objects.all().order_by('id')
    serializer_class = MatriculaSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




class CartaoViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,  # para patch/put
                    viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Cartao.objects.all().order_by('id')
    serializer_class = CartaoSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Cartao.objects.all()
        return Cartao.objects.filter(aluno=self.request.user.aluno)

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            aluno_id = self.request.data.get('aluno')
            if not aluno_id:
                raise serializers.ValidationError({'aluno': 'Campo aluno é obrigatório para criar cartão.'})
            try:
                aluno = Aluno.objects.get(pk=aluno_id)
            except Aluno.DoesNotExist:
                raise serializers.ValidationError({'aluno': 'Aluno não encontrado.'})
        else:
            aluno = self.request.user.aluno  # Só o próprio aluno pode criar o cartão

        serializer.save(aluno=aluno)

    def perform_destroy(self, instance):
        if not self.request.user.is_superuser and instance.aluno != self.request.user.aluno:
            raise PermissionDenied("Você não pode deletar o cartão de outro aluno.")
        instance.delete()

    def perform_update(self, serializer):
        instance = self.get_object()
        if not self.request.user.is_superuser and instance.aluno != self.request.user.aluno:
            raise PermissionDenied("Você não pode atualizar o cartão de outro aluno.")
        serializer.save()

