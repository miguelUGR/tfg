from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario 

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = Usuario
#         fields = ('nombre','tipoCocina','alergenos','precio',)

class UsuarioCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Usuario
        fields = ('tipoUsuario',)


class UsuarioChangeForm(UserChangeForm):

    class Meta:
        model = Usuario
        fields = ('tipoUsuario',)
   