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

#--ESTO ES PARA  visualizacion mas bonita en http://127.0.0.1:8000/admin/desarrollo/usuario/
class UsuarioAdmin(UserAdmin):
    # add_form = UsuarioCreationForm
    # form = UsuarioChangeForm
    # model = Usuario
    list_display = ('username', 'is_staff', 'is_active','tipoUsuario') #PARA QUE SE VEAN LAS COLUMNAS  EN LA TABLA DONDE SE LISTAN TODOS LOS USUARIOS
    # slist_filter = ('username', 'is_staff', 'is_active','tipoUsuario')
    # fieldsets = ( # PARA EDITAR USUARIO
    #         (None, {
    #             'fields': ('username', 'password','tipoUsuario')}),
    #         # ('Permissions', {'fields': ('is_staff', 'is_active')}),
    #     )
    # add_fieldsets = ( # PARA AÑADIR NUEVO USUARIO
    #         (None, {
    #             'classes': ('wide',),
    #             # 'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active','tipoUsuario')}
    #             'fields': ('username', 'password1', 'password2','tipoUsuario')}
    #         ),
    #     )
    # search_fields = ('username',)
    # ordering = ('username',)

admin.site.unregister(Usuario) #para que no de problemas al actualizar
admin.site.register(Usuario, UsuarioAdmin) 