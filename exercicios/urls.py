from django.urls import path

from .views import ExercicioListCreateView, ExercicioRetrieveUpdateDestroyView

urlpatterns = [
    path('', ExercicioListCreateView.as_view(), name='exercicios'),
    path('<int:pk>/', ExercicioRetrieveUpdateDestroyView.as_view(), name='exercicio'),
]