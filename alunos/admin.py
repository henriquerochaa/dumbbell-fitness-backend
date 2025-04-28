from django.contrib import admin

from alunos.models import Aluno, Matricula


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'status', 'criacao', 'atualizacao')


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'plano', 'status', 'criacao', 'atualizacao')
