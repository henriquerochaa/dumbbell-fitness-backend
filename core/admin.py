from django.contrib import admin
from core.models import EnderecoModel

admin.site.register(EnderecoModel)  
class EnderecoModelAdmin(admin.ModelAdmin):
    list_display = ('cep', 'rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado')
