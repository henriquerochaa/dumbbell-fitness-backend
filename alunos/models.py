from django.db import models
from .planos import Plano


class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Sexo(models.TextChoices):
    MASCULINO = 'M', 'Masculino'
    FEMININO = 'F', 'Feminino'
    OUTRO = 'O', 'Outro'


class FormaPagamento(models.TextChoices):
    CARTAO_CREDITO = 'C', 'Cartão de Crédito'
    PIX = 'P', 'PIX'


class Estado(Base):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.sigla


class Municipio(Base):
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} – {self.estado.sigla}"


class Aluno(Base):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField()
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    data_nascimento = models.DateField()
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
    endereco = models.CharField(max_length=255)
    status = models.CharField(max_length=8, choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo')
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = 'aluno'
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'

    def __str__(self):
        return self.nome


class CartaoCredito(Base):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    numero_cartao = models.CharField(max_length=16)
    nome_titular = models.CharField(max_length=255)
    data_validade = models.DateField()
    cvv = models.CharField(max_length=3)
    bandeira_cartao = models.CharField(max_length=20)

    class Meta:
        db_table = 'cartoes_credito'
        verbose_name = 'Cartão de Crédito'
        verbose_name_plural = 'Cartões de Crédito'

    def __str__(self):
        return f"{self.nome_titular} – ****{self.numero_cartao[-4:]}"


class Matricula(Base):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    plano = models.ForeignKey(Plano, on_delete=models.PROTECT)
    forma_pagamento = models.CharField(max_length=1, choices=FormaPagamento.choices)
    cartao_credito = models.ForeignKey(CartaoCredito, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'matriculas'
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'

    def __str__(self):
        return f"Matrícula de {self.aluno.nome} no plano {self.plano.nome}"
