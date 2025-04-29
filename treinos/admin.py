from django.contrib import admin

from .models import Treino


@admin.register(Treino)
class TreinoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'objetivo', 'disponibilidade', 'criacao', 'atualizacao', 'ativo')

    def peso(self, obj):
        return obj.aluno.peso

    def altura(self, obj):
        return obj.aluno.altura
