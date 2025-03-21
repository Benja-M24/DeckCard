from rest_framework import serializers
from .models import Mazo, CartaNegocio, CartaPersonaje, CartaEspecial, Room, Participant

class MazoSerializer(serializers.ModelSerializer):
    fecha_creacion = serializers.DateTimeField(format='%d-%m-%Y', read_only=True)
    
    class Meta:
        model = Mazo
        fields = ['id', 'nombre', 'version', 'fecha_creacion']

class CartaPersonajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartaPersonaje
        fields = ['id', 'nombre', 'descripcion', 'historia', 'imagen', 
                 'dinero', 'karma', 'fama', 'consignas_juego', 'mazo']

class CartaNegocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartaNegocio
        fields = ['id', 'nombre', 'frase', 'tipo', 'precio', 
                 'beneficio_base', 'beneficio_final', 'consignas_juego', 
                 'niveles_soportados', 'mazo']

class CartaEspecialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartaEspecial
        fields = ['id', 'titulo', 'frase', 'consignas_juego', 'imagen', 'mazo']


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'name', 'admin', 'dinero', 'karma', 'fama', 'extra_data', 'fecha_ingreso']


class ParticipantCreateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=['admin', 'player'], write_only=True, required=False, default='player')
    extraData = serializers.JSONField(write_only=True, required=False)
    
    class Meta:
        model = Participant
        fields = ['id', 'name', 'admin', 'role', 'extraData']
        read_only_fields = ['id', 'admin']
    
    def create(self, validated_data):
        role = validated_data.pop('role', 'player')
        extra_data = validated_data.pop('extraData', {})
        
        # Determinar si es admin basado en el rol
        is_admin = (role == 'admin')
        
        # Crear el participante
        participant = Participant.objects.create(
            admin=is_admin,
            extra_data=extra_data,
            **validated_data
        )
        
        return participant


class RoomSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    participants_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Room
        fields = ['id', 'code', 'name', 'max_participants', 'status', 'fecha_creacion', 'mazo', 'participants', 'participants_count']
        read_only_fields = ['id', 'code', 'fecha_creacion', 'participants_count']


class RoomCreateSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = Room
        fields = ['id', 'code', 'name', 'max_participants', 'mazo', 'admin_name']
        read_only_fields = ['id', 'code']
    
    def create(self, validated_data):
        admin_name = validated_data.pop('admin_name')
        
        # Crear la sala
        room = Room.objects.create(**validated_data)
        
        # Crear el administrador
        Participant.objects.create(
            name=admin_name,
            admin=True,
            room=room
        )
        
        return room
