from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Treino
from .serializers import TreinoSerializer

class TreinoViewSet(viewsets.ModelViewSet):
    queryset = Treino.objects.all().order_by('id')
    serializer_class = TreinoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(aluno__user=user)

    def perform_create(self, serializer):
        serializer.save(aluno=self.request.user.aluno)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
