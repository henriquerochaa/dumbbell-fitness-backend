from django.contrib import admin
from .models import Aluno, Matricula, Cartao


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    # Mostra esses campos na lista de alunos no admin
    list_display = ('id', 'nome', 'ativo', 'criacao', 'atualizacao')


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    # Lista as matrículas com info de aluno, plano e status
    list_display = ('aluno', 'plano', 'ativo', 'criacao', 'atualizacao')


@admin.register(Cartao)
class CartaoAdmin(admin.ModelAdmin):
    # Mostra dados do cartão, incluindo titular, validade e status
    list_display = ('aluno', 'nome_titular', 'data_validade',
                    'bandeira_cartao', 'criacao', 'atualizacao', 'ativo')
