from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MazoViewSet, CartaPersonajeViewSet, CartaNegocioViewSet, CartaEspecialViewSet, RoomViewSet, ParticipantViewSet

router = DefaultRouter()
router.register(r'mazos', MazoViewSet, basename='mazo')
router.register(r'personajes', CartaPersonajeViewSet, basename='carta-personaje')
router.register(r'negocios', CartaNegocioViewSet, basename='carta-negocio')
router.register(r'especiales', CartaEspecialViewSet, basename='carta-especial')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'participants', ParticipantViewSet, basename='participant')

urlpatterns = [
    path('', include(router.urls)),
]
