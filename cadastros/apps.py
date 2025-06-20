from django.apps import AppConfig


class AlunosConfig(AppConfig):
    # Deixa o campo ID com bigint por padrão, pra não faltar espaço
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cadastros'  # Nome do app que vai ser usado nas configurações do projeto
