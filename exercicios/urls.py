from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ExercicioViewSet

router = DefaultRouter()
router.register('exercicios', ExercicioViewSet)

urlpatterns = router.urls