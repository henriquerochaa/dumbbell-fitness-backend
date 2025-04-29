from django.db import models
from base.models import Base

class Exercicio(Base):
    """
    Modelo de Dados para Exercicio
    """
    nome = models.CharField("Nome", max_length=255)
    descricao = models.TextField("Descrição")
    categoria = models.CharField("Categoria", max_length=255)
    equipamento = models.CharField("Equipamento", max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome
