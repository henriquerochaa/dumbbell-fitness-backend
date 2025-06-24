# Importa classes para views genéricas e viewsets do DRF
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

# Importa os modelos que serão manipulados nas views
from .models import Plano, Modalidade, PlanoModalidade

# Importa os serializers responsáveis pela conversão dos dados
from .serializers import PlanoSerializer, ModalidadeSerializer, PlanoModalidadeSerializer, UserSerializer

# Importa o modelo User do Django
from django.contrib.auth.models import User

# Importa o modelo Matricula para remover referências
from cadastros.models import Matricula


@api_view(['GET'])
@permission_classes([AllowAny])
def planos_list(request):
    """
    View para listar todos os planos ativos.
    
    Permite acesso sem autenticação para visualização dos planos disponíveis.
    """
    planos = Plano.objects.filter(ativo=True).order_by('preco')
    serializer = PlanoSerializer(planos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def plano_detail(request, pk):
    """
    View para obter detalhes de um plano específico.
    
    Requer autenticação para acessar informações detalhadas do plano.
    """
    try:
        plano = Plano.objects.get(pk=pk, ativo=True)
        serializer = PlanoSerializer(plano)
        return Response(serializer.data)
    except Plano.DoesNotExist:
        return Response(
            {'error': 'Plano não encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )


class CustomAuthToken(ObtainAuthToken):
    """
    View customizada para autenticação que retorna token + dados do usuário.
    
    Estende a funcionalidade padrão do ObtainAuthToken para incluir
    informações do usuário na resposta.
    """
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """
    View para retornar informações do usuário logado.
    
    Requer autenticação e retorna dados do usuário atual.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class PlanoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD no modelo Plano.

    Permite criar, listar, atualizar e deletar registros de planos.
    """
    queryset = Plano.objects.all().order_by('id')
    serializer_class = PlanoSerializer
    permission_classes = [IsAuthenticated]  # Adiciona autenticação obrigatória

    def destroy(self, request, *args, **kwargs):
        """
        Sobrescreve o método destroy para remover matrículas relacionadas
        antes de deletar o plano.
        
        Isso evita o erro ProtectedError quando o plano está sendo usado
        em matrículas.
        """
        plano = self.get_object()
        
        try:
            # Remove todas as matrículas relacionadas ao plano
            matriculas = Matricula.objects.filter(plano=plano)
            count_matriculas = matriculas.count()
            
            if count_matriculas > 0:
                matriculas.delete()
                print(f"Removidas {count_matriculas} matrículas do plano '{plano.titulo}'")
            
            # Remove relacionamentos PlanoModalidade
            plano_modalidades = PlanoModalidade.objects.filter(plano=plano)
            count_modalidades = plano_modalidades.count()
            
            if count_modalidades > 0:
                plano_modalidades.delete()
                print(f"Removidas {count_modalidades} relações de modalidade do plano '{plano.titulo}'")
            
            # Agora pode deletar o plano com segurança
            self.perform_destroy(plano)
            
            return Response(
                {
                    'message': f'Plano "{plano.titulo}" deletado com sucesso.',
                    'matriculas_removidas': count_matriculas,
                    'modalidades_removidas': count_modalidades
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {
                    'error': f'Erro ao deletar plano: {str(e)}'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ModalidadeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD no modelo Modalidade.

    Permite criar, listar, atualizar e deletar registros de modalidades.
    """
    queryset = Modalidade.objects.all().order_by('id')
    serializer_class = ModalidadeSerializer


class PlanoModalidadeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD no modelo PlanoModalidade.

    Permite criar, listar, atualizar e deletar registros que relacionam planos e modalidades.
    """
    queryset = PlanoModalidade.objects.all().order_by('id')
    serializer_class = PlanoModalidadeSerializer
