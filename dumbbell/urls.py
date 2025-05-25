from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token  # 🔥 essa linha aqui

from cadastros.urls import router as cadastros_router
from exercicios.urls import router as exercicios_router
from planos.urls import router as planos_router
from treinos.urls import router as treinos_router

urlpatterns = [

    path('api/v1/cadastros/', include(cadastros_router.urls)),
    path('api/v1/exercicios/', include(exercicios_router.urls)),
    path('api/v1/planos/', include(planos_router.urls)),
    path('api/v1/treinos/', include(treinos_router.urls)),


    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
]
