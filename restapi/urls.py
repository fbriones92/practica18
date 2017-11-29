'''
Created on 17 may. 2017

@author: Frank
'''
from django.conf.urls import url
from restapi.views import EmpleadoViewSet

urlpatterns = [
    url(r'^empleado/(?P<pk>\d+)/', EmpleadoViewSet.as_view()),
    url(r'^empleado/', EmpleadoViewSet.as_view()),
    
]