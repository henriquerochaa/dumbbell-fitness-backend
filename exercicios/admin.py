# Importa o módulo admin do Django para registrar modelos na interface administrativa
from django.contrib import admin

# Importa o modelo Exercicio para gerenciar pelo admin
from .models import Exercicio

# Registra o modelo Exercicio na interface admin com configurações personalizadas


@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    # Define os campos que aparecem na lista de registros do admin
    list_display = ('nome', 'categoria', 'equipamento',
                    'atualizacao', 'criacao', 'ativo')
