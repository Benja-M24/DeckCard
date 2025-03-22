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
        fields = ['id', 'name', 'admin', 'dinero', 'karma', 'fama', 'userAgent', 'fecha_ingreso']


class ParticipantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'name', 'admin', 'userAgent', 'room']
        read_only_fields = ['id', 'admin']
    
    def create(self, validated_data):
        # Crear el participante
        participant = Participant.objects.create(**validated_data)
        return participant


class RoomSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    
    class Meta:
        model = Room
        fields = ['code', 'name', 'mazo', 'status', 'fecha_creacion', 'participants', 'max_participants']
        read_only_fields = ['code', 'name', 'max_participants', 'fecha_creacion']
    def get_status(self, obj):
        return obj.update_status

class RoomCreateSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = Room
        fields = ['code', 'name', 'max_participants', 'mazo', 'admin_name']
        read_only_fields = ['code']
    
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
        
        room.status = 'created'
        room.save()

        return room
