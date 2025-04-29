from rest_framework import serializers
from .models import Treino


class TreinoSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Treino. Converte os dados do treino para JSON
    """

    class Meta:
        model = Treino
        fields = (
            'id',
            'aluno',
            'objetivo',
            'disponibilidade',
            'observacao',
            'peso',
            'altura'
        )
        depth = 1
