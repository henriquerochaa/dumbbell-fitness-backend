# =============================================================================
# ARQUIVO: cadastros/views.py
# DESCRIÇÃO: ViewSets para gerenciamento de cadastros do projeto Dumbbell Fitness
# FUNÇÃO: Define endpoints da API para alunos, matrículas e cartões
# =============================================================================

from rest_framework import viewsets, mixins, serializers, status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Aluno, Matricula, Cartao
from .serializers import AlunoSerializer, MatriculaSerializer, CartaoSerializer


class AlunoViewSet(viewsets.ModelViewSet, UpdateModelMixin):
    """
    ViewSet completo para o recurso Aluno.
    
    Fornece endpoints RESTful completos para gerenciamento de alunos:
    - GET /api/v1/cadastros/alunos/ - Lista todos os alunos
    - POST /api/v1/cadastros/alunos/ - Cria novo aluno (sem autenticação)
    - GET /api/v1/cadastros/alunos/{id}/ - Obtém aluno específico
    - PUT /api/v1/cadastros/alunos/{id}/ - Atualiza aluno
    - DELETE /api/v1/cadastros/alunos/{id}/ - Remove aluno
    
    Funcionalidades especiais:
    - Permite criação sem autenticação (cadastro público)
    - Exige autenticação para outras operações
    - Remove usuário vinculado ao deletar aluno
    """
    queryset = Aluno.objects.all().order_by('id')
    serializer_class = AlunoSerializer

    def get_permissions(self):
        """
        Define permissões baseadas na ação sendo executada.
        
        - Criação (create): Permite acesso sem autenticação (AllowAny)
        - Outras ações: Exige usuário autenticado (IsAuthenticated)
        
        Returns:
            list: Lista de classes de permissão
        """
        if self.action == 'create':
            return [AllowAny()]  # Cadastro público
        return [IsAuthenticated()]  # Outras operações precisam de login

    def get_queryset(self):
        """
        Retorna alunos conforme filtros aplicados.
        
        Permite filtrar alunos por diferentes critérios:
        - Por usuário: ?user=id
        - Por nome: ?nome=nome
        - Por email: ?email=email
        
        Returns:
            QuerySet: Alunos filtrados conforme parâmetros
        """
        queryset = Aluno.objects.all().order_by('id')
        
        # Filtro por usuário
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        
        # Filtro por nome
        nome = self.request.query_params.get('nome', None)
        if nome is not None:
            queryset = queryset.filter(nome__icontains=nome)
        
        # Filtro por email
        email = self.request.query_params.get('email', None)
        if email is not None:
            queryset = queryset.filter(email__icontains=email)
        
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Retorna lista paginada dos alunos.
        
        Sobrescreve o método padrão para garantir uso do serializer correto
        e permitir futuras customizações.
        
        Args:
            request: Requisição HTTP
            *args: Argumentos posicionais
            **kwargs: Argumentos nomeados
            
        Returns:
            Response: Lista de alunos serializados
        """
        queryset = self.get_queryset()
        
        # Filtrar por usuário se especificado
        user_id = request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
            print(f"Filtrando alunos por usuário: {user_id}")
        
        print(f"Total de alunos encontrados: {queryset.count()}")
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Sobrescreve a exclusão para apagar o usuário relacionado antes de deletar o aluno.
        
        Quando um aluno é deletado, o usuário do Django vinculado também é removido
        para evitar dados órfãos no sistema.
        
        Args:
            request: Requisição HTTP
            *args: Argumentos posicionais
            **kwargs: Argumentos nomeados
            
        Returns:
            Response: Status 204 (No Content) em caso de sucesso
        """
        aluno = self.get_object()
        user = aluno.user
        
        # Remove o usuário vinculado primeiro
        if user:
            user.delete()  # Apaga usuário associado primeiro
            
        # Depois remove o aluno
        self.perform_destroy(aluno)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MatriculaViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para o recurso Matrícula.
    
    Fornece endpoints RESTful completos para gerenciamento de matrículas:
    - GET /api/v1/cadastros/matriculas/ - Lista todas as matrículas ativas
    - POST /api/v1/cadastros/matriculas/ - Cria nova matrícula
    - GET /api/v1/cadastros/matriculas/{id}/ - Obtém matrícula específica
    - PUT /api/v1/cadastros/matriculas/{id}/ - Atualiza matrícula
    - DELETE /api/v1/cadastros/matriculas/{id}/ - Remove matrícula (soft delete)
    
    Funcionalidades:
    - Gerencia relacionamentos entre aluno, plano e cartão
    - Valida regras de negócio via serializer
    - Exige autenticação para todas as operações
    - Filtra apenas matrículas ativas por padrão
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MatriculaSerializer

    def get_queryset(self):
        """
        Retorna apenas matrículas ativas.
        
        Filtra automaticamente por matrículas com ativo=True.
        Permite filtros adicionais via query parameters.
        
        Returns:
            QuerySet: Matrículas ativas filtradas
        """
        queryset = Matricula.objects.filter(ativo=True).order_by('id')
        
        # Filtrar por aluno se especificado
        aluno_id = self.request.query_params.get('aluno')
        if aluno_id:
            queryset = queryset.filter(aluno_id=aluno_id)
            print(f"Filtrando matrículas por aluno: {aluno_id}")
        
        print(f"Total de matrículas ativas encontradas: {queryset.count()}")
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Retorna lista paginada das matrículas ativas.
        
        Sobrescreve o método padrão para garantir uso do serializer correto
        e permitir futuras customizações.
        
        Args:
            request: Requisição HTTP
            *args: Argumentos posicionais
            **kwargs: Argumentos nomeados
            
        Returns:
            Response: Lista de matrículas serializadas
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        """
        Realiza soft delete da matrícula.
        
        Em vez de deletar fisicamente, marca como inativa (ativo=False).
        Isso preserva o histórico e permite reativação se necessário.
        
        Args:
            instance: Instância da matrícula a ser desativada
        """
        instance.ativo = False
        instance.save()
        print(f"Matrícula {instance.id} desativada (soft delete)")

    def perform_create(self, serializer):
        """
        Controla a criação da matrícula.
        
        Define automaticamente o aluno da matrícula baseado no usuário logado:
        - Superusuários precisam informar o 'aluno' no corpo da requisição
        - Usuários comuns criam matrícula vinculada a si mesmos
        
        Args:
            serializer: Serializer da matrícula
            
        Raises:
            ValidationError: Se superusuário não informar aluno
        """
        if self.request.user.is_superuser:
            # Superusuário precisa especificar o aluno
            aluno_id = self.request.data.get('aluno')
            if not aluno_id:
                raise serializers.ValidationError(
                    {'aluno': 'Campo aluno é obrigatório para criar matrícula.'})
            try:
                aluno = Aluno.objects.get(pk=aluno_id)
            except Aluno.DoesNotExist:
                raise serializers.ValidationError(
                    {'aluno': 'Aluno não encontrado.'})
        else:
            # Usuário comum cria matrícula para si mesmo
            try:
                aluno = Aluno.objects.get(user=self.request.user)
            except Aluno.DoesNotExist:
                raise serializers.ValidationError(
                    {'aluno': 'Aluno não encontrado para este usuário.'})

        # Remove o campo aluno dos dados se existir (para usuários comuns)
        if not self.request.user.is_superuser and 'aluno' in serializer.validated_data:
            del serializer.validated_data['aluno']

        # Garante que a matrícula seja criada como ativa
        serializer.save(aluno=aluno, ativo=True)
        print(f"Nova matrícula criada para aluno {aluno.id}")


class CartaoViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """
    ViewSet customizado para Cartão.
    
    Fornece endpoints RESTful para gerenciamento de cartões com regras específicas:
    - GET /api/v1/cadastros/cartoes/ - Lista cartões (filtrados por usuário)
    - POST /api/v1/cadastros/cartoes/ - Cria novo cartão
    - GET /api/v1/cadastros/cartoes/{id}/ - Obtém cartão específico
    - PUT /api/v1/cadastros/cartoes/{id}/ - Atualiza cartão
    - DELETE /api/v1/cadastros/cartoes/{id}/ - Remove cartão
    
    Regras de permissão:
    - Apenas usuários autenticados acessam
    - Superusuários podem ver e manipular todos os cartões
    - Usuários comuns só podem mexer nos seus próprios cartões
    """
    permission_classes = [IsAuthenticated]
    queryset = Cartao.objects.all().order_by('id')
    serializer_class = CartaoSerializer

    def get_queryset(self):
        """
        Retorna cartões conforme o perfil do usuário.
        
        Filtra os cartões baseado no tipo de usuário:
        - Superusuários: Veem todos os cartões
        - Usuários comuns: Veem apenas seus próprios cartões
        
        Returns:
            QuerySet: Cartões filtrados conforme permissões
        """
        if self.request.user.is_superuser:
            return Cartao.objects.all()  # Superusuário vê tudo
        
        # Usuário comum vê só os seus cartões
        try:
            aluno = Aluno.objects.get(user=self.request.user)
            return Cartao.objects.filter(aluno=aluno)
        except Aluno.DoesNotExist:
            return Cartao.objects.none()  # Retorna queryset vazio se não encontrar aluno

    def perform_create(self, serializer):
        """
        Controla a criação do cartão.
        
        Define automaticamente o aluno dono do cartão baseado no usuário logado:
        - Superusuários precisam informar o 'aluno' no corpo da requisição
        - Usuários comuns criam cartão vinculado a si mesmos
        
        Args:
            serializer: Serializer do cartão
            
        Raises:
            ValidationError: Se superusuário não informar aluno
        """
        if self.request.user.is_superuser:
            # Superusuário precisa especificar o aluno
            aluno_id = self.request.data.get('aluno')
            if not aluno_id:
                raise serializers.ValidationError(
                    {'aluno': 'Campo aluno é obrigatório para criar cartão.'})
            try:
                aluno = Aluno.objects.get(pk=aluno_id)
            except Aluno.DoesNotExist:
                raise serializers.ValidationError(
                    {'aluno': 'Aluno não encontrado.'})
        else:
            # Usuário comum cria cartão para si mesmo
            try:
                aluno = Aluno.objects.get(user=self.request.user)
            except Aluno.DoesNotExist:
                raise serializers.ValidationError(
                    {'aluno': 'Aluno não encontrado para este usuário.'})

        # Remove o campo aluno dos dados se existir (para usuários comuns)
        if not self.request.user.is_superuser and 'aluno' in serializer.validated_data:
            del serializer.validated_data['aluno']

        serializer.save(aluno=aluno)

    def perform_destroy(self, instance):
        """
        Impede que usuário comum delete cartão de outro aluno.
        
        Valida se o usuário tem permissão para deletar o cartão:
        - Superusuário tem permissão total
        - Usuário comum só pode deletar seus próprios cartões
        
        Args:
            instance: Instância do cartão a ser deletado
            
        Raises:
            PermissionDenied: Se usuário não tem permissão
        """
        if not self.request.user.is_superuser:
            try:
                aluno = Aluno.objects.get(user=self.request.user)
                if instance.aluno != aluno:
                    raise PermissionDenied(
                        "Você não pode deletar o cartão de outro aluno.")
            except Aluno.DoesNotExist:
                raise PermissionDenied(
                    "Aluno não encontrado para este usuário.")
        instance.delete()

    def perform_update(self, serializer):
        """
        Controla atualização do cartão.
        
        Aplica as mesmas regras de permissão da exclusão:
        - Superusuário pode atualizar qualquer cartão
        - Usuário comum só pode atualizar seus próprios cartões
        
        Args:
            serializer: Serializer do cartão
            
        Raises:
            PermissionDenied: Se usuário não tem permissão
        """
        instance = self.get_object()
        if not self.request.user.is_superuser:
            try:
                aluno = Aluno.objects.get(user=self.request.user)
                if instance.aluno != aluno:
                    raise PermissionDenied(
                        "Você não pode atualizar o cartão de outro aluno.")
            except Aluno.DoesNotExist:
                raise PermissionDenied(
                    "Aluno não encontrado para este usuário.")
        serializer.save()
