from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VersionViewSet, 
    CartaPersonajeViewSet, 
    CartaNegocioViewSet, 
    CartaEspecialViewSet, 
    CartaEventoViewSet, 
    CartaObjetivoViewSet, 
    RoomViewSet, 
    ParticipantViewSet,
)

router = DefaultRouter()
router.register(r'versions', VersionViewSet, basename='version')
router.register(r'personajes', CartaPersonajeViewSet, basename='carta-personaje')
router.register(r'negocios', CartaNegocioViewSet, basename='carta-negocio')
router.register(r'especiales', CartaEspecialViewSet, basename='carta-especial')
router.register(r'eventos', CartaEventoViewSet, basename='carta-evento')
router.register(r'objetivos', CartaObjetivoViewSet, basename='carta-objetivo')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'participants', ParticipantViewSet, basename='participant')

urlpatterns = [
    path('', include(router.urls)),
]
