from django.db import models
from planos.models import Plano
from base.models import Base


class Sexo(models.TextChoices):
    """
    Lista de Sexos
    """
    MASCULINO = 'M', 'Masculino'
    FEMININO = 'F', 'Feminino'
    OUTRO = 'O', 'Outro'


class FormaPagamento(models.TextChoices):
    """
    Lista de Forma Pagamento
    """
    CARTAO_CREDITO = 'C', 'Cartão de Crédito'
    PIX = 'P', 'PIX'


class Estado(Base):
    """
    Modelos de dados para Estado
    """
    nome = models.CharField('Nome do Estado', max_length=100)
    sigla = models.CharField('Sigla do Estado', max_length=2, unique=True)

    def __str__(self):
        return self.sigla


class Municipio(Base):
    """
    Modelos de dados para Municipio
    """
    nome = models.CharField('Nome do Município', max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name='Estado')

    def __str__(self):
        return f"{self.nome} – {self.estado.sigla}"


class Aluno(Base):
    """
    Modelo de dados para Aluno
    """
    nome = models.CharField('Nome completo', max_length=255)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    email = models.EmailField("E-mail", max_length=150)
    sexo = models.CharField("Sexo", max_length=1, choices=Sexo.choices)
    data_nascimento = models.DateField("Data de Nascimento")
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, verbose_name="Estado de residência")
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT, verbose_name="Município de residência")
    endereco = models.CharField("Endereço", max_length=255)
    peso = models.DecimalField("Peso (kg)", max_digits=5, decimal_places=2)
    altura = models.DecimalField("Altura (m)", max_digits=4, decimal_places=2)

    class Meta:
        """
        Verbose name para o campo aluno
        """
        db_table = 'aluno'
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'

    def __str__(self):
        return self.nome


class CartaoCredito(Base):
    """
    Modelo de dados para Cartao de Credito
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="Aluno")
    numero_cartao = models.CharField("Número do Cartão", max_length=16)
    nome_titular = models.CharField("Nome no Cartão", max_length=255)
    data_validade = models.DateField("Data de Validade")
    cvv = models.CharField("CVV", max_length=3)
    bandeira_cartao = models.CharField("Bandeira do Cartão", max_length=20)

    class Meta:
        """
        Verbose name para o campo aluno
        """
        db_table = 'cartoes_credito'
        verbose_name = 'Cartão de Crédito'
        verbose_name_plural = 'Cartões de Crédito'

    def __str__(self):
        return f"{self.nome_titular} – ****{self.numero_cartao[-4:]}"


class Matricula(Base):
    """
    Modelo de dados para Matricula
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="Aluno")
    plano = models.ForeignKey(Plano, on_delete=models.PROTECT, verbose_name="Plano")
    forma_pagamento = models.CharField("Forma de Pagamento", max_length=1, choices=FormaPagamento.choices)
    cartao_credito = models.ForeignKey(CartaoCredito, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cartão de Crédito")

    class Meta:
        """
        Verbose name para o campo aluno
        """
        db_table = 'matriculas'
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'

    def __str__(self):
        return f"Matrícula de {self.aluno.nome} no plano {self.plano.nome}"
