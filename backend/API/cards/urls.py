from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MazoViewSet, CartaPersonajeViewSet, CartaNegocioViewSet, CartaEspecialViewSet

router = DefaultRouter()
router.register(r'mazos', MazoViewSet, basename='mazo')
router.register(r'personajes', CartaPersonajeViewSet, basename='carta-personaje')
router.register(r'negocios', CartaNegocioViewSet, basename='carta-negocio')
router.register(r'especiales', CartaEspecialViewSet, basename='carta-especial')

urlpatterns = [
    path('', include(router.urls)),
]
