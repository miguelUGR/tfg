# creo el fichero urls.py desde cero cero
from django.urls import path
from . import views

 #en el path el primer y tercer elemento(name) tienen que ser igual

urlpatterns = [

    path('hola/<nombre>/', views.hola, name='hola'),
    path('inicio',views.iniciar, name='inicio'),
    path('base',views.base, name='base'),

    path('observacion',views.observaciones,name='observacion'),
    path('editar_observacion',views.edit_observaciones,name='editar_observacion'),
    path('modificar_observacion', views.modificar_observacion, name='modificar_observacion'),
    path('crear_observacion',views.crear_observaciones,name='crear_observacion'),
    path('borrar_observacion',views.borrar_observaciones,name='borrar_observacion'),
    path('borrar_confirmado_observacion',views.borrar_confirmado_observacion,name='borrar_confirmado_observacion'),

    path('observatorio',views.observatorios,name='observatorio'),
    path('editar_observatorio',views.edit_observatorios,name='editar_observatorio'),
    path('modificar_observatorio',views.modificar_observatorio,name='modificar_observatorio'),
    path('borrar_observatorio',views.borrar_observatorio,name='borrar_observatorio'),
    path('borrar_confirmado_observatorio',views.borrar_confirmado_observatorio,name='borrar_confirmado_observatorio'),
    path('crear_observatorio',views.crear_observatorio,name='crear_observatorio'),

    path('inscripcion',views.inscripciones,name='inscripcion'),
    path('borrar_inscripcion',views.borrar_inscripciones,name='borrar_inscripcion'),
    path('borrar_confirmado_inscripcion',views.borrar_confirmado_inscripcion,name='borrar_confirmado_inscripcion'),
    path('crear_inscripcion',views.crear_inscripcion,name='crear_inscripcion'),

] 

