from django.db import models


# Create your models here.

class Cargo(models.Model):
    
    TIPO_CARGO_FUNCIONAL = 0
    TIPO_CARGO_CORPORATIVO = 1
    TIPO_CARGO_OPERATIVO = 2
    
    TIPO_CARGO_CHOICES = (
            (TIPO_CARGO_FUNCIONAL, 'Funcional'),
            (TIPO_CARGO_CORPORATIVO, 'Corporativo'),
            (TIPO_CARGO_OPERATIVO, 'Operativo'),
        )
    
    nombre = models.CharField(max_length = 200)
    nombre_abreviado = models.CharField(max_length = 30)
    requisitos = models.TextField(max_length = 200, null=True)
    responsabilidades = models.TextField(max_length = 200, null=True)
    tipo = models.SmallIntegerField(choices = TIPO_CARGO_CHOICES, null = True)
    
    def __str__(self):
        return self.nombre

    
    