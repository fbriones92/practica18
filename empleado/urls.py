'''
Created on 10 may. 2017

@author: Frank
'''
from django.conf.urls import url
from empleado.views import empleado, empleados, eliminar, plaza_trabajo, buscar_plaza_trabajo
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    url(r'^$', empleados, name="empleados"),
    url(r'^crear/$', empleado, name="empleado"),
    url(r'^crear/(?P<empleado_id>\d+)/$', empleado, name="empleado"),
    url(r'^eliminar/(?P<empleado_id>\d+)/', eliminar, name="eliminar_empleado"),
    url(r'^plaza_trabajo/$', plaza_trabajo, name="plaza_trabajo"),
    url(r'^plaza_trabajo/busqueda/$', buscar_plaza_trabajo, name='buscar_plaza_trabajo'),
    
]