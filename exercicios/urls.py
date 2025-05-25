
from rest_framework.routers import DefaultRouter

from .views import ExercicioViewSet

router = DefaultRouter()
router.register('', ExercicioViewSet)

urlpatterns = router.urls