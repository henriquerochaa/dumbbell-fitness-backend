# Import do pacote serializer
from rest_framework import serializers

# Import do modelo padrão User
from django.contrib.auth.models import User

# Import do models Endereco
from .models import EnderecoModel


class BaseUserSerializer(serializers.ModelSerializer):
    """
    Serializer base para User, que cuida do hash da senha no create e update.
    """

    class Meta:
        model = User  # Especifique seu model aqui
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},  # Nunca exponha senha no GET
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password:
            user.set_password(password)  # A magia do hash seguro
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Atualiza hash da senha
        instance.save()
        return instance


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnderecoModel
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
        }
