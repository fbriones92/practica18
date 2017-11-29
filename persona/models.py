from django.db import models
from random import choice


    
class Pais(models.Model):
    nombre = models.CharField(max_length = 250)
    
    def __str__(self):
        return self.nombre
    
class Provincia(models.Model):
    nombre = models.CharField(max_length = 250)
    pais = models.ForeignKey(Pais)
    
    def __str__(self):
        return "%s - %s" % (self.nombre, self.pais.nombre)

class Ciudad(models.Model):
    nombre = models.CharField(max_length = 250)
    provincia = models.ForeignKey(Provincia)
    
    def __str__(self):
        return "%s - %s - %s" % (self.nombre, self.provincia.nombre, self.provincia.pais.nombre)

# Create your models here.
class Persona(models.Model):
    
    TIPO_PERSONA_NATURAL = 0
    TIPO_PERSONA_JURIDICA = 1
    TIPO_PERSONA_CHOICES = (
            (TIPO_PERSONA_JURIDICA, 'Persona juridica'),
            (TIPO_PERSONA_NATURAL, 'Persona natural'),
        )
    
    ruc = models.CharField(max_length = 13, null = True)
    nombre_comercial = models.CharField(max_length = 200, null = True)
    observaciones = models.TextField(max_length = 2000, 
                                     null = True, blank = True)
    actividad_economica = models.TextField(null = True)
    producto_servicio = models.TextField(null = True)
    
    tipo = models.SmallIntegerField(choices = TIPO_PERSONA_CHOICES)
    
    def __str__(self):
        return "%d" % self.id
    
class PersonaNatural(models.Model):
    SEXO_MASCULINO = 0
    SEXO_FEMENINO = 1
    SEXO_CHOICES = (
            (SEXO_MASCULINO, 'Masculino'),
            (SEXO_FEMENINO, 'Femenino'),
        )
    
    cedula = models.CharField(max_length = 10)
    pasaporte= models.CharField(max_length = 15, null = True)
    persona = models.OneToOneField(Persona)
    nombres = models.CharField(max_length = 250)
    apellido_paterno = models.CharField(max_length = 250)
    apellido_materno = models.CharField(max_length = 250, null = True)
    sexo = models.SmallIntegerField(choices = SEXO_CHOICES)
    fecha_nacimiento = models.DateField(null = True)
    ciudad_nacimiento = models.ForeignKey(Ciudad, null = True, blank = True)
    
    def __str__(self):
        return "%s %s" % (self.apellido_paterno, self.nombres)
    

class Empresa(models.Model):
    persona = models.OneToOneField(Persona)
    razon_social = models.CharField(max_length = 250)
    fecha_constitucion = models.DateField(null = True)
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        