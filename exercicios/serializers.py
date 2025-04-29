from rest_framework import serializers
from .models import Exercicio


class ExercicioSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Exercicio. Converte os dados do exercício para JSON, incluindo nome, descrição e equipamento.
    """

    class Meta:
        model = Exercicio
        fields = (
            'id',
            'nome',
            'descricao',
            'equipamento'
        )
