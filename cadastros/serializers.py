# =============================================================================
# ARQUIVO: cadastros/serializers.py
# DESCRIÇÃO: Serializers para gerenciamento de cadastros do projeto Dumbbell Fitness
# FUNÇÃO: Converte e valida dados dos modelos para JSON e vice-versa
# =============================================================================

# Expressões regulares para validações (ex: data_validade cartão)
import re
# Manipulação de datas para validar validade do cartão
from datetime import datetime

# Modelo User padrão do Django
from django.contrib.auth.models import User

# Serializers do DRF para converter e validar dados
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Modelos do app Cadastros
from .models import Aluno, Matricula, Cartao

# Import do Serializer Padrão para usuarios
from core.serializers import BaseUserSerializer

# Validators do core para regras específicas
from core.validators import validate_aluno_matricula_unica, validate_forma_pagamento_cartao


class AlunoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Aluno.
    
    Gerencia a conversão de dados do modelo Aluno para JSON e vice-versa.
    Inclui lógica especial para criação de usuário e token de autenticação.
    
    Funcionalidades:
    - Cria automaticamente um User do Django quando um Aluno é criado
    - Gera token de autenticação para o novo usuário
    - Valida dados pessoais e físicos do aluno
    - Gerencia relacionamento com endereço
    """
    # Campo password para criação do usuário (não é salvo no modelo Aluno)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'cpf', 'email', 'sexo', 'data_nascimento', 'endereco',
                  'peso', 'altura', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # Nunca retorna a senha nas respostas
            'email': {'write_only': True},     # Email usado como username
            'cpf': {'write_only': True},       # CPF é sensível
        }

    def create(self, validated_data):
        """
        Cria user e aluno ligados.
        
        Este método é chamado quando um novo Aluno é criado via API.
        Ele cria automaticamente um User do Django e gera um token de autenticação.
        
        Args:
            validated_data (dict): Dados validados do aluno
            
        Returns:
            Aluno: Instância do aluno criado
            
        Processo:
        1. Extrai a senha dos dados validados
        2. Cria um User do Django usando email como username
        3. Cria o Aluno vinculado ao User
        4. Gera token de autenticação
        5. Retorna o aluno criado
        """
        # Extrai a senha dos dados validados
        senha = validated_data.pop('password')
        email = validated_data.get('email')
        nome = validated_data.get('nome')
        cpf = validated_data.get('cpf')

        # Cria o User do Django
        # Usa o email como username para facilitar login
        user = User.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=nome  # Define o primeiro nome do usuário
        )
        
        # Cria o Aluno vinculado ao User
        aluno = Aluno.objects.create(user=user, **validated_data)

        # Criar token padrão DRF para esse user
        # O token é usado para autenticação via API
        token, created = Token.objects.get_or_create(user=user)
        self._token = token.key  # Armazena o token para uso posterior

        return aluno

    def update(self, instance, validated_data):
        """
        Atualiza user embutido e dados do aluno.
        
        Este método é chamado quando um Aluno existente é atualizado via API.
        Ele atualiza tanto os dados do aluno quanto do usuário vinculado.
        
        Args:
            instance (Aluno): Instância atual do aluno
            validated_data (dict): Novos dados validados
            
        Returns:
            Aluno: Instância do aluno atualizada
        """
        # Se houver dados do usuário, atualiza o User vinculado
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = BaseUserSerializer(
                instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # Atualiza o email do aluno se fornecido
        if 'email' in validated_data:
            instance.email = validated_data.pop('email')

        # Atualiza os demais campos do aluno
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class CartaoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Cartao.
    
    Valida e gerencia dados do cartão de crédito do aluno.
    Inclui validações para número, CVV, validade e associação ao aluno.
    
    Funcionalidades:
    - Valida formato do número do cartão (16 dígitos)
    - Valida CVV (3 dígitos)
    - Valida data de validade (formato AAAA/MM)
    - Associa cartão ao aluno automaticamente
    """
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
            'nome_titular': {'write_only': True},  # Dados sensíveis
            'numero_cartao': {'write_only': True}, # Nunca expor número completo
            'cvv': {'write_only': True},           # Código de segurança
        }


class MatriculaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Matricula.
    
    Controla matrícula de aluno em planos e forma de pagamento.
    Inclui validações complexas para garantir integridade dos dados.
    
    Funcionalidades:
    - Valida relação entre forma de pagamento e cartão
    - Evita duplicidade de matrículas ativas para o mesmo aluno
    - Gerencia relacionamentos entre aluno, plano e cartão
    """
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
            'cartao': {'write_only': False}  # Permite visualizar dados do cartão
        }

    def validate(self, data):
        """
        Valida a relação entre forma_pagamento e cartão e matrícula única.
        
        Este método é chamado automaticamente pelo DRF para validar
        os dados antes de salvar no banco.
        
        Args:
            data (dict): Dados da matrícula a serem validados
            
        Returns:
            dict: Dados validados
            
        Raises:
            ValidationError: Se as validações falharem
        """
        # Valida se a forma de pagamento é compatível com o cartão
        validate_forma_pagamento_cartao(data)
        
        # Valida se o aluno não tem matrícula ativa duplicada
        validate_aluno_matricula_unica(data, instance=self.instance)
        
        return data
