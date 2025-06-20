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

    Campos:
        - user: vínculo com o usuário de autenticação do Django.
        - nome: nome completo do aluno.
        - cpf: CPF único do aluno.
        - email: e-mail de contato do aluno.
        - sexo: gênero do aluno (usando choices).
        - data_nascimento: data de nascimento do aluno.
        - endereco: endereço vinculado ao aluno.
        - peso: peso atual do aluno (em kg).
        - altura: altura do aluno (em metros).
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='aluno')
    nome = models.CharField('Nome completo', max_length=255)
    cpf = models.CharField("CPF", max_length=14,
                           unique=True, validators=[cpf_validator])
    email = models.EmailField("E-mail", max_length=150)
    sexo = models.CharField("Sexo", max_length=1, choices=SEXO_USUARIO)
    data_nascimento = models.DateField("Data de Nascimento")
    endereco = models.ForeignKey(
        EnderecoModel, on_delete=models.CASCADE, null=False, blank=False, related_name="alunos")
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
        return self.nome


class Cartao(BaseModel):
    """
    Representa um cartão de crédito vinculado a um aluno.

    Campos:
        - aluno: referência ao aluno dono do cartão.
        - numero_cartao: número do cartão (sem espaços).
        - nome_titular: nome do titular impresso no cartão.
        - data_validade: validade no formato AAAA/MM.
        - cvv: código de segurança do cartão.
        - bandeira_cartao: bandeira do cartão (ex: Visa, Mastercard).
    """
    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, verbose_name="cartoes")
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
        return f"{self.nome_titular} – ****{self.numero_cartao[-4:]}"


class Matricula(BaseModel):
    """
    Representa a matrícula de um aluno em um plano da academia.

    Campos:
        - aluno: referência ao aluno matriculado.
        - plano: plano escolhido pelo aluno.
        - forma_pagamento: forma de pagamento da matrícula (PIX, cartão, etc.).
        - cartao: cartão usado no pagamento (opcional, dependendo da forma).
    """
    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, verbose_name="matriculas")
    plano = models.ForeignKey(
        Plano, on_delete=models.PROTECT, verbose_name="plano")
    forma_pagamento = models.CharField(
        "Forma de Pagamento", max_length=1, choices=FORMA_PAGAMENTO)
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
        return f"Matrícula de {self.aluno.nome} no plano {self.plano.nome}"
