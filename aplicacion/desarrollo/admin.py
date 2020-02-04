from django.contrib import admin
from .models import Usuario,Observatorio,Observacion,Inscripciones

from django.contrib.auth.admin import UserAdmin
from .forms import UsuarioCreationForm, UsuarioChangeForm

# Register your models here. 

# --------PARA QUE SE VEAN LOS MODELOS EN 127.0.0.0.1:8000/admin....----------

admin.site .register(Usuario)
# admin.site .register(User_Astronomo)
# admin.site .register(User_Aficionado)
admin.site .register(Observatorio)
admin.site .register(Observacion)
admin.site .register(Inscripciones)


