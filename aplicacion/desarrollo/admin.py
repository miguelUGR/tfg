from django.contrib import admin
from .models import Usuario,Observatorio,Observacion,User_Astronomo,User_Aficionado,Inscripciones
# Register your models here.

admin.site .register(Usuario)
admin.site .register(User_Astronomo)
admin.site .register(User_Aficionado)
admin.site .register(Observatorio)
# admin.site .register(Coordenadas)
admin.site .register(Observacion)
admin.site .register(Inscripciones)
