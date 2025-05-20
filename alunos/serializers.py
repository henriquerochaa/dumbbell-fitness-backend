from rest_framework import serializers
from .models import Aluno, Matricula, CartaoCredito
from planos.serializers import PlanoSerializer


class AlunoSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Aluno. Converte os dados do aluno para JSON e define campos como 'cpf' e 'email'
    como somente para escrita.
    """

    data_nascimento = serializers.DateField(
        format="%d/%m/%Y",  # Formato de saída
        input_formats=["%d/%m/%Y"],  # Formato de entrada
    )

    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'cpf', 'email', 'sexo', 'data_nascimento', 'estado',
                  'municipio', 'endereco', 'peso', 'altura']
        extra_kwargs = {
            'email': {'write_only': True},
            'cpf': {'write_only': True}
        }


class MatriculaSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Matricula. Converte dados da matrícula, incluindo informações do aluno, plano,
    forma de pagamento e cartão de crédito.
    """
    metodos_pagamento_disponiveis = serializers.SerializerMethodField()

    class Meta:
        model = Matricula
        fields = [
            'id',
            'plano',
            'aluno',
            'forma_pagamento',
            'cartao_credito',
            'metodos_pagamento_disponiveis',
        ]
        extra_kwargs = {
            'cartao_credito': {'required': False}
        }

    def get_metodos_pagamento_disponiveis(self, obj):
        if 'dumbbell' in obj.plano.nome.lower():
            return [{'value': 'C', 'label': 'Cartão de Crédito'}]
        return [
            {'value': 'C', 'label': 'Cartão de Crédito'},
            {'value': 'P', 'label': 'PIX'},
            {'value': 'D', 'label': 'Débito'}
        ]
