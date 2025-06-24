# Imports do Django para criação de modelos (tabelas no banco)
from django.db import models

# Importa modelos base e relacionados para usar como FK e herança
from core.models import BaseModel
from cadastros.models import Aluno
from exercicios.models import Exercicio

# Importa escolhas predefinidas para campo de objetivo do treino
from core.choices import OBJETIVO_TREINO


class Treino(BaseModel):
    """
    Representa um treino associado a um aluno.

    Contém informações sobre nome, objetivo e observações do treino.
    Propriedades calculadas para peso e altura do aluno vinculado.
    """
    nome = models.CharField("Nome da Rotina", max_length=100, default="Nova Rotina")
    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, verbose_name='Aluno')
    objetivo = models.CharField(
        "Objetivo", max_length=20, choices=OBJETIVO_TREINO)
    observacao = models.TextField("Observações", blank=True)

    @property
    def peso(self):
        return self.aluno.peso

    @property
    def altura(self):
        return self.aluno.altura


class ExercicioTreino(BaseModel):
    """
    Associação entre treino e exercício.

    Define séries, repetições, carga e descanso para cada exercício no treino.
    """
    treino = models.ForeignKey(
        Treino, on_delete=models.CASCADE, related_name='exercicios')
    exercicio = models.ForeignKey(Exercicio, on_delete=models.PROTECT)
    series = models.PositiveIntegerField(
        verbose_name="Número de séries", default=None)
    repeticoes = models.PositiveIntegerField(
        verbose_name="Número de repetições", default=None)
    carga = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    descanso = models.PositiveIntegerField(
        verbose_name="Tempo de descanso (em segundos)",
        help_text="Informe o tempo de descanso em segundos", default=90)
