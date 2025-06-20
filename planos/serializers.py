# Importa serializers do DRF para transformar modelos em JSON e vice-versa
from rest_framework import serializers

# Importa os modelos que serão serializados
from .models import Plano, Modalidade, PlanoModalidade


class PlanoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Plano.

    Expõe os campos id, nome e valor do plano.
    """
    class Meta:
        model = Plano
        fields = (
            'id',
            'nome',
            'valor'
        )


class ModalidadeSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Modalidade.

    Expõe os campos id e categoria da modalidade.
    """
    class Meta:
        model = Modalidade
        fields = (
            'id',
            'categoria'
        )


class PlanoModalidadeSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo PlanoModalidade.

    Serializa as relações entre plano e modalidade,  
    incluindo os serializers aninhados de Plano e Modalidade.
    """
    plano = PlanoSerializer()
    modalidade = ModalidadeSerializer()

    class Meta:
        model = PlanoModalidade
        fields = (
            'id',
            'plano',
            'modalidade',
        )
