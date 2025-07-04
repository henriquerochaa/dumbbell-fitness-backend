# Importa serializers do DRF para transformar modelos Django em JSON e vice-versa
from rest_framework import serializers

# Importa o modelo Exercicio para ser serializado
from .models import Exercicio


class ExercicioSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Exercicio.
    Converte os dados do exercício para JSON, incluindo nome, descrição e equipamento.
    """

    class Meta:
        model = Exercicio
        fields = (
            'id',
            'nome',
            'descricao',
            'equipamento',
            'grupo_muscular',
            'categoria',
        )
