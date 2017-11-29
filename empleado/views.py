# -*- coding: utf-8 -*-
from django.shortcuts import render
from persona.models import PersonaNatural, Persona
from empleado.models import PlazaTrabajo, Empleado
from django.http.response import HttpResponseRedirect, JsonResponse
from django.urls.base import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth.decorators import permission_required
from organizacion.models import Cargo
from django.db.models import Q
from empleado.forms import EmpleadoForm, PlazaTrabajoForm
from django.conf import settings
from django.contrib.gis.geos.point import Point

# Create your views here.
@permission_required('auth.add_user')
@permission_required('empleado.add_empleado')
@permission_required('persona.add_persona')
@permission_required('persona.add_personanatural')
@transaction.atomic
def empleado(request, empleado_id = None):
    
    def eliminar_campos(formulario):
        del form.fields['usuario']
        del form.fields['contrasenia']
    
    template = 'empleado/nuevo_empleado.html'
    form = EmpleadoForm()
    empleado = None
    
    if empleado_id is not None:
        empleado = Empleado.objects.get(id = empleado_id)
        form = EmpleadoForm(initial = empleado.as_data())
        form.modificarQuerySet(empleado.persona.ciudad_nacimiento.provincia.pais.id, empleado.persona.ciudad_nacimiento.provincia.id)
        eliminar_campos(form)
    
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES)
        form.modificarQuerySet(request.POST["pais"], request.POST["provincia"])
        
        if empleado is not None:
            eliminar_campos(form)
        
        if form.is_valid():
            form.save(empleado)
            request.session['msg'] = "Empleado creado con éxito"
            return HttpResponseRedirect(reverse('empleados'))
    
    data = {'form':form}
    return render(request, template, data) 
    
    
    
#    CON MODELS-FORM
#     template = 'empleado/nuevo_empleado.html'
#     form = EmpleadoForm()
#     empleado = None
#     
#     if empleado_id is not None:
#         empleado = Empleado.objects.get(id = empleado_id)
#         form = EmpleadoForm(instance = empleado)
#     
#     if request.method == 'POST':
#         form = EmpleadoForm(request.POST, request.FILES, instance = empleado)
#         if form.is_valid():
#             form.save()
#             request.session['msg'] = "Empleado creado con éxito"
#             return HttpResponseRedirect(reverse('empleados'))
#         
#     
#     
#     data = {'form':form}
#     return render(request, template, data) 
        
    
    
    

def empleados(request):
    msg = None
    if 'msg' in request.session:
        msg = request.session['msg']
        del request.session['msg']
    
    template = 'empleado/empleados.html'
    
#     empleados = Empleado.objects.filter(
#                 Q(plazas_trabajo__cargo__nombre__istartswith = "gerente") |
#                 Q(persona__sexo = PersonaNatural.SEXO_FEMENINO) & 
#                 Q(estado = Empleado.ESTADO_ACTIVO)).distinct().order_by("-persona__nombres")
    empleados = Empleado.objects.all()
    data = {
            'msg':msg,
            #'empleados':Empleado.objects.filter(
            #    persona__sexo = PersonaNatural.SEXO_FEMENINO)
            #'empleados':Empleado.objects.filter(
            #plazas_trabajo__cargo__tipo = Cargo.TIPO_CARGO_FUNCIONAL).distinct().order_by("persona__apellido_paterno")
            #'empleados':Empleado.objects.filter(
            #    plazas_trabajo__cargo__nombre__istartswith = "gerente")
            #.distinct()
            'empleados': empleados,
            'MEDIA_URL':settings.MEDIA_URL
            
        }
    return render(request, template, data)

def eliminar(request, empleado_id):
    empleado = Empleado.objects.get(id = empleado_id)
    empleado.delete()
    request.session['msg'] = "Empleado eliminado con éxito"
    return HttpResponseRedirect(reverse('empleados'))

def plaza_trabajo(request):
    form = PlazaTrabajoForm()
    data = {'form': form}
    template = 'plaza_trabajo/plaza_trabajo.html'
    
    if request.method == 'POST':
        form = PlazaTrabajoForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['msg'] = "Plaza de trabajo creada con éxito"
            return HttpResponseRedirect(reverse('empleados'))
    
    return render(request, template, data)

def buscar_plaza_trabajo(request):
    data = {}
    templeate = 'plaza_trabajo/busqueda_plaza_trabajo.html'
    if request.method == 'POST' and 'lat' in request.POST and 'lng' in request.POST and 'radio' in request.POST:
        centro = Point(float(request.POST['lng']), float(request.POST['lat']))
        radio_busqueda = centro.buffer(int(request.POST['radio']) / 100)
        plazas_trabajo = PlazaTrabajo.objects.filter(coordenadas__contained = radio_busqueda)     
        return JsonResponse([{'lat': plaza.coordenadas.y, 'lng':plaza.coordenadas.x, 'nombre':plaza.cargo.nombre} for plaza in plazas_trabajo], safe=False)

    return render(request, templeate, data)





