from django.urls import path

from .views import TreinoListCreateView, TreinoRetrieveUpdateDestroyView

urlpatterns = [
    path('', TreinoListCreateView.as_view(), name='treinos'),
    path('<int:pk>/', TreinoRetrieveUpdateDestroyView.as_view(), name='treino'),
]