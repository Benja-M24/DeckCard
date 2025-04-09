from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Version, CartaNegocio, CartaPersonaje, CartaEspecial, CartaEvento, CartaObjetivo, Room, Participant, business_upgrade, business_industry
from .serializers import (
    VersionSerializer, 
    CartaNegocioSerializer, 
    CartaPersonajeSerializer, 
    CartaEspecialSerializer,
    CartaEventoSerializer,
    CartaObjetivoSerializer,
    RoomSerializer,
    ParticipantSerializer
)
from .services import RoomService, ParticipantService, VersionService

# Create your views here.

class VersionViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver y editar versiones.
    """
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    
    @action(detail=True, methods=['get'])
    def cartas(self, request, pk=None):
        """
        Obtiene todas las cartas asociadas a una versión específica
        """
        version = self.get_object()
        
        # Usar el servicio para obtener todas las cartas de la versión
        cards_by_type = VersionService.get_all_cards_by_version(version)
        
        # Serializar cada tipo de carta
        result = {
            'personajes': CartaPersonajeSerializer(cards_by_type['personajes'], many=True).data,
            'negocios': CartaNegocioSerializer(cards_by_type['negocios'], many=True).data,
            'especiales': CartaEspecialSerializer(cards_by_type['especiales'], many=True).data,
            'eventos': CartaEventoSerializer(cards_by_type['eventos'], many=True).data,
            'objetivos': CartaObjetivoSerializer(cards_by_type['objetivos'], many=True).data
        }
        
        return Response(result)

class CartaPersonajeViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver y editar cartas de personaje.
    """
    serializer_class = CartaPersonajeSerializer
    
    def get_queryset(self):
        """
        Este método permite filtrar las cartas de personaje por versión.
        Se puede filtrar agregando ?version=<id_de_version> a la URL.
        """
        queryset = CartaPersonaje.objects.all()
        version_id = self.request.query_params.get('version', None)
        if version_id is not None:
            queryset = queryset.filter(version__id=version_id)
        return queryset

class CartaNegocioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver y editar cartas de negocio.
    """
    serializer_class = CartaNegocioSerializer
    
    def get_queryset(self):
        """
        Este método permite filtrar las cartas de negocio por versión.
        Se puede filtrar agregando ?version=<id_de_version> a la URL.
        """
        queryset = CartaNegocio.objects.all()
        version_id = self.request.query_params.get('version', None)
        if version_id is not None:
            queryset = queryset.filter(version__id=version_id)
        return queryset

class CartaEspecialViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver y editar cartas especiales.
    """
    serializer_class = CartaEspecialSerializer
    def get_queryset(self):
        """
        Este método permite filtrar las cartas de personaje por versión.
        Se puede filtrar agregando ?version=<id_de_version> a la URL.
        """
        queryset = CartaEspecial.objects.all()
        version_id = self.request.query_params.get('version', None)
        if version_id is not None:
            queryset = queryset.filter(version__id=version_id)
        return queryset

class CartaEventoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver y editar cartas de evento.
    """
    serializer_class = CartaEventoSerializer
    def get_queryset(self):
        """
        Este método permite filtrar las cartas de evento por versión.
        Se puede filtrar agregando ?version=<id_de_version> a la URL.
        """
        queryset = CartaEvento.objects.all()
        version_id = self.request.query_params.get('version', None)
        if version_id is not None:
            queryset = queryset.filter(version__id=version_id)
        return queryset

class CartaObjetivoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para ver y editar cartas de objetivo.
    """
    serializer_class = CartaObjetivoSerializer
    def get_queryset(self):
        """
        Este método permite filtrar las cartas de objetivo por versión.
        Se puede filtrar agregando ?version=<id_de_version> a la URL.
        """
        queryset = CartaObjetivo.objects.all()
        version_id = self.request.query_params.get('version', None)
        if version_id is not None:
            queryset = queryset.filter(version__id=version_id)
        return queryset





