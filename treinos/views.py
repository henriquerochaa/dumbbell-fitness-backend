from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Treino
from .serializers import TreinoSerializer


class TreinoViewSet(viewsets.ModelViewSet):
    queryset = Treino.objects.all()
    serializer_class = TreinoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(aluno__user=user)

    def perform_create(self, serializer):
        serializer.save(aluno=self.request.user.aluno)
