# Importa serializers do DRF para transformar modelos em JSON e vice-versa
from rest_framework import serializers

# Importa os modelos que serão serializados
from .models import Plano, Modalidade, PlanoModalidade


class PlanoSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Plano.

    Converte os dados do plano para JSON, incluindo nome, valor e benefícios listados.
    """
    class Meta:
        model = Plano
        fields = (
            'id',
            'nome',
            'valor',
            'beneficios'  # Campo ArrayField adicionado para exibir os benefícios
        )


class ModalidadeSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Modalidade.

    Expõe a categoria da modalidade para visualização e manipulação via API.
    """
    class Meta:
        model = Modalidade
        fields = (
            'id',
            'categoria'
        )


class PlanoModalidadeSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo PlanoModalidade.

    Representa a associação entre um plano e uma modalidade específica.
    Inclui serializadores aninhados para mostrar os dados completos de cada relação.
    """
    plano = PlanoSerializer(read_only=True)
    modalidade = ModalidadeSerializer(read_only=True)

    class Meta:
        model = PlanoModalidade
        fields = (
            'id',
            'plano',
            'modalidade',
        )
