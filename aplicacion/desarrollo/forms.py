from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario
from .models import Observacion 
from allauth.account.forms import SignupForm

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = Usuario
#         fields = ('nombre','tipoCocina','alergenos','precio',)

#Las dos sigueintes clases, son para que me muestre en el navegador parte /admin, que cuando quera un nuevo usuario 
# este incluido lo que yo quiera, en este caso tipoUsuario(quen pondre por defecto aficionado y una opcion de que quiero o no ser astrofisico)
class UsuarioCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Usuario
        fields = ('tipoUsuario',)


class UsuarioChangeForm(UserChangeForm):

    class Meta:
        model = Usuario
        fields = ('tipoUsuario',)

class MiSignupForm(SignupForm):
    # Aqui lo que hago es para que me lo muestre a la hora de registrar nuevo usuario en la aplicacion
    # Como tengo en class Usuario un tipoUsuario, genero uno campo forms.MultipleChoiseField
    ATRO = 'AT'
    AFICIONADO = 'AF'

    TIPO_USUARIO = (
    (ATRO , "Atro"),
    (AFICIONADO , "Aficionado"))
    #LO QUE EH ECHO, es no me muestre la opcion de elegir usuario y por defecto ponga AFICIONADO
    # tipoUsuario= forms.MultipleChoiceField(widget=forms.Select, choices = TIPO_USUARIO )# idicio que sea forms.Select, en vez de forms.CheckboxSelectMultiple
    def signup(self, request, user): #para que lo cree y lo guarde 
        user.tipoUsuario = self.cleaned_data['tipoUsuario']
        user.save()
        return user

class ObservacionForm(forms.ModelForm):
    class Meta:
        model = Observacion 
        fields = ('nombre','fecha_observacion','latitude','longitude','duracion_ocultacion','hora_inicio','hora_final','descripcion','image','user',)

   