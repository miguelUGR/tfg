from django.contrib import admin
from .models import Usuario,Observatorios,Observaciones,User_Astronomo,User_Aficionado
# Register your models here.

admin.site .register(Usuario)
admin.site .register(User_Astronomo)
admin.site .register(User_Aficionado)
admin.site .register(Observatorios)
# admin.site .register(Coordenadas)
admin.site .register(Observaciones)
