from django.contrib import admin
from persona.models import Pais, Provincia, Ciudad

# Register your models here.
admin.site.register(Pais)
admin.site.register(Ciudad)
admin.site.register(Provincia)