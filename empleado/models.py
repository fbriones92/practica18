# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from persona.models import PersonaNatural
from organizacion.models import Cargo
from django.contrib.auth.models import User
from django.utils.html import format_html



class PlazaTrabajo(models.Model):
    cargo = models.ForeignKey(Cargo)
    numero_puestos = models.IntegerField()
    latitud = models.FloatField(default=0, null = True)
    longitud = models.FloatField(default=0, null=True)
    coordenadas = models.PointField(null = True)
    objects = models.GeoManager()
    
    def __str__(self):
        return "%s" % self.cargo.nombre

# Create your models here.
class Empleado(models.Model):
    ESTADO_ACTIVO = 0
    ESTADO_INACTIVO = 1
    ESTADO_CHOICES = (
            (ESTADO_ACTIVO, 'Activo'),
            (ESTADO_INACTIVO, 'Inactivo'),
        )
    
    persona = models.ForeignKey(PersonaNatural)
    estado = models.SmallIntegerField(choices = ESTADO_CHOICES, default = ESTADO_ACTIVO)
    observaciones = models.TextField(max_length = 2000, null=True)
    plazas_trabajo = models.ManyToManyField(PlazaTrabajo)
    usuario = models.OneToOneField(User, null=True, blank=True)
    foto = models.ImageField(upload_to= "fotos", null=True, blank=True)
    
    class Meta:
        permissions = (
                ('genera_nomina', 'Puede generar la nómina'),
            ) 
    
    def __str__(self):
        return self.persona.apellido_paterno + " " + self.persona.nombres
    
    def nombres(self):
        return format_html(
            '<span style="color: red;">{} {}</span>',
            #self.color_code,
            self.persona.apellido_paterno,
            self.persona.nombres,
        )
    
    def as_data(self):
        dic= self.__dict__
        dic['usuario'] = self.usuario.username
        dic['nombres'] = self.persona.nombres
        dic['apellido_paterno'] = self.persona.apellido_paterno
        dic['apellido_materno'] = self.persona.apellido_materno
        dic['cedula'] = self.persona.cedula
        dic['sexo'] = self.persona.sexo
        dic['email'] = self.usuario.email
        dic['plazas_trabajo'] = self.plazas_trabajo.all()
        dic['foto'] = self.foto
        dic['fecha_nacimiento'] = self.persona.fecha_nacimiento
        dic['ciudad'] = self.persona.ciudad_nacimiento
        dic['provincia'] = self.persona.ciudad_nacimiento.provincia
        dic['pais'] = self.persona.ciudad_nacimiento.provincia.pais
        
        return dic
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    