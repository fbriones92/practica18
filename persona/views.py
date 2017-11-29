from django.shortcuts import render
from persona.models import PersonaNatural, Provincia, Ciudad
from django.core.paginator import Paginator
from django.http.response import JsonResponse, HttpResponseBadRequest
# Create your views here.

def personas_naturales(request):
    personas = PersonaNatural.objects.all()
    
    query = ''
    
    if 'query' in request.GET:
        query = request.GET['query']
        personas = personas.filter(nombres__istartswith = query)
        
    paginator = Paginator(personas, 10)
    page = 1
    
    if 'page' in request.GET:
        page = int(request.GET['page'])

    pagina = paginator.page(page) 

    data = {
            'personas_naturales':pagina,
            'query':query
        }
    template = 'persona/personas_naturales.html'
    return render(request, template, data)


def consultarProvinciasAsJson(request):
    if request.method == 'POST' and "pais_id" in request.POST:
        pais_id = request.POST["pais_id"]
        if pais_id not in ('', None):
            provincias = Provincia.objects.filter(pais__id = pais_id)
            return JsonResponse([{'id':'', 'nombre':'Escoger una provincia'}] + [{'id': provincia.id, 'nombre':provincia.nombre} for provincia in provincias], safe=False)
        else:
            return JsonResponse([{'id':'', 'nombre':'Escoger una provincia'}], safe=False)
    else:
        return HttpResponseBadRequest("Se ha realizado un mal requerimiento")

def consultarCiudadAsJson(request):
    if request.method == 'POST' and "provincia_id" in request.POST:
        provincia_id = request.POST["provincia_id"]
        if provincia_id not in  ('', None):
            ciudades = Ciudad.objects.filter(provincia__id = provincia_id)
            return JsonResponse([{'id':'', 'nombre':'Escoger una ciudad'}] + [{'id': ciudad.id, 'nombre':ciudad.nombre} for ciudad in ciudades], safe=False)
        else:
            return JsonResponse([{'id':'', 'nombre':'Escoger una ciudad'}], safe=False)
    else:
        return HttpResponseBadRequest("Se ha realizado un mal requerimiento")
    
    
    
    
    