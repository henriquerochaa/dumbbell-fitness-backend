# Importa serializers do DRF para transformar modelos em JSON e vice-versa
from rest_framework import serializers

# Importa os modelos que serão serializados
from .models import Plano, Modalidade, PlanoModalidade

# Importa o modelo User do Django
from django.contrib.auth.models import User


class PlanoSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Plano.

    Converte os dados do plano para JSON, incluindo título, preço, descrição e benefícios.
    """
    class Meta:
        model = Plano
        fields = (
            'id',
            'titulo',
            'preco',
            'beneficios',
            'ativo'
        )


class UserSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo User do Django.

    Expõe informações básicas do usuário para a API.
    """
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name'
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
