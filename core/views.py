# =============================================================================
# ARQUIVO: core/views.py
# DESCRIÇÃO: ViewSets para funcionalidades compartilhadas do projeto Dumbbell Fitness
# FUNÇÃO: Define endpoints da API para endereços e outras funcionalidades base
# =============================================================================

# Importa os viewsets prontos do DRF para operações CRUD automáticas
from rest_framework import viewsets
# Importa o objeto Response para retornar dados HTTP nas views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

# Importa o modelo que representa o endereço no banco
from .models import EnderecoModel
# Importa o serializer para converter e validar os dados do endereço
from .serializers import EnderecoSerializer


class EnderecoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento completo dos endereços.
    
    Fornece endpoints RESTful completos para gerenciamento de endereços:
    - GET /api/v1/cadastros/endereco/ - Lista todos os endereços
    - POST /api/v1/cadastros/endereco/ - Cria novo endereço (sem autenticação)
    - GET /api/v1/cadastros/endereco/{id}/ - Obtém endereço específico
    - PUT /api/v1/cadastros/endereco/{id}/ - Atualiza endereço
    - DELETE /api/v1/cadastros/endereco/{id}/ - Remove endereço
    
    Funcionalidades:
    - Permite criação sem autenticação (para cadastro de alunos)
    - Exige autenticação para outras operações
    - Validação automática de CEP e outros campos
    - Ordenação por data de criação (mais recentes primeiro)
    
    Este ViewSet é usado pelo app cadastros para gerenciar endereços
    que são vinculados aos alunos durante o processo de cadastro.
    """

    # QuerySet base para endereços, ordenado por data de criação decrescente
    queryset = EnderecoModel.objects.all().order_by('-id')
    
    # Serializer usado para converter dados
    serializer_class = EnderecoSerializer

    def get_permissions(self):
        """
        Define permissões baseadas na ação sendo executada.
        
        - Criação (create): Permite acesso sem autenticação (AllowAny)
          Isso permite que novos alunos criem endereços durante o cadastro
        - Outras ações: Exige usuário autenticado (IsAuthenticated)
          Para listar, editar ou deletar endereços
        
        Returns:
            list: Lista de classes de permissão
        """
        if self.action == 'create':
            return [AllowAny()]  # Criação pública para cadastro
        return [IsAuthenticated()]  # Outras operações precisam de login

    def list(self, request, *args, **kwargs):
        """
        Retorna a lista completa de endereços serializados.
        
        Sobrescreve o método list padrão para garantir uso do serializer correto
        e permitir futura customização se necessário.
        
        Args:
            request: Requisição HTTP
            *args: Argumentos posicionais
            **kwargs: Argumentos nomeados
            
        Returns:
            Response: Lista de endereços serializados
            
        Nota:
            Este método pode ser customizado no futuro para adicionar
            filtros, paginação ou outras funcionalidades específicas.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
