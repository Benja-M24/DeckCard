from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Mazo, CartaNegocio, CartaPersonaje, CartaEspecial
from .serializers import (
    MazoSerializer, 
    CartaNegocioSerializer, 
    CartaPersonajeSerializer, 
    CartaEspecialSerializer
)

# Create your views here.

class MazoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver y editar mazos.
    """
    queryset = Mazo.objects.all()
    serializer_class = MazoSerializer
    
    @action(detail=True, methods=['get'])
    def cartas(self, request, pk=None):
        """
        Obtiene todas las cartas asociadas a un mazo específico
        """
        mazo = self.get_object()
        
        # Obtener cartas por tipo
        cartas_personaje = CartaPersonaje.objects.filter(mazo=mazo)
        cartas_negocio = CartaNegocio.objects.filter(mazo=mazo)
        cartas_especiales = CartaEspecial.objects.filter(mazo=mazo)
        
        # Serializar cada tipo de carta
        personajes_data = CartaPersonajeSerializer(cartas_personaje, many=True).data
        negocios_data = CartaNegocioSerializer(cartas_negocio, many=True).data
        especiales_data = CartaEspecialSerializer(cartas_especiales, many=True).data
        
        # Agrupar todos los resultados
        result = {
            'personajes': personajes_data,
            'negocios': negocios_data,
            'especiales': especiales_data
        }
        
        return Response(result)

class CartaPersonajeViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver y editar cartas de personaje.
    """
    serializer_class = CartaPersonajeSerializer
    
    def get_queryset(self):
        """
        Este método permite filtrar las cartas de personaje por mazo.
        Se puede filtrar agregando ?mazo=<id_del_mazo> a la URL.
        """
        queryset = CartaPersonaje.objects.all()
        mazo_id = self.request.query_params.get('mazo', None)
        if mazo_id is not None:
            queryset = queryset.filter(mazo__id=mazo_id)
        return queryset

class CartaNegocioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver y editar cartas de negocio.
    """
    serializer_class = CartaNegocioSerializer
    
    def get_queryset(self):
        """
        Este método permite filtrar las cartas de negocio por mazo.
        Se puede filtrar agregando ?mazo=<id_del_mazo> a la URL.
        """
        queryset = CartaNegocio.objects.all()
        mazo_id = self.request.query_params.get('mazo', None)
        if mazo_id is not None:
            queryset = queryset.filter(mazo__id=mazo_id)
        return queryset

class CartaEspecialViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver y editar cartas especiales.
    """
    serializer_class = CartaEspecialSerializer
    def get_queryset(self):
        """
        Este método permite filtrar las cartas de personaje por mazo.
        Se puede filtrar agregando ?mazo=<id_del_mazo> a la URL.
        """
        queryset = CartaEspecial.objects.all()
        mazo_id = self.request.query_params.get('mazo', None)
        if mazo_id is not None:
            queryset = queryset.filter(mazo__id=mazo_id)
        return queryset