class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar salas de juego.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """
        Recupera los detalles de una sala específica por su código.
        """
        room_code = kwargs.get('pk')
        room = RoomService.get_room_by_code(room_code)
        
        if not room:
            return Response({
                'success': False,
                'error': 'El código ingresado no corresponde a ninguna sala'
            }, status=status.HTTP_404_NOT_FOUND)
            
        # Serializar la sala con sus participantes
        serializer = self.get_serializer(room)
        
        return Response({
            'success': True,
            'room': serializer.data
        })
    
    # @action(detail=True, methods=['post'])
    # def participants(self, request, pk=None):
    #     """
    #     Añade participantes a una sala específica.
    #     """
    #     try:
    #         # Obtener la sala por su código
    #         room = Room.objects.get(code=pk)
            
    #         # Distinguir entre GET y POST
    #         if request.method == 'POST':
    #             # Verificar si la sala está llena
    #             if room.is_full:
    #                 return Response({
    #                     'success': False,
    #                     'error': 'La sala está llena'
    #                 }, status=status.HTTP_400_BAD_REQUEST)
                
    #             # Verificar si el nombre del participante ya existe
    #             if Participant.objects.filter(room=room, name=request.data.get('name')).exists():
    #                 return Response({
    #                     'success': False,
    #                     'error': 'El nombre del participante ya existe'
    #                 }, status=status.HTTP_400_BAD_REQUEST)
                
    #             # Crear un nuevo participante
    #             serializer = ParticipantSerializer(data=request.data)
    #             if serializer.is_valid():
    #                 # Asignar la sala al participante
    #                 serializer.save(room=room)
    #                 return Response({
    #                     'success': True,    
    #                     'participant': serializer.data
    #                 }, status=status.HTTP_201_CREATED)
    #             else:
    #                 return Response({
    #                     'success': False,
    #                     'errors': serializer.errors
    #                 }, status=status.HTTP_400_BAD_REQUEST)
                        
    #     except Room.DoesNotExist:
    #         return Response({
    #             'success': False,
    #             'error': 'Sala no encontrada'
    #         }, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request, *args, **kwargs):
        """
        Crea una nueva sala con su administrador.
        """
        data = request.data.copy()
        admin_name = data.pop('admin_name', None)
        
        if not admin_name:
            return Response({
                'success': False,
                'error': 'Se requiere el nombre del administrador'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar los datos de la sala
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            try:
                # Usar el servicio para crear la sala y el administrador
                room = RoomService.create_room(serializer.validated_data, admin_name)
                
                # Serializar respuesta
                response_serializer = self.get_serializer(room)
                return Response({
                    'success': True,
                    'room': response_serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'success': False,
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ParticipantViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar participantes.
    """
    serializer_class = ParticipantSerializer
    
    def get_queryset(self):
        """
        Este método permite filtrar los participantes por sala.
        Se puede filtrar agregando ?room=<código_de_la_sala> a la URL.
        """
        queryset = Participant.objects.all()
        room_code = self.request.query_params.get('room', None)
        
        if room_code is not None:
            # Usar el servicio para obtener la sala
            room = RoomService.get_room_by_code(room_code)
            if room:
                queryset = ParticipantService.get_participants_by_room(room)
            else:
                queryset = Participant.objects.none()
        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo participante, verificando primero si la sala existe y no está llena.
        """
        data = request.data.copy()
        room_code = data.get('room')
        
        if not room_code:
            return Response({
                'success': False,
                'error': 'Se requiere el código de la sala'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Usar el servicio para obtener la sala
        room = RoomService.get_room_by_code(room_code)
        if not room:
            return Response({
                'success': False,
                'error': 'Sala no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
            
        # Validar los datos del participante
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Usar el servicio para crear el participante
            participant = ParticipantService.create_participant(serializer.validated_data, room)
            
            return Response({
                'success': True,
                'participant': self.get_serializer(participant).data
            }, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

