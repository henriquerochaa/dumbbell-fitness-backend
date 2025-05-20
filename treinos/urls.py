from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import TreinoViewSet

router = DefaultRouter()
router.register('treino', TreinoViewSet)

urlpatterns = router.urls