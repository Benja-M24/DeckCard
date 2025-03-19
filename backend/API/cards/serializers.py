from rest_framework import serializers
from .models import Mazo, CartaNegocio, CartaPersonaje, CartaEspecial

class MazoSerializer(serializers.ModelSerializer):
    fecha_creacion = serializers.DateTimeField(format='%d-%m-%Y', read_only=True)
    
    class Meta:
        model = Mazo
        fields = ['id', 'nombre', 'version', 'fecha_creacion']

class CartaPersonajeSerializer(serializers.ModelSerializer):
    consignas = serializers.ListField(source='consignas_juego', required=False)
    
    class Meta:
        model = CartaPersonaje
        fields = ['id', 'nombre', 'descripcion', 'historia', 'imagen', 
                 'dinero', 'karma', 'fama', 'consignas', 'mazo']

class CartaNegocioSerializer(serializers.ModelSerializer):
    consignas = serializers.ListField(source='consignas_juego', required=False)
    
    class Meta:
        model = CartaNegocio
        fields = ['id', 'nombre', 'frase', 'tipo', 'precio', 
                 'beneficio_base', 'beneficio_final', 'consignas_juego', 
                 'consignas', 'niveles_soportados', 'mazo']

class CartaEspecialSerializer(serializers.ModelSerializer):
    consignas = serializers.ListField(source='consignas_juego', required=False)
    
    class Meta:
        model = CartaEspecial
        fields = ['id', 'titulo', 'frase', 'consignas_juego', 'consignas', 'imagen', 'mazo']
