from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UsuarioViewSet, PersonaViewSet, ImagenViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'personas', PersonaViewSet, basename='persona')
router.register(r'imagenes', ImagenViewSet, basename='imagen')

urlpatterns = [
    path('', include(router.urls)),
]
