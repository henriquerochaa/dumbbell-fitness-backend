# Importa o módulo admin do Django para registrar modelos na interface administrativa
from django.contrib import admin

# Importa os modelos Plano, Modalidade e PlanoModalidade para serem gerenciados no admin
from planos.models import Plano, Modalidade, PlanoModalidade


# Registra o modelo Plano no admin com configuração personalizada
@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    # Campos exibidos na lista de registros do admin para facilitar a visualização
    list_display = ('id', 'nome', 'valor', 'criacao', 'atualizacao', 'ativo')


# Registra o modelo Modalidade no admin com configuração personalizada
@admin.register(Modalidade)
class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoria', 'criacao', 'atualizacao', 'ativo')


# Registra o modelo PlanoModalidade no admin com configuração personalizada
@admin.register(PlanoModalidade)
class PlanoModalidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'plano', 'modalidade',
                    'criacao', 'atualizacao', 'ativo')
