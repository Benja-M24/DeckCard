from rest_framework import serializers
from .models import Version, CartaNegocio, CartaPersonaje, CartaEspecial, CartaEvento, CartaObjetivo, Room, Participant, business_upgrade, business_industry

class VersionSerializer(serializers.ModelSerializer):
    fecha_creacion = serializers.DateTimeField(format='%d-%m-%Y', read_only=True)
    
    class Meta:
        model = Version
        fields = ['id', 'nombre', 'version', 'fecha_creacion']

class CartaPersonajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartaPersonaje
        fields = ['id', 'nombre', 'descripcion', 'historia', 'imagen', 
                 'dinero', 'karma', 'fama', 'consignas_juego', 'version']

class BusinessIndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = business_industry
        fields = ['id', 'industry_name']

class BusinessUpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = business_upgrade
        fields = ['id', 'upgrade_name', 'n_wachines_necesarios', 'costo_mejora', 'version']

class CartaNegocioSerializer(serializers.ModelSerializer):
    business_industry_name = serializers.ReadOnlyField(source='business_industry.industry_name')
    
    class Meta:
        model = CartaNegocio
        fields = ['id', 'nombre', 'frase', 'business_industry', 'business_industry_name', 'precio', 
                 'beneficio_base', 'beneficio_mejorado', 'consignas_juego', 'business_class_name',
                 'business_upgrade', 'version']

class CartaEspecialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartaEspecial
        fields = ['id', 'titulo', 'frase', 'consignas_juego', 'imagen', 'version']

class CartaEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartaEvento
        fields = ['id', 'titulo', 'frase', 'consignas_juego', 'imagen', 'version']

class CartaObjetivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartaObjetivo
        fields = ['id', 'titulo', 'consignas_juego', 'imagen', 'version']

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'name', 'admin', 'dinero', 'karma', 'fama', 'userAgent', 'room']
        read_only_fields = ['id']

class RoomSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(
        many=True,
        read_only=True
    )
    
    class Meta:
        model = Room
        fields = ['code', 'name', 'version', 'status', 'fecha_creacion', 'participants', 'max_participants']
        read_only_fields = ['code']
    def get_status(self, obj):
        return obj.update_status