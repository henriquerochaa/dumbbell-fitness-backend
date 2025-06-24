# Importa o módulo models do Django para criar classes que viram tabelas no banco
from django.db import models

# Importa BaseModel do core, que centraliza campos comuns (timestamps, id, etc)
from core.models import BaseModel

# Importa opções predefinidas para categorias de modalidades de exercícios
from core.choices import CATEGORIA_MODALIDADES

# Importa opções predefinidas para grupos musculares
from core.choices import GRUPO_MUSCULAR


class Exercicio(BaseModel):
    """
    Representa um exercício físico com nome, descrição, categoria e equipamento.

    Campos:
    - nome: nome do exercício (obrigatório)
    - descricao: texto detalhado do exercício
    - categoria: modalidade do exercício, com opções pré-definidas
    - equipamento: equipamento necessário (opcional)
    """

    nome = models.CharField("Nome", max_length=255)
    descricao = models.TextField("Descrição")
    categoria = models.CharField(
        "Categoria", max_length=30, choices=CATEGORIA_MODALIDADES)
    grupo_muscular = models.CharField(
        "Grupo Muscular", max_length=30, choices=GRUPO_MUSCULAR, default='Outros')
    equipamento = models.CharField(
        "Equipamento", max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome  # Exibe o nome no admin e em outras referências
