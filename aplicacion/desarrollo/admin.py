from django.contrib import admin
from .models import Usuario, Observatorios,Observaciones
# Register your models here.

admin.site .register(Usuario)
admin.site .register(Observatorios)
# admin.site .register(Coordenadas)
admin.site .register(Observaciones)
