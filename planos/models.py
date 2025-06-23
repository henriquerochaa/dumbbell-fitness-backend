# Imports do Django
from django.db import models

# Import para utilização do tipo ArrayField
from django.contrib.postgres.fields import ArrayField

# Import de models
from core.models import BaseModel

# Import de Choices
from core.choices import CATEGORIA_MODALIDADES


class Plano(BaseModel):
    """
    Modelo que representa um plano de treino.

    Contém informações básicas como título, preço, descrição e benefícios do plano.
    """

    titulo = models.CharField('Título', max_length=255)
    preco = models.DecimalField('Preço', max_digits=8, decimal_places=2)
    descricao = models.TextField('Descrição', blank=True)
    beneficios = models.JSONField('Benefícios', default=list, help_text='Lista de benefícios oferecidos pelo plano')
    ativo = models.BooleanField('Ativo', default=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
        ordering = ['preco']


class Modalidade(BaseModel):
    """
    Modelo que representa uma modalidade de exercício.

    Define a categoria da modalidade com base em opções predefinidas.
    """

    categoria = models.CharField(
        'Categoria', max_length=255, choices=CATEGORIA_MODALIDADES)

    def __str__(self):
        return self.categoria


class PlanoModalidade(BaseModel):
    """
    Modelo que representa a relação entre plano e modalidade.

    Utilizado para associar um plano a uma ou mais modalidades.
    """

    plano = models.ForeignKey(Plano, on_delete=models.CASCADE)
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE)
