from django.db import models
from base.models import Base
from alunos.models import Aluno
from exercicios.models import Exercicio


class Objetivos(models.TextChoices):
    """
    Lista de objetivos para o treino
    """
    HIPERTROFIA = 'H', 'Hipertrofia'
    FORCA = 'F', 'Forca'
    RESISTENCIA = 'R', 'Resistencia'
    EMAGRECIMENTO = 'E', 'Emagrecimento'
    FLEXIBILIDADE = 'X', 'Flexibilidade'


class Treino(Base):
    """
    Modelo de dados de treino
    """
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT, verbose_name='Aluno')
    objetivo = models.CharField("Objetivo", max_length=1, choices=Objetivos.choices)
    disponibilidade = models.CharField("Disponibilidade", max_length=1)
    observacao = models.TextField("Observações")

    @property
    def peso(self):
        return self.aluno.peso

    @property
    def altura(self):
        return self.aluno.altura
