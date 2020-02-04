# creo el fichero urls.py desde cero cero
from django.urls import path
from . import views

 #en el path el primer y tercer elemento(name) tienen que ser igual

urlpatterns = [

    path('hola/<nombre>/', views.hola, name='hola'),
    path('inicio',views.iniciar, name='inicio'),
    path('base',views.base, name='base'),
    path('observacion',views.observaciones,name='observacion'),
    path('editar_observaciones',views.edit_observaciones,name='editar_observaciones'),
    path('modificar_observacion', views.modificar_observacion, name="modificar_observacion"),

] 

