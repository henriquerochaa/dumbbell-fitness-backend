# Importa os viewsets prontos do DRF para operações CRUD automáticas
from rest_framework import viewsets
# Importa o objeto Response para retornar dados HTTP nas views
from rest_framework.response import Response

# Importa o modelo que representa o endereço no banco
from .models import EnderecoModel
# Importa o serializer para converter e validar os dados do endereço
from .serializers import EnderecoSerializer


class EnderecoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento completo dos endereços.

    Fornece endpoints para:
        - Listar todos os endereços ordenados pelo ID decrescente (mais recentes primeiro)
        - Criar novos endereços
        - Atualizar endereços existentes
        - Deletar endereços pelo ID

    Utiliza o serializer EnderecoSerializer para validação e formatação dos dados.
    """

    queryset = EnderecoModel.objects.all().order_by('-id')
    serializer_class = EnderecoSerializer

    def list(self, request, *args, **kwargs):
        """
        Retorna a lista completa de endereços serializados.

        Sobrescreve o método list padrão para garantir uso do serializer correto
        e permitir futura customização se necessário.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
