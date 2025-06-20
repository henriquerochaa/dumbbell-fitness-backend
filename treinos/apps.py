# Importa a classe base para configuração do app Django
from django.apps import AppConfig


class TreinosConfig(AppConfig):
    # Define o tipo padrão para os campos auto-incrementais das tabelas
    default_auto_field = 'django.db.models.BigAutoField'

    # Nome do app usado pelo Django para referência interna
    name = 'treinos'
