# Importa o módulo admin do Django para registrar modelos na interface administrativa
from django.contrib import admin

# Importa o modelo Treino para gerenciar no admin
from .models import Treino


@admin.register(Treino)
class TreinoAdmin(admin.ModelAdmin):
    # Define os campos exibidos na listagem do admin para facilitar a visualização
    list_display = ('aluno', 'objetivo', 'disponibilidade',
                    'criacao', 'atualizacao', 'ativo')

    # Métodos para mostrar peso e altura do aluno no admin, se quiser adicionar depois
    def peso(self, obj):
        return obj.aluno.peso

    def altura(self, obj):
        return obj.aluno.altura
