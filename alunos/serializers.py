from rest_framework import serializers
from .models import Aluno, Matricula

class AlunoSerializer(serializers.ModelSerializer):

    class Meta:
        extra_kwargs = {
            'email': {'write_only': True},
            'cpf': {'write_only': True}
        }
        model = Aluno
        fields = (
            'id',
            'nome',
            'cpf',
            'email',
            'sexo',
            'data_nascimento',
            'estado',
            'municipio',
            'endereco',
            'status',
            'peso',
            'altura'
        )

class MatriculaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Matricula
        fields = (
            'id',
            'aluno',
            'plano',
            'forma_pagamento',
        )
