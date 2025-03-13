from django.db import models
from django.utils import timezone
import json

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
        ordering = ['-fecha_creacion']

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
    plus_de_beneficio = models.FloatField(verbose_name="Plus de beneficio")
    
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
    titulo = models.CharField(max_length=100, verbose_name="Título")
    subtitulo = models.CharField(max_length=200, blank=True, verbose_name="Subtítulo")
    tipo = models.ForeignKey(TipoDeNegocio, on_delete=models.CASCADE, verbose_name="Tipo")
    costo = models.PositiveIntegerField(verbose_name="Costo")
    mazo = models.ForeignKey(Mazo, related_name='cartas_negocio', on_delete=models.CASCADE, verbose_name="Mazo")
    niveles_soportados = models.ManyToManyField(NivelDeNegocio, related_name='cartas', verbose_name="Niveles soportados")
    beneficio_base = models.FloatField(verbose_name="Beneficio base")
    beneficios_por_turno = models.TextField(default='Produce (4 * (nivel de negocio)) wachines por turno.', verbose_name="Beneficios por turno en cada nivel")
    
    class Meta:
        verbose_name = "Carta de negocio"
        verbose_name_plural = "Cartas de negocio"
    
    def __str__(self):
        return self.titulo
    
    def get_beneficios_por_turno(self):
        """Retorna los beneficios por turno como una lista"""
        return json.loads(self.beneficios_por_turno)
    
    def set_beneficios_por_turno(self, beneficios_lista):
        """Guarda los beneficios por turno como JSON"""
        self.beneficios_por_turno = json.dumps(beneficios_lista)

class AtributoPersonaje(models.Model):
    """
    Modelo para representar atributos de personajes.
    """
    karma = models.IntegerField(default=0, verbose_name="Karma")
    dinero = models.FloatField(default=0, verbose_name="Dinero")
    fama = models.IntegerField(default=0, verbose_name="Fama")
    extra = models.TextField(default='Recive $100 en cada turno', blank=True, null=True, verbose_name="Atributos extra")
    
    class Meta:
        verbose_name = "Atributo de personaje"
        verbose_name_plural = "Atributos de personaje"
    
    def __str__(self):
        return f"Karma: {self.karma}, Dinero: {self.dinero}, Fama: {self.fama}"

class CartaPersonaje(models.Model):
    """
    Modelo para representar cartas de personajes.
    """
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino')
    ]
    
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    historia = models.TextField(verbose_name="Historia")
    edad = models.PositiveIntegerField(verbose_name="Edad")
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name="Sexo")
    imagen = models.ImageField(upload_to='personajes/', blank=True, null=True, verbose_name="Imagen")
    atributos = models.OneToOneField(AtributoPersonaje, on_delete=models.CASCADE, verbose_name="Atributos")
    mazo = models.ForeignKey(Mazo, related_name='cartas_personaje', on_delete=models.CASCADE, verbose_name="Mazo")
    
    class Meta:
        verbose_name = "Carta de personaje"
        verbose_name_plural = "Cartas de personaje"
    
    def __str__(self):
        return f"{self.nombre} ({self.edad} años)"

class CartaEspecial(models.Model):
    """
    Modelo para representar cartas especiales.
    """
    titulo = models.CharField(max_length=100, verbose_name="Título")
    frase = models.CharField(max_length=200, verbose_name="Frase")
    consigna = models.TextField(verbose_name="Consigna")
    imagen = models.ImageField(upload_to='especiales/', blank=True, null=True, verbose_name="Imagen")
    mazo = models.ForeignKey(Mazo, related_name='cartas_especiales', on_delete=models.CASCADE, verbose_name="Mazo")
    
    class Meta:
        verbose_name = "Carta especial"
        verbose_name_plural = "Cartas especiales"
    
    def __str__(self):
        return self.titulo
