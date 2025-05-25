import re
from datetime import datetime

from django.contrib.auth.models import User

from rest_framework import serializers
from .models import Aluno, Matricula, Cartao
from planos.serializers import PlanoSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AlunoSerializer(serializers.ModelSerializer):
    estado = serializers.SerializerMethodField()
    user = UserSerializer(write_only=True)  # Recebe os dados do usuário junto

    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'cpf', 'email', 'sexo', 'data_nascimento', 'estado',
                  'municipio', 'endereco', 'peso', 'altura', 'user']
        extra_kwargs = {
            'email': {'write_only': True},
            'cpf': {'write_only': True}
        }

    def get_estado(self, obj):
        return obj.municipio.estado

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        aluno = Aluno.objects.create(**validated_data)
        aluno.user = user
        aluno.save()
        return aluno

    def update(self, instance, validated_data):
        # Se vier user no update, atualiza o user relacionado
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

        # Atualiza email somente se vier
        if 'email' in validated_data:
            instance.email = validated_data.pop('email')

        # Atualiza os outros campos normais
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class CartaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartao
        fields = [
            'id',
            'aluno',
            'numero_cartao',
            'nome_titular',
            'data_validade',
            'cvv',
            'bandeira_cartao',
        ]
        extra_kwargs = {
            'nome_titular': {'write_only': True},
            'numero_cartao': {'write_only': True},
            'cvv': {'write_only': True},
        }

    def validate_numero_cartao(self, value):
        if not value.isdigit() or len(value) != 16:
            raise serializers.ValidationError("Número do cartão deve ter 16 dígitos.")
        return value

    def validate_cvv(self, value):
        if not value.isdigit() or len(value) != 3:
            raise serializers.ValidationError("CVV deve ter 3 dígitos.")
        return value

    def validate_data_validade(self, value):
        if not re.match(r'^\d{4}/(0[1-9]|1[0-2])$', value):
            raise serializers.ValidationError("Formato inválido. Use AAAA/MM.")

        ano, mes = map(int, value.split('/'))
        validade = datetime(ano, mes, 1)
        hoje = datetime.today().replace(day=1)

        if validade < hoje:
            raise serializers.ValidationError("Cartão expirado.")

        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            # Aqui garante que o cartão seja sempre do aluno do usuário logado
            validated_data['aluno'] = request.user.aluno
        return super().create(validated_data)


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = [
            'id',
            'plano',
            'aluno',
            'forma_pagamento',
            'cartao'
        ]
        extra_kwargs = {
            'cartao': {'write_only': False}
        }

    def validate(self, data):
        forma_pagamento = data.get('forma_pagamento')
        cartao = data.get('cartao')

        if forma_pagamento in ['credito', 'debito']:
            if not cartao:
                raise serializers.ValidationError({
                    'cartao': 'Você precisa fornecer os dados do cartão para essa forma de pagamento.'
                })
        elif forma_pagamento == 'pix':
            if cartao:
                raise serializers.ValidationError({
                    'cartao': 'Não forneça dados do cartão para pagamento via PIX.'
                })

        aluno = data.get('aluno')
        if aluno:
            qs = Matricula.objects.filter(aluno=aluno)
            # Ignora a própria instância, se for update
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    "Aluno já possui matrícula ativa no sistema."
                )

        return data
