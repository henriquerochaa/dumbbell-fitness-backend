# Expressões regulares para validações (ex: data_validade cartão)
import re
# Manipulação de datas para validar validade do cartão
from datetime import datetime

# Modelo User padrão do Django
from django.contrib.auth.models import User

# Serializers do DRF para converter e validar dados
from rest_framework import serializers

# Modelos do app Cadastros
from .models import Aluno, Matricula, Cartao

# Import do Serializer Padrão para usuarios
from core.serializers import BaseUserSerializer

# Validators do core para regras específicas
from core.validators import validate_aluno_matricula_unica, validate_forma_pagamento_cartao


class AlunoSerializer(serializers.ModelSerializer):
    """
    Dados completos do aluno, com usuário embutido.

    Cria o user junto, gerencia atualização dos dois.
    """

    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'cpf', 'email', 'sexo', 'data_nascimento', 'endereco',
                  'peso', 'altura', 'user']
        extra_kwargs = {
            'email': {'write_only': True},
            'cpf': {'write_only': True}
        }

    def create(self, validated_data):
        """Cria user e aluno ligados."""
        user_data = validated_data.pop('user')
        user = BaseUserSerializer.create(
            BaseUserSerializer(), validated_data=user_data)
        aluno = Aluno.objects.create(**validated_data)
        aluno.user = user
        aluno.save()
        return aluno

    def update(self, instance, validated_data):
        """Atualiza user embutido e dados do aluno."""
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = BaseUserSerializer(
                instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        if 'email' in validated_data:
            instance.email = validated_data.pop('email')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class CartaoSerializer(serializers.ModelSerializer):
    """
    Valida e gerencia dados do cartão de crédito do aluno.

    Checa número, CVV, validade, e associa cartão ao aluno logado.
    """
    class Meta:
        model = Cartao
        fields = [
            'id',
            'aluno',
            'numero_cartao',
            'nome_titular',
            'data_validade',
            'cvv',
            'bandeira_cartao',
        ]
        extra_kwargs = {
            'nome_titular': {'write_only': True},
            'numero_cartao': {'write_only': True},
            'cvv': {'write_only': True},
        }


class MatriculaSerializer(serializers.ModelSerializer):
    """
    Controla matrícula de aluno em planos e forma de pagamento.

    Garante que o pagamento e o cartão estejam coerentes,
    e evita duplicidade de matrículas ativas para o aluno.
    """
    class Meta:
        model = Matricula
        fields = [
            'id',
            'plano',
            'aluno',
            'forma_pagamento',
            'cartao'
        ]
        extra_kwargs = {
            'cartao': {'write_only': False}
        }

    def validate(self, data):
        """Valida a relação entre forma_pagamento e cartão e matrícula única."""
        validate_forma_pagamento_cartao(data)
        validate_aluno_matricula_unica(data, instance=self.instance)
        return data
