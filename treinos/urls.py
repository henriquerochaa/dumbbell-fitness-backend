from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import TreinoViewSet

router = DefaultRouter()
router.register('', TreinoViewSet)
router

urlpatterns = router.urls