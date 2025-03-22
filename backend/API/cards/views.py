from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Mazo, CartaNegocio, CartaPersonaje, CartaEspecial, Room, Participant
from .serializers import (
    MazoSerializer, 
    CartaNegocioSerializer, 
    CartaPersonajeSerializer, 
    CartaEspecialSerializer,
    RoomSerializer,
    RoomCreateSerializer,
    ParticipantSerializer,
    ParticipantCreateSerializer
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


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar salas de juego.
    """
    queryset = Room.objects.all()
    
    def get_serializer_class(self):
        # Room.clean_older_rooms()
        if self.action == 'create':
            return RoomCreateSerializer
        return RoomSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retorna los detalles de una sala específica por su código o ID.
        """
        # Permite buscar por código o por id
        lookup_field = kwargs.get('pk')
        
        # Intentamos encontrar la sala
        try:
            # Primero intentamos buscar por código
            if not lookup_field.isdigit():
                room = Room.objects.get(code=lookup_field)
            else:
                # Si es un número, intentamos buscar por id
                room = Room.objects.get(pk=lookup_field)
                
            serializer = self.get_serializer(room)
            return Response({
                'success': True,
                'room': serializer.data
            })
        except Room.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Sala no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get', 'post'])
    def participants(self, request, pk=None):
        """
        Obtiene o añade participantes a una sala específica.
        """
        try:
            # Permite buscar por código o por id
            if not pk.isdigit():
                room = Room.objects.get(code=pk)
            else:
                room = Room.objects.get(pk=pk)
            
            # Distinguir entre GET y POST
            if request.method == 'GET':
                participants = Participant.objects.filter(room=room)
                serializer = ParticipantSerializer(participants, many=True)
                return Response(serializer.data)
            
            elif request.method == 'POST':
                # Verificar si la sala está llena
                if room.is_full:
                    return Response({
                        'success': False,
                        'error': 'La sala está llena'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Crear un nuevo participante
                serializer = ParticipantCreateSerializer(data=request.data)
                if serializer.is_valid():
                    # Asignar la sala al participante
                    serializer.save(room=room)
                    return Response({
                        'success': True,
                        'participant': serializer.data
                    }, status=status.HTTP_201_CREATED)
                return Response({
                    'success': False,
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Room.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Sala no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request, *args, **kwargs):
        """
        Crea una nueva sala con su administrador.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save()
            # Usar el serializer específico para la respuesta
            response_serializer = RoomSerializer(room)
            return Response({
                'success': True,
                'room': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ParticipantViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar participantes.
    """
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ParticipantCreateSerializer
        return ParticipantSerializer
    
    def get_queryset(self):
        """
        Este método permite filtrar los participantes por sala.
        Se puede filtrar agregando ?room=<id_de_la_sala> a la URL.
        """
        queryset = Participant.objects.all()
        room_id = self.request.query_params.get('room', None)
        if room_id is not None:
            # Intentar encontrar la sala por código o id
            try:
                if not room_id.isdigit():
                    room = Room.objects.get(code=room_id)
                else:
                    room = Room.objects.get(pk=room_id)
                queryset = queryset.filter(room=room)
            except Room.DoesNotExist:
                queryset = Participant.objects.none()
        return queryset

