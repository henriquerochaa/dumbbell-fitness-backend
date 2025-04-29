from rest_framework import serializers

from .models import Plano, Modalidade, PlanoModalidade


class PlanoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plano
        fields = (
            'id',
            'nome',
            'valor'
        )

class ModalidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Modalidade
        fields = (
            'id',
            'nome',
            'categoria'
        )

class PlanoModalidadeSerializer(serializers.ModelSerializer):
    plano = PlanoSerializer()
    modalidade = ModalidadeSerializer()