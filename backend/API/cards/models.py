from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
import json
import secrets
import string

class Mazo(models.Model):
    """
    Modelo para representar un mazo de cartas.
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    version = models.CharField(max_length=20, verbose_name="Versión")
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Mazo"
        verbose_name_plural = "Mazos"
        ordering = ['fecha_creacion']

    def __str__(self):
        return f"{self.nombre} (v{self.version})"
    
    def mezclar_mazo(self):
        """Método para mezclar las cartas del mazo"""
        # Implementación de la mezcla (será desarrollada posteriormente)
        pass
    
    def repartir_cartas(self, num_cartas, num_jugadores):
        """Método para repartir cartas a varios jugadores"""
        # Implementación del reparto (será desarrollada posteriormente)
        pass
    
    def tomar_carta(self):
        """Método para tomar la siguiente carta del mazo"""
        # Implementación para tomar carta (será desarrollada posteriormente)
        pass

class NivelDeNegocio(models.Model):
    """
    Modelo para representar niveles de negocio para las cartas de negocios.
    """
    n_nivel = models.PositiveIntegerField(verbose_name="Número de nivel")
    n_wachines_necesarios = models.PositiveIntegerField(verbose_name="Número de trabajadores necesarios")
    costo_mejora = models.PositiveIntegerField(verbose_name="Costo de mejora", validators=[MinValueValidator(1), MaxValueValidator(100)])
    plus_de_beneficio = models.FloatField(verbose_name="Plus de beneficio", validators=[MinValueValidator(0.1), MaxValueValidator(100)])
    
    class Meta:
        verbose_name = "Nivel de negocio"
        verbose_name_plural = "Niveles de negocio"
        ordering = ['n_nivel']
    
    def __str__(self):
        return f"Nivel {self.n_nivel} (Trabajadores: {self.n_wachines_necesarios})"

class TipoDeNegocio(models.Model):
    """
    Modelo para representar tipos de negocio para las cartas de negocios.
    """
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    
    class Meta:
        verbose_name = "Tipo de negocio"
        verbose_name_plural = "Tipos de negocio"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class CartaNegocio(models.Model):
    """
    Modelo para representar cartas de negocios.
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    frase = models.CharField(max_length=200, blank=True, verbose_name="Frase")
    precio = models.PositiveIntegerField(
        default=3600,
        verbose_name="Precio del Negocio",
        validators=[
            MinValueValidator(1, message='El precio no puede ser negativo'),
            MaxValueValidator(100, message='Límite máximo: $ 100')
        ]
    )
    niveles_soportados = models.ManyToManyField(NivelDeNegocio, related_name='cartas', verbose_name="Niveles soportados")
    beneficio_base = models.IntegerField(
        default=5,
        verbose_name="beneficio base",
        validators=[
            MinValueValidator(1, message='Beneficio base minimo 1'),
            MaxValueValidator(10, message='Beneficio base limite 10')
        ]
    )
    beneficio_final = models.IntegerField(
        default=5,
        verbose_name="beneficio final",
        validators=[
            MinValueValidator(1, message='Beneficio final minimo 1'),
            MaxValueValidator(10, message='Beneficio final limite 10')
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
    
    tipo = models.ForeignKey(TipoDeNegocio, on_delete=models.PROTECT, null=False, blank=False, related_name='cartas_negocio', verbose_name="Tipo de Negocio")
    mazo = models.ForeignKey(Mazo, on_delete=models.PROTECT, null=False, blank=False, related_name='cartas_negocio', verbose_name="Mazo")

    class Meta:
        verbose_name = "Carta de negocio"
        verbose_name_plural = "Cartas de negocio"
    
    def __str__(self):
        return self.nombre
    
    def get_beneficios_por_turno(self):
        """Retorna los beneficios por turno como una lista"""
        return json.loads(self.beneficios_por_turno)
    
    def set_beneficios_por_turno(self, beneficios_lista):
        """Guarda los beneficios por turno como JSON"""
        self.beneficios_por_turno = json.dumps(beneficios_lista)

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

    # @property
    # def reglas_formateadas(self) -> list[str]:
    #     """Devuelve las reglas listas para mostrar en frontend"""
    #     return [f"• {regla}" for regla in self.atributos_juego] if self.atributos_juego else []

    mazo = models.ForeignKey(Mazo, on_delete=models.PROTECT, null=False, blank=False, related_name='cartas_personaje', verbose_name="Mazo")
    
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
    mazo = models.ForeignKey(Mazo, related_name='cartas_especiales', on_delete=models.PROTECT, null=False, blank=False, verbose_name="Mazo")
    
    class Meta:
        verbose_name = "Carta especial"
        verbose_name_plural = "Cartas especiales"
    
    def __str__(self):
        return self.titulo


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
    code = models.CharField(max_length=6, unique=True, default=generate_room_code, verbose_name="Código de sala")
    name = models.CharField(max_length=100, verbose_name="Nombre de la sala")
    max_participants = models.PositiveIntegerField(default=6, validators=[MinValueValidator(2), MaxValueValidator(10)], verbose_name="Máximo de participantes")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name="Estado")
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de creación")
    mazo = models.ForeignKey(Mazo, on_delete=models.PROTECT, related_name='rooms', verbose_name="Mazo")
    
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
    def is_started(self):
        return self.status == 'in_progress'
    
    @property
    def is_finished(self):
        return self.status == 'finished'
    # Borra el registro si la sala está finalizada y tiene más de un día de antigüedad
    def clean(self):
        if self.status == 'finished' and (timezone.now() - self.fecha_creacion).days > 1:
            self.delete()

class Participant(models.Model):
    """
    Modelo para representar un participante en una sala de juego.
    """
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('player', 'Jugador'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nombre")
    admin = models.BooleanField(default=False, verbose_name="Administrador")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='jugadores', verbose_name="Sala")
    carta_personaje = models.ManyToManyField(CartaPersonaje, related_name='jugadores', verbose_name="Carta de personaje")
    cartas_negocios = models.ManyToManyField(CartaNegocio, related_name='jugadores', verbose_name="Cartas de negocio")
    cartas_especiales = models.ManyToManyField(CartaEspecial, related_name='jugadores', verbose_name="Carta especial")
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
    extra_data = models.JSONField(default=dict, blank=True, null=True, verbose_name="Datos adicionales")
    fecha_ingreso = models.DateTimeField(default=timezone.now, verbose_name="Fecha de ingreso")
    
    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"
        ordering = ['fecha_ingreso']
        # Garantiza que no haya participantes duplicados en una misma sala
        unique_together = ['name', 'room']
    
    def __str__(self):
        return f"{self.name} ({self.room.code})"

