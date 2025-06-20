# Importa AppConfig para configuração do app Django
from django.apps import AppConfig


class PlanosConfig(AppConfig):
    # Define o tipo padrão para campos auto-incrementais das tabelas desse app
    default_auto_field = 'django.db.models.BigAutoField'

    # Nome do app, usado internamente pelo Django
    name = 'planos'
