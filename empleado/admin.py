from django.contrib.gis import admin
from empleado.models import Empleado, PlazaTrabajo

def activar_empleado(modeladmin, request, queryset):
    queryset.update(estado=Empleado.ESTADO_ACTIVO)
activar_empleado.short_description = "Activar empleados masivamente"

class EmpleadoAdmin(admin.ModelAdmin):
    fields = (('estado', 'observaciones'), 'persona')
    list_filter =['usuario__username', 'estado']
    search_fields = ['plazas_trabajo__cargo__nombre', 'persona__apellido_paterno']
    actions = [activar_empleado]
    list_display = ('nombres', 'estado',)
    

# Register your models here.
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(PlazaTrabajo, admin.OSMGeoAdmin)