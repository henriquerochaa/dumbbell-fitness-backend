from django.contrib import admin

from .models import Aluno, Matricula, Estado, Municipio, Cartao


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'ativo', 'criacao', 'atualizacao')


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'plano', 'ativo', 'criacao', 'atualizacao')


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estado', 'criacao', 'atualizacao', 'ativo')


@admin.register(Cartao)
class CartaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'nome_titular', 'data_validade', 'bandeira_cartao', 'criacao', 'atualizacao', 'ativo')
