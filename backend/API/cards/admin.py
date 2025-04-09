from django.contrib import admin
from .models import (
    Version, 
    business_upgrade,
    business_industry, 
    CartaNegocio, 
    CartaPersonaje, 
    CartaEspecial,
    Room,
    CartaObjetivo,
    CartaEvento,
    Participant
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

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'version', 'fecha_creacion')
    search_fields = ('nombre', 'version')
    list_filter = ('fecha_creacion',)
    inlines = [CartaNegocioInline, CartaPersonajeInline, CartaEspecialInline]

@admin.register(business_upgrade)
class BusinessUpgradeAdmin(admin.ModelAdmin):
    list_display = ('upgrade_name', 'n_wachines_necesarios', 'costo_mejora', 'version')
    search_fields = ('upgrade_name',)
    list_filter = ('version',)

@admin.register(business_industry)
class BusinessIndustryAdmin(admin.ModelAdmin):
    list_display = ('industry_name',)
    search_fields = ('industry_name',)

@admin.register(CartaNegocio)
class CartaNegocioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'frase', 'business_industry', 'precio', 'business_class_name', 'version', 'beneficio_base', 'beneficio_mejorado', 'consignas_juego')
    search_fields = ('nombre', 'frase', 'business_industry__industry_name')
    list_filter = ('business_industry', 'version', 'business_class_name')
    filter_horizontal = ('business_upgrade',)

@admin.register(CartaPersonaje)
class CartaPersonajeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'dinero', 'karma', 'fama', 'version')
    search_fields = ('nombre', 'historia', 'descripcion')
    list_filter = ('version',)

@admin.register(CartaEspecial)
class CartaEspecialAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'frase', 'version')
    search_fields = ('titulo', 'frase', 'consignas_juego')
    list_filter = ('version',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'status', 'version', 'fecha_creacion', 'max_participants', 'participants_count')
    search_fields = ('code', 'name')
    list_filter = ('status', 'version', 'fecha_creacion')
    readonly_fields = ('code',)

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'room', 'admin', 'dinero', 'karma', 'fama', 'fecha_ingreso')
    search_fields = ('name',)
    list_filter = ('room', 'admin', 'fecha_ingreso')
    filter_horizontal = ('cartas_negocios', 'cartas_especiales')

@admin.register(CartaObjetivo)
class CartaObjetivoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'version')
    search_fields = ('titulo', 'consignas_juego')
    list_filter = ('version',)

@admin.register(CartaEvento)
class CartaEventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'frase', 'version')
    search_fields = ('titulo', 'frase', 'consignas_juego')
    list_filter = ('version',)
