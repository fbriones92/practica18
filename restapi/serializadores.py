from rest_framework import serializers
'''
Created on 17 may. 2017

@author: Frank
'''
from empleado.models import Empleado
from persona.models import PersonaNatural
from django.contrib.auth.models import User

class EmpleadoSerializador(serializers.ModelSerializer):
    #persona_info = PersonaNaturalSerializador(read_only=True)
    #usuario_info = UsuarioSerializador(read_only=True)
    nombres = serializers.ReadOnlyField(source='persona.nombres', read_only=True)
    apellido_paterno = serializers.ReadOnlyField(source='persona.apellido_paterno', read_only=True)
    nombre_usuario = serializers.ReadOnlyField(source='usuario.username', read_only=True)
    
    
    class Meta:
        model = Empleado
        fields = ('id', 'estado', 'observaciones', 'persona','nombres', 'apellido_paterno', 
                  'usuario', 'nombre_usuario')
    

        
        
        
        