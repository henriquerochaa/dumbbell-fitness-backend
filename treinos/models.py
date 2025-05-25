from django.db import models
from base.models import Base
from cadastros.models import Aluno
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
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name='Aluno')
    objetivo = models.CharField("Objetivo", max_length=1, choices=Objetivos.choices)
    disponibilidade = models.CharField("Disponibilidade", max_length=1)
    observacao = models.TextField("Observações", blank=True)

    @property
    def peso(self):
        return self.aluno.peso

    @property
    def altura(self):
        return self.aluno.altura


class ExercicioTreino(Base):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, related_name='exercicios')
    exercicio = models.ForeignKey(Exercicio, on_delete=models.PROTECT)
    series = models.PositiveIntegerField(verbose_name="Número de séries", default=None)
    repeticoes = models.PositiveIntegerField(verbose_name="Número de repetições", default=None)
    carga = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    descanso = models.PositiveIntegerField(verbose_name="Tempo de descanso (em segundos)",
                                           help_text="Informe o tempo de descanso em segundos", default=90)
