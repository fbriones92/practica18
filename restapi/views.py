from django.shortcuts import render
from rest_framework.views import APIView
from empleado.models import Empleado
from restapi.serializadores import EmpleadoSerializador
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class EmpleadoViewSet(APIView):
    
    def get(self, request, pk, format = None):
        empleado = Empleado.objects.get(id = pk)
        serializador = EmpleadoSerializador(empleado)
        return Response(serializador.data)
    
    def post(self, request, format=None):
        serializador = EmpleadoSerializador(data = request.data)
        if serializador.is_valid():     
            serializador.save()
            return Response(serializador.data, status = status.HTTP_201_CREATED)
        return Response(serializador.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format = None):
        empleado = Empleado.objects.get(id = pk)
        serializador = EmpleadoSerializador(empleado, data = request.data)
        if serializador.is_valid():     
            serializador.save()
            return Response(serializador.data, status = status.HTTP_201_CREATED)
        return Response(serializador.errors, status = status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk, format = None):
        empleado = Empleado.objects.get(id = pk)
        empleado.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        