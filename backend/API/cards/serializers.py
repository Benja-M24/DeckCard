from rest_framework import serializers
from .models import Mazo, CartaNegocio, CartaPersonaje, CartaEspecial

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
