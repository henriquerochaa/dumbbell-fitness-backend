# Imports do Django
from django.db import models

# Import de models
from core.models import BaseModel

# Import de Choices
from core.choices import CATEGORIA_MODALIDADES


class Plano(BaseModel):
    """
    Modelo que representa um plano de treino.

    Contém informações básicas como nome e valor do plano.
    """

    nome = models.CharField('Nome', max_length=255)
    valor = models.DecimalField('Valor', max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nome


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
