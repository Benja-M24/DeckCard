from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
import json
import secrets
import string

class Version(models.Model):
    """
    Modelo para representar una versión de cartas.
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    version = models.CharField(max_length=20, verbose_name="Versión")
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de creación")
    
    # Variable para establecer la versión por defecto para nuevas cartas
    DEFAULT_VERSION_ID = 3
    
    @classmethod
    def get_default_version(cls):
        # No podemos retornar directamente DEFAULT_VERSION_ID porque necesitamos
        # el objeto Version completo, no solo su ID.
        # Ejemplo incorrecto:
        #   return cls.DEFAULT_VERSION_ID  # Esto retornaría solo el número 3, no el objeto Version
        
        # Necesitamos hacer una consulta a la base de datos para obtener
        # el objeto Version completo con todos sus atributos
        # Ejemplo correcto:
        try:
            return cls.objects.get(id=cls.DEFAULT_VERSION_ID)
        except cls.DoesNotExist:
            # Fallback to first version if default doesn't exist
            return cls.objects.first()

    class Meta:
        verbose_name = "Versión"
        verbose_name_plural = "Versiones"
        ordering = ['fecha_creacion']

    def __str__(self):
        return f"{self.nombre} (v{self.version})"
    
    def mezclar_mazo(self):
        """Método para mezclar las cartas de la versión"""
        # Implementación de la mezcla (será desarrollada posteriormente)
        pass
    
    def repartir_cartas(self, num_cartas, num_jugadores):
        """Método para repartir cartas a varios jugadores"""
        # Implementación del reparto (será desarrollada posteriormente)
        pass
    
    def tomar_carta(self):
        """Método para tomar la siguiente carta de la versión"""
        # Implementación para tomar carta (será desarrollada posteriormente)
        pass
    

class business_upgrade(models.Model):
    """
    Modelo para representar niveles de negocio para las cartas de negocios.
    """
    upgrade_name = models.CharField(max_length=30, verbose_name="Nombre de mejora")
    n_wachines_necesarios = models.PositiveIntegerField(verbose_name="Número de trabajadores necesarios")
    costo_mejora = models.PositiveIntegerField(verbose_name="Costo de mejora", validators=[MinValueValidator(1), MaxValueValidator(100000)])
    version = models.ForeignKey(Version, on_delete=models.PROTECT, null=False, blank=False, related_name='business_upgrades', verbose_name="Versión", default=Version.DEFAULT_VERSION_ID)
    
    class Meta:
        verbose_name = "Mejora de negocio"
        verbose_name_plural = "Mejoras de negocio"
        ordering = ['upgrade_name']
    
    def __str__(self):
        return f"{self.upgrade_name} (Trabajadores: {self.n_wachines_necesarios} | Costo: {self.costo_mejora})"

class business_industry(models.Model):
    """
    Modelo para representar los distinto rubros para las cartas de negocios.
    """
    industry_name = models.CharField(max_length=20, verbose_name="Nombre")
    
    class Meta:
        verbose_name = "Rubro de negocio"
        verbose_name_plural = "Rubros de negocio"
        ordering = ['industry_name']
    
    def __str__(self):
        return self.industry_name

class CartaNegocio(models.Model):
    """
    Modelo para representar cartas de negocios.
    """
    business_class_choices = [
        ('Bronze', 'Bronce'),
        ('Silver', 'Plata'),
        ('Gold', 'Oro'),
        ('Platinum', 'Platino')
    ]
    
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    frase = models.CharField(max_length=200, blank=True, verbose_name="Frase")
    precio = models.PositiveIntegerField(
        default=3600,
        verbose_name="Precio del Negocio",
        validators=[
            MinValueValidator(1000, message='El precio no puede ser negativo'),
            MaxValueValidator(1000000, message='Límite máximo: $ 1000000')
        ]
    )
    business_class_name = models.CharField(max_length=20, choices=business_class_choices, default='Bronze', verbose_name="Clase")
    business_upgrade = models.ManyToManyField(business_upgrade, related_name='business_cards', verbose_name="Mejoras disponibles")
    business_industry = models.ForeignKey(business_industry, on_delete=models.PROTECT, null=True, blank=True, related_name='business_cards', verbose_name="Rubro de Negocio")
    beneficio_base = models.IntegerField(
        default=180,
        verbose_name="beneficio base",
        validators=[
            MinValueValidator(100, message='Beneficio base minimo 100'),
            MaxValueValidator(100000, message='Beneficio base limite 100000')
        ]
    )
    beneficio_mejorado = models.IntegerField(
        default=250,
        verbose_name="beneficio final",
        validators=[
            MinValueValidator(100, message='Beneficio final minimo 100'),
            MaxValueValidator(100000, message='Beneficio final limite 100000')
        ]
    )
    consignas_juego = models.JSONField(
        default=list,
        blank=True,
        null=True,
        verbose_name="Consignas del Negocio",
        validators=[
            MaxLengthValidator(5)
        ]   
    )
    version = models.ForeignKey(Version, on_delete=models.PROTECT, null=False, blank=False, related_name='cartas_negocio', verbose_name="Versión", default=Version.DEFAULT_VERSION_ID)

    class Meta:
        verbose_name = "Carta de negocio"
        verbose_name_plural = "Cartas de negocio"
    
    def __str__(self):
        return self.nombre

class CartaPersonaje(models.Model):
    """
    Modelo para representar cartas de personajes.
    """ 
    
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.CharField(max_length=200, default='Masculino de 32 años, ingeniero...', verbose_name="Descripción")
    historia = models.TextField(verbose_name="Historia", default='Recien llegado a la ciudad en busca de una aventura.')
    imagen = models.ImageField(upload_to='personajes/', default='personajes/ejemplo.png', blank=True, null=True, verbose_name="Imagen")
    dinero = models.IntegerField(
        default=3600,
        verbose_name="Dinero",
        validators=[
            MinValueValidator(0, message='El dinero no puede ser negativo'),
            MaxValueValidator(100000, message='Límite máximo: $100.000')
        ]
    )
    karma = models.IntegerField(
        default=500,
        verbose_name="Karma",
        validators=[
            MinValueValidator(0, message='El karma no puede ser negativo'),
            MaxValueValidator(1000, message='Límite máximo: 1000')
        ]
    )
    fama = models.IntegerField(
        default=500,
        verbose_name="Fama",
        validators=[
            MinValueValidator(0, message='La fama no puede ser negativa'),
            MaxValueValidator(1000, message='Límite máximo: 1000')
        ]
    )
    consignas_juego = models.JSONField(
        default=list,
        blank=True,
        null=True,
        verbose_name="Consigna del personaje",
        validators=[
            MaxLengthValidator(5)
        ]
    )

    def agregar_consigna(self, consigna: str):
        """Agrega una nueva consigna a la lista"""
        if not self.consignas_juego:
            self.consignas_juego = []
        self.consignas_juego.append(consigna.strip())

    version = models.ForeignKey(Version, on_delete=models.PROTECT, null=False, blank=False, related_name='cartas_personaje', verbose_name="Versión", default=Version.DEFAULT_VERSION_ID)
    
    class Meta:
        verbose_name = "Carta de personaje"
        verbose_name_plural = "Cartas de personaje"
    
    def __str__(self):
        return f"{self.nombre} \"{self.descripcion}\""

class CartaEspecial(models.Model):
    """
    Modelo para representar cartas especiales.
    """
    titulo = models.CharField(max_length=100, verbose_name="Título")
    frase = models.CharField(max_length=200, verbose_name="Frase")
    consignas_juego = models.JSONField(
        default=list,
        blank=True,
        null=True,
        verbose_name="Consignas de Carta Especial",
        validators=[
            MaxLengthValidator(5)
        ]
    )
    imagen = models.ImageField(upload_to='especiales/', blank=True, null=True, verbose_name="Imagen")
    version = models.ForeignKey(Version, related_name='cartas_especiales', on_delete=models.PROTECT, null=False, blank=False, verbose_name="Versión", default=Version.DEFAULT_VERSION_ID)
    
    class Meta:
        verbose_name = "Carta especial"
        verbose_name_plural = "Cartas especiales"
    
    def __str__(self):
        return self.titulo

class CartaEvento(models.Model):
    """
    Modelo para representar cartas de evento.
    """
    titulo = models.CharField(max_length=100, verbose_name="Título")
    frase = models.CharField(max_length=200, verbose_name="Frase")
    consignas_juego = models.JSONField(
        default=list,
        blank=True,
        null=True,
        verbose_name="Consignas de Carta Especial",
        validators=[
            MaxLengthValidator(5)
        ]
    )
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True, verbose_name="Imagen")
    version = models.ForeignKey(Version, related_name='cartas_eventos', on_delete=models.PROTECT, null=False, blank=False, verbose_name="Versión", default=Version.DEFAULT_VERSION_ID)
    
    class Meta:
        verbose_name = "Carta de evento"
        verbose_name_plural = "Cartas de evento"
    
    def __str__(self):
        return self.titulo

class CartaObjetivo(models.Model):
    """
    Modelo para representar cartas de objetivo.
    """
    titulo = models.CharField(max_length=100, verbose_name="Título")
    consignas_juego = models.TextField(
        default="Conquista todas las panaderias.",
        blank=True,
        null=True,
        verbose_name="Consignas de Carta Especial",
        validators=[
            MaxLengthValidator(5)
        ]
    )
    imagen = models.ImageField(upload_to='objetivos/', blank=True, null=True, verbose_name="Imagen")
    version = models.ForeignKey(Version, related_name='cartas_objetivos', on_delete=models.PROTECT, null=False, blank=False, verbose_name="Versión", default=Version.DEFAULT_VERSION_ID)
    
    class Meta:
        verbose_name = "Carta de objetivo"
        verbose_name_plural = "Cartas de objetivo"
    
    def __str__(self):
        return self.titulo

# Borra el registro si la sala está finalizada y tiene más de un día de antigüedad
@classmethod
def clean_older_rooms(room):
    room.objects.filter(fecha_creacion__lt=timezone.now() - timedelta(days=2)).delete()

def generate_room_code():
    """
    Genera un código hexadecimal único de 6 caracteres para la sala.
    """
    characters = string.ascii_uppercase + string.digits
    while True:
        # Generar código hexadecimal aleatorio de 6 caracteres
        code = ''.join(secrets.choice(characters) for _ in range(6))
        # Verificar que no exista una sala con este código
        if not Room.objects.filter(code=code).exists():
            return code


class Room(models.Model):
    """
    Modelo para representar una sala de juego.
    """
    STATUS_CHOICES = [
        ('created', 'Creada'),
        ('waiting', 'Esperando jugadores'),
        ('in_progress', 'En progreso'),
        ('finished', 'Finalizada'),
    ]
    
    # Código único hexadecimal de 6 caracteres para la sala
    code = models.CharField(max_length=6, primary_key=True, default=generate_room_code, verbose_name="Código de sala")
    name = models.CharField(max_length=100, verbose_name="Nombre de la sala")
    version = models.ForeignKey(Version, on_delete=models.PROTECT, null=True, blank=True, related_name='rooms', verbose_name="Versión")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name="Estado")
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de creación")
    max_participants = models.PositiveIntegerField(default=6, validators=[MinValueValidator(2), MaxValueValidator(10)], verbose_name="Máximo de participantes")
    
    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.name} #{self.code}"
    
    @property
    def participants_count(self):
        return self.participants.count()
    
    @property
    def is_full(self):
        return self.participants_count >= self.max_participants
    
    @property
    def update_status(self):
        """Actualiza automáticamente el estado basado en cantidad de participantes"""
        current_count = self.participants.count()
        
        if current_count < self.max_participants:
            self.status = 'waiting'
        elif current_count == self.max_participants:
            self.status = 'in_progress'
        
        self.save()
        return self.status

class Participant(models.Model):
    """
    Modelo para representar un participante en una sala de juego.
    """
    
    name = models.CharField(max_length=100, verbose_name="Nombre")
    admin = models.BooleanField(default=False, verbose_name="Administrador")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='participants', verbose_name="Sala")
    carta_personaje = models.ForeignKey(CartaPersonaje, on_delete=models.CASCADE, related_name='participants', verbose_name="Carta de personaje", null=True, blank=True)
    cartas_negocios = models.ManyToManyField(CartaNegocio, default=[], related_name='participants', verbose_name="Cartas de negocio")
    cartas_especiales = models.ManyToManyField(CartaEspecial, default=[], related_name='participants', verbose_name="Carta especial")
    dinero = models.IntegerField(
        default=0,
        verbose_name="Dinero",
        validators=[
            MinValueValidator(0, message='El dinero no puede ser negativo'),
            MaxValueValidator(100000, message='Límite máximo: $100.000')
        ]
    )
    karma = models.IntegerField(
        default=0,
        verbose_name="Karma",
        validators=[
            MinValueValidator(0, message='El karma no puede ser negativo'),
            MaxValueValidator(1000, message='Límite máximo: 1000')
        ]
    )
    fama = models.IntegerField(
        default=0,
        verbose_name="Fama",
        validators=[
            MinValueValidator(0, message='La fama no puede ser negativa'),
            MaxValueValidator(1000, message='Límite máximo: 1000')
        ]
    )
    userAgent = models.JSONField(default=dict, blank=True, null=True, verbose_name="Datos adicionales")
    fecha_ingreso = models.DateTimeField(default=timezone.now, verbose_name="Fecha de ingreso")
    
    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"
        ordering = ['fecha_ingreso']
        # Garantiza que no haya participantes duplicados en una misma sala
        unique_together = ['name', 'room']
    
    def __str__(self):
        return f"{self.name} ({self.room.code})"

