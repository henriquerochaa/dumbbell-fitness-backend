from django.contrib import admin

from .models import Aluno, Matricula


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'ativo', 'criacao', 'atualizacao')


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'plano', 'ativo', 'criacao', 'atualizacao')
