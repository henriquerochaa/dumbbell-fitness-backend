from django.urls import path

from .views import AlunoListCreateView, AlunoRetrieveUpdateDestroyView, MatriculaListCreateView, MatriculaRetrieveUpdateDestroyView

urlpatterns = [
    path('', AlunoListCreateView.as_view(), name='alunos'),
    path('<int:pk>/', AlunoRetrieveUpdateDestroyView.as_view(), name='aluno'),
    path('matriculas/', MatriculaListCreateView.as_view(), name='matriculas'),
    path('matriculas/<int:pk>/', MatriculaRetrieveUpdateDestroyView.as_view(), name='matricula'),
]
