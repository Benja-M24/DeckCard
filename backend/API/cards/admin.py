from django.contrib import admin
from .models import (
    Mazo, 
    NivelDeNegocio,
    TipoDeNegocio, 
    CartaNegocio, 
    CartaPersonaje, 
    CartaEspecial
)

class CartaNegocioInline(admin.TabularInline):
    model = CartaNegocio
    extra = 1

class CartaPersonajeInline(admin.TabularInline):
    model = CartaPersonaje
    extra = 1

class CartaEspecialInline(admin.TabularInline):
    model = CartaEspecial
    extra = 1

@admin.register(Mazo)
class MazoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'version', 'fecha_creacion')
    search_fields = ('nombre', 'version')
    list_filter = ('fecha_creacion',)
    inlines = [CartaNegocioInline, CartaPersonajeInline, CartaEspecialInline]

@admin.register(NivelDeNegocio)
class NivelDeNegocioAdmin(admin.ModelAdmin):
    list_display = ('n_nivel', 'n_wachines_necesarios', 'plus_de_beneficio')
    search_fields = ('n_nivel',)
    list_filter = ('n_nivel',)

@admin.register(TipoDeNegocio)
class TipoDeNegocioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(CartaNegocio)
class CartaNegocioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'frase', 'tipo', 'precio', 'mazo', 'beneficio_base')
    search_fields = ('nombre', 'frase', 'tipo')
    list_filter = ('tipo', 'mazo')
    filter_horizontal = ('niveles_soportados',)

@admin.register(CartaPersonaje)
class CartaPersonajeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'dinero', 'karma', 'fama', 'mazo')
    search_fields = ('nombre', 'historia', 'descripcion')
    list_filter = ('mazo',)

@admin.register(CartaEspecial)
class CartaEspecialAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'frase', 'mazo')
    search_fields = ('titulo', 'frase', 'consignas_juego')
    list_filter = ('mazo',)
