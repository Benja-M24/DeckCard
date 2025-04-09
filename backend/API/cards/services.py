from django.db import transaction
from typing import Dict, Any, Optional
from .models import Room, Participant, Version


class RoomService:
    """
    Servicio para gestionar salas de juego.
    Aplica el principio de responsabilidad única manejando solo la lógica de negocios relacionada con salas.
    """
    
    @staticmethod
    @transaction.atomic
    def create_room(data: Dict[str, Any], admin_name: str) -> Room:
        """
        Crea una nueva sala junto con su administrador en una transacción atómica.
        
        Args:
            data: Datos validados para crear la sala
            admin_name: Nombre del administrador
            
        Returns:
            Room: Instancia de sala creada
        """
        # Crear la sala
        room = Room.objects.create(**data)
        
        # Crear el administrador
        Participant.objects.create(
            name=admin_name,
            admin=True,
            room=room
        )
        
        # Actualizar el estado
        room.status = 'created'
        room.save()
        
        return room
    
    @staticmethod
    def get_room_by_code(code: str) -> Optional[Room]:
        """
        Obtiene una sala por su código
        
        Args:
            code: Código único de la sala
            
        Returns:
            Room o None: La sala encontrada o None si no existe
        """
        try:
            return Room.objects.get(code=code)
        except Room.DoesNotExist:
            return None


class ParticipantService:
    """
    Servicio para gestionar participantes.
    Aplica el principio de responsabilidad única manejando solo la lógica de negocios relacionada con participantes.
    """
    
    @staticmethod
    def create_participant(data: Dict[str, Any], room: Room) -> Participant:
        """
        Crea un nuevo participante para una sala
        
        Args:
            data: Datos validados para crear el participante
            room: Sala a la que pertenecerá el participante
            
        Returns:
            Participant: Instancia del participante creado
        """
        # Validar nombre único en la sala
        name = data.get('name')
        if Participant.objects.filter(room=room, name=name).exists():
            raise ValueError('El nombre del participante ya existe en esta sala')
            
        # Validar si la sala está llena
        if room.is_full:
            raise ValueError('La sala está llena')
            
        # Crear el participante
        return Participant.objects.create(room=room, **data)
    
    @staticmethod
    def get_participants_by_room(room: Room):
        """
        Obtiene todos los participantes de una sala
        
        Args:
            room: Sala de la que se obtendrán los participantes
            
        Returns:
            QuerySet: Participantes de la sala
        """
        return Participant.objects.filter(room=room)


class VersionService:
    """
    Servicio para gestionar versiones y sus cartas.
    Aplica el principio de responsabilidad única manejando solo la lógica de negocios relacionada con versiones.
    """
    
    @staticmethod
    def get_all_cards_by_version(version: Version) -> Dict[str, list]:
        """
        Obtiene todas las cartas de una versión agrupadas por tipo
        
        Args:
            version: Versión de la que se obtendrán las cartas
            
        Returns:
            Dict: Diccionario con las cartas agrupadas por tipo
        """
        return {
            'personajes': list(version.cartas_personaje.all()),
            'negocios': list(version.cartas_negocio.all()),
            'especiales': list(version.cartas_especiales.all()),
            'eventos': list(version.cartas_eventos.all()),
            'objetivos': list(version.cartas_objetivos.all())
        }
