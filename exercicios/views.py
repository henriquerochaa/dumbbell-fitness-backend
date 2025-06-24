# Importa o módulo viewsets do DRF, que facilita criar CRUDs completos com pouco código
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Importa o modelo Exercicio para manipulação de dados
from .models import Exercicio

# Importa o serializer que transforma dados do modelo em JSON e vice-versa
from .serializers import ExercicioSerializer

# Importa o modelo ExercicioTreino para remover referências
from treinos.models import ExercicioTreino


class ExercicioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar operações CRUD no modelo Exercicio.

    Permite criar, listar, atualizar e deletar registros de exercícios,
    utilizando o serializer ExercicioSerializer para conversão dos dados.
    
    Acesso público - qualquer pessoa pode ver os exercícios disponíveis.
    """

    queryset = Exercicio.objects.all().order_by('id')
    serializer_class = ExercicioSerializer
    permission_classes = [AllowAny]  # Permite acesso público aos exercícios

    def destroy(self, request, *args, **kwargs):
        """
        Sobrescreve o método destroy para remover referências do exercício
        nos treinos antes de deletar o exercício.
        
        Isso evita o erro ProtectedError quando o exercício está sendo usado
        em treinos.
        """
        exercicio = self.get_object()
        
        try:
            # Remove todas as referências do exercício nos treinos
            exercicios_treino = ExercicioTreino.objects.filter(exercicio=exercicio)
            count_removidos = exercicios_treino.count()
            
            if count_removidos > 0:
                exercicios_treino.delete()
                print(f"Removidas {count_removidos} referências do exercício '{exercicio.nome}' nos treinos")
            
            # Agora pode deletar o exercício com segurança
            self.perform_destroy(exercicio)
            
            return Response(
                {
                    'message': f'Exercício "{exercicio.nome}" deletado com sucesso.',
                    'referencias_removidas': count_removidos
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {
                    'error': f'Erro ao deletar exercício: {str(e)}'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
