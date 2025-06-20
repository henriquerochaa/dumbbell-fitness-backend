# Importa AppConfig para configurar apps Django
from django.apps import AppConfig


class ExerciciosConfig(AppConfig):
    # Define o tipo padrão para campos auto-incrementais (PKs) nas tabelas desse app
    default_auto_field = 'django.db.models.BigAutoField'

    # Nome do app Django, usado para referenciar internamente
    name = 'exercicios'
