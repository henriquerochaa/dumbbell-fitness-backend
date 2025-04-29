from rest_framework import serializers
from .models import Aluno, Matricula, CartaoCredito


class AlunoSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Aluno. Converte os dados do aluno para JSON e define campos como 'cpf' e 'email'
    como somente para escrita.
    """

    class Meta:
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
        extra_kwargs = {
            'email': {'write_only': True},
            'cpf': {'write_only': True}
        }


class MatriculaSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Matricula. Converte dados da matrícula, incluindo informações do aluno, plano,
    forma de pagamento e cartão de crédito.
    """
    aluno = AlunoSerializer(read_only=True)
    aluno_id = serializers.PrimaryKeyRelatedField(queryset=Aluno.objects.all(), write_only=True, source='aluno')
    cartao_credito_id = serializers.PrimaryKeyRelatedField(queryset=CartaoCredito.objects.all(), write_only=True,
                                                           required=False, source='cartao_credito')
    forma_pagamento_display = serializers.CharField(source='get_forma_pagamento_display', read_only=True)

    class Meta:
        model = Matricula
        fields = (
            'id',
            'aluno',
            'aluno_id',
            'plano',
            'forma_pagamento',
            'forma_pagamento_display',
            'cartao_credito_id',
        )
