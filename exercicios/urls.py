from django.urls import path

from .views import ExercicioListCreateView, ExercicioRetrieveUpdateDestroyView

urlpatterns = [
    path('exercicios/', ExercicioListCreateView.as_view(), name='exercicios'),
    path('exercicios/<int:pk>/', ExercicioRetrieveUpdateDestroyView.as_view(), name='exercicio'),
]