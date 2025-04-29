from django.db import models
from base.models import Base

class Categoria(models.TextChoices):
    """
    Categorias disponíveis para modalidades.
    """
    MUSCULACAO = 'M', 'Musculação'
    DANCA = 'D', 'Dança'


class Plano(Base):
    """
    Modelo de dados para o plano.
    """
    nome = models.CharField('Nome', max_length=255)
    valor = models.DecimalField('Valor', max_digits=8, decimal_places=2)


class Modalidade(Base):
    """
    Modelo de dados para a modalidade.
    """
    nome = models.CharField('Nome', max_length=255)
    categoria = models.CharField('Categoria', max_length=255, choices=Categoria.choices)


class PlanoModalidade(Base):
    """
    Relacionamento entre plano e modalidade.
    """
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE)
    modalidade = models.ForeignKey(Modalidade, on_delete=models.CASCADE)
