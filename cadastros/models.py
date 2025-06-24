# =============================================================================
# ARQUIVO: cadastros/models.py
# DESCRIÇÃO: Modelos para gerenciamento de cadastros do projeto Dumbbell Fitness
# FUNÇÃO: Define modelos para alunos, matrículas, cartões e relacionamentos
# =============================================================================

# Imports Django
from django.db import models
from django.contrib.auth.models import User

# Imports DRF
from rest_framework.authtoken.models import Token

# Imports de models
from planos.models import Plano
from core.models import BaseModel, EnderecoModel

# Imports de choices
from core.choices import FORMA_PAGAMENTO, BANDEIRA_CARTAO, SEXO_USUARIO

# Imports de validators
from core.validators import (cpf_validator, validate_numero_cartao,
                             validate_cvv, validate_data_validade)


class Aluno(BaseModel):
    """
    Representa um aluno matriculado na academia.
    
    Este modelo armazena todas as informações pessoais e físicas do aluno,
    incluindo dados de autenticação (vinculado ao User do Django).
    
    Campos principais:
    - user: vínculo com o usuário de autenticação do Django
    - dados pessoais: nome, cpf, email, sexo, data_nascimento
    - dados físicos: peso, altura
    - endereco: vínculo com o modelo EnderecoModel
    """
    # Vínculo com o sistema de autenticação do Django
    # OneToOneField garante que cada aluno tenha um usuário único
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='aluno')
    
    # Dados pessoais do aluno
    nome = models.CharField('Nome completo', max_length=255)
    cpf = models.CharField("CPF", max_length=14, unique=True, validators=[cpf_validator])
    email = models.EmailField("E-mail", max_length=150)
    sexo = models.CharField("Sexo", max_length=1, choices=SEXO_USUARIO)
    data_nascimento = models.DateField("Data de Nascimento")
    
    # Vínculo com endereço (obrigatório)
    endereco = models.ForeignKey(
        EnderecoModel, on_delete=models.CASCADE, null=False, blank=False, related_name="alunos")
    
    # Dados físicos do aluno
    peso = models.DecimalField("Peso (kg)", max_digits=5, decimal_places=2)
    altura = models.DecimalField("Altura (m)", max_digits=4, decimal_places=2)

    class Meta:
        """
        Configurações de meta para o modelo Aluno.
        """
        db_table = 'aluno'
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'

    def __str__(self):
        """
        Representação em string do aluno.
        
        Retorna o nome do aluno para facilitar identificação.
        """
        return self.nome


class Cartao(BaseModel):
    """
    Representa um cartão de crédito vinculado a um aluno.
    
    Este modelo armazena os dados do cartão de crédito/débito do aluno,
    usado para pagamento das mensalidades.
    
    Campos principais:
    - aluno: referência ao aluno dono do cartão
    - dados do cartão: número, titular, validade, CVV, bandeira
    """
    # Vínculo com o aluno dono do cartão
    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, verbose_name="cartoes")
    
    # Dados do cartão
    numero_cartao = models.CharField(
        "Número do Cartão", max_length=16, validators=[validate_numero_cartao])
    nome_titular = models.CharField("Nome no Cartão", max_length=255)
    data_validade = models.CharField(
        "Data de Validade (AAAA/MM)", max_length=7, validators=[validate_data_validade])
    cvv = models.CharField("CVV", max_length=3, validators=[validate_cvv])
    bandeira_cartao = models.CharField(
        "Bandeira de Cartão", max_length=10, choices=BANDEIRA_CARTAO)

    class Meta:
        """
        Configurações de meta para o modelo Cartao.
        """
        db_table = 'cartoes'
        verbose_name = 'Cartão'
        verbose_name_plural = 'Cartões'

    def __str__(self):
        """
        Representação em string do cartão.
        
        Retorna o nome do titular e os últimos 4 dígitos do cartão
        para facilitar identificação sem expor dados sensíveis.
        """
        return f"{self.nome_titular} – ****{self.numero_cartao[-4:]}"


class Matricula(BaseModel):
    """
    Representa a matrícula de um aluno em um plano da academia.
    
    Este modelo gerencia a relação entre aluno e plano, incluindo
    informações sobre pagamento e forma de pagamento.
    
    Campos principais:
    - aluno: referência ao aluno matriculado
    - plano: plano escolhido pelo aluno
    - forma_pagamento: forma de pagamento da matrícula
    - cartao: cartão usado no pagamento (opcional)
    """
    # Vínculo com o aluno matriculado
    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, verbose_name="matriculas")
    
    # Vínculo com o plano escolhido
    plano = models.ForeignKey(
        Plano, on_delete=models.PROTECT, verbose_name="plano")
    
    # Forma de pagamento (obrigatório)
    forma_pagamento = models.CharField(
        "Forma de Pagamento", max_length=1, choices=FORMA_PAGAMENTO)
    
    # Cartão usado no pagamento (opcional, depende da forma de pagamento)
    cartao = models.ForeignKey(
        Cartao, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="Cartão", related_name="matriculas"
    )

    class Meta:
        """
        Configurações de meta para o modelo Matricula.
        """
        db_table = 'matriculas'
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'

    def __str__(self):
        """
        Representação em string da matrícula.
        
        Retorna uma descrição clara da matrícula incluindo
        nome do aluno e plano escolhido.
        """
        return f"Matrícula de {self.aluno.nome} no plano {self.plano.titulo}"
