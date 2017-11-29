# -*- coding: utf-8 -*-
'''
Created on 22 may. 2017

@author: frankcarlos
'''
#from django.forms import ModelForm
from empleado.models import Empleado, PlazaTrabajo
from django.contrib.gis import forms
from persona.models import Persona, PersonaNatural, Pais, Provincia, Ciudad
from django.contrib.auth.models import User
from random import choice
from distutils.command.clean import clean
from django.utils.translation import ugettext_lazy as _
from django.urls.base import reverse_lazy
#from mapwidgets.widgets import GooglePointFieldWidget
from django.contrib.gis.geos.point import Point


# from django.forms.widgets import Textarea, CheckboxSelectMultiple, Select,\
#     SelectMultiple
# 
# class EmpleadoForm(ModelForm):
#     class Meta:
#         model = Empleado
#         #fields = ['persona', 'estado', 'observaciones', 'plazas_trabajo', 'usuario']
#         fields = '__all__'
#         widgets = {
#             'plazas_trabajo': SelectMultiple(attrs={'style': 'width:800px; height:400px'}),
#         }
#         labels = {    
#             'plazas_trabajo': 'Plazas de trabajo'
#         }
# #         help_texts = {
# #             'name': _('Some useful help text.'),
# #         }
# #         error_messages = {
# #             'name': {
# #                 'max_length': _("This writer's name is too long."),
# #             },
# #         }


class EmpleadoForm(forms.Form):
    
    cedula = forms.CharField(required=False, label=u'Cédula')
    nombres = forms.CharField(max_length=250,  widget=forms.TextInput(attrs={'size':'30'}))
    apellido_paterno = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'size':'30'}))
    apellido_materno = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'size':'30'}), required=False)
    
    pais = forms.ModelChoiceField(queryset=Pais.objects.all(),empty_label="Escoger un pais", 
        widget=forms.Select(attrs={'placeholder':'País', 'onChange':"getProvincias(this.value)"}))
    provincia = forms.ModelChoiceField(queryset=Provincia.objects.none(), empty_label="Escoger una provincia", 
        widget=forms.Select(attrs={'placeholder':'Provincia o estado', 'onChange':"getCiudades(this.value)"}))
    ciudad = forms.ModelChoiceField(queryset=Ciudad.objects.none(), empty_label="Escoger una ciudad", widget=forms.Select(attrs={'placeholder':'Ciudad o Cantón'}))
    
    sexo = forms.ChoiceField(choices=PersonaNatural.SEXO_CHOICES, required=True)
    fecha_nacimiento = forms.DateField(required = False)
    observaciones = forms.CharField( widget=forms.Textarea())
    usuario = forms.CharField(max_length=13, widget=forms.TextInput(attrs={'size':'30'}))
    contrasenia = forms.CharField(max_length=13, widget=forms.PasswordInput(attrs={'size':'30'}))
    email = forms.EmailField(max_length=25, widget=forms.TextInput(attrs={'size':'30'}))
    plazas_trabajo = forms.ModelMultipleChoiceField(queryset=PlazaTrabajo.objects.all(), widget = forms.SelectMultiple)
    foto = forms.ImageField(required=False)
    
    def modificarQuerySet(self, pais_id, provincia_id):
        if pais_id not in ('', None):
            self.fields['provincia'].queryset = Provincia.objects.filter(pais__id = pais_id)
            
        if provincia_id not in ('', None):
            self.fields['ciudad'].queryset = Ciudad.objects.filter(provincia__id = provincia_id)
    
    def save(self, empleado = None):
        cleaned_data = super(EmpleadoForm, self).clean()

        if empleado is None:
            persona = Persona()
            persona.tipo = Persona.TIPO_PERSONA_NATURAL
            persona.observaciones = cleaned_data["observaciones"]
            persona.ruc = cleaned_data["cedula"]
            persona.nombre_comercial = ""
            persona.save()
             
            usuario = User()
            usuario.username = cleaned_data["usuario"]
            usuario.set_password(cleaned_data["contrasenia"])
            usuario.email = cleaned_data["email"]
            usuario.save()
             
            persona_natural = PersonaNatural()
            persona_natural.ciudad_nacimiento = cleaned_data['ciudad']
            persona_natural.cedula = cleaned_data["cedula"]
            persona_natural.nombres = cleaned_data["nombres"]
            persona_natural.apellido_paterno = cleaned_data["apellido_paterno"]
            persona_natural.apellido_materno = cleaned_data["apellido_materno"]
            persona_natural.persona = persona
            persona_natural.sexo = cleaned_data["sexo"]
            persona_natural.fecha_nacimiento = cleaned_data["fecha_nacimiento"]
            persona_natural.save()
             
             
            empleado = Empleado()
            empleado.persona = persona_natural
            empleado.usuario = usuario
            empleado.foto = cleaned_data["foto"]
            empleado.observaciones = cleaned_data["observaciones"]
            empleado.save()
            empleado.plazas_trabajo = cleaned_data["plazas_trabajo"]
            empleado.save()
        else:
            empleado.persona.nombres = cleaned_data["nombres"]
            empleado.persona.apellido_paterno = cleaned_data["apellido_paterno"]
            empleado.persona.apellido_materno = cleaned_data["apellido_materno"]
            empleado.persona.sexo = cleaned_data["sexo"]
            empleado.persona.cedula = cleaned_data["cedula"]
            empleado.persona.ciudad_nacimiento = cleaned_data["ciudad"]
            empleado.persona.save()
            
            empleado.usuario.email = cleaned_data["email"]
            empleado.usuario.save()
            
            empleado.foto = cleaned_data["foto"]
            empleado.observaciones = cleaned_data["observaciones"]
            empleado.save()
            
            empleado.plazas_trabajo = cleaned_data["plazas_trabajo"]
            empleado.save() 
    
        return empleado
    
    
    def clean_usuario(self):
        if self.cleaned_data['usuario']:
                p = User.objects.filter(username = self.cleaned_data['usuario'])
                if len(p) > 0:
                    raise forms.ValidationError(_("Ya esxiste un usuario con este username"))
        return self.cleaned_data['usuario']
    

class PlazaTrabajoForm(forms.ModelForm):
    class Meta:
        model = PlazaTrabajo
        fields = '__all__'
        exclude=['coordenadas']
        
    def save(self, commit=True):
        plaza_trabajo = super(PlazaTrabajoForm, self).save(commit=False)
        punto = Point(plaza_trabajo.longitud, plaza_trabajo.latitud)
        plaza_trabajo.coordenadas = punto
        if commit:
            plaza_trabajo.save()
        return plaza_trabajo

    
    