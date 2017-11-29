'''
Created on 8 may. 2017

@author: Frank
'''

from django.conf.urls import url
from persona.views import personas_naturales, consultarProvinciasAsJson,\
    consultarCiudadAsJson

urlpatterns = [
    url(r'^personasnaturales/$', personas_naturales),
    url(r'^provinciasAsJson/$', consultarProvinciasAsJson, name='provinciasAsJson'),
    url(r'^ciudadAsJson/$', consultarCiudadAsJson, name='ciudadAsJson'),
]
