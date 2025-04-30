from django.contrib import admin

from planos.models import Plano, Modalidade, PlanoModalidade


@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'valor', 'criacao', 'atualizacao', 'ativo')


@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoria', 'criacao', 'atualizacao', 'ativo')


@admin.register(PlanoModalidade)
class PlanoModalidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'plano', 'modalidade', 'criacao', 'atualizacao', 'ativo')