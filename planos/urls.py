from django.urls import path

from .views import (PlanoListCreateView, PlanoRetrieveUpdateDestroyView, ModalidadeListCreateView,
                    ModalidadeRetrieveUpdateDestroyView, PlanoModalidadeListCreateView, PlanoModalidadeRetrieveUpdateDestroyView)

urlpatterns = [
    path('', PlanoListCreateView.as_view(), name='planos'),
    path('<int:pk>/', PlanoRetrieveUpdateDestroyView.as_view(), name='plano'),
    path('modalidades/', ModalidadeListCreateView.as_view(), name='modalidades'),
    path('modalidades/<int:pk>/', ModalidadeRetrieveUpdateDestroyView.as_view(), name='modalidade'),
    path('planosmodalidades/', PlanoModalidadeListCreateView.as_view(), name='planosmodalidades'),
    path('planosmodalidades/<int:pk>/', PlanoModalidadeRetrieveUpdateDestroyView.as_view(), name='planosmodalidade'),
]