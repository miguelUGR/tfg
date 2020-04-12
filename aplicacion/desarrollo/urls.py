# creo el fichero urls.py desde cero cero
from django.urls import path
from . import views

 #en el path el primer y tercer elemento(name) tienen que ser igual

urlpatterns = [

    path('hola/<nombre>/', views.hola, name='hola'),
    path('index2', views.hola2, name='index2'),
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
    path('editar_inscripcion',views.edit_inscripciones,name='editar_inscripcion'),
    path('modificar_inscripcion',views.modificar_inscripcion,name='modificar_inscripcion'),
    path('borrar_inscripcion',views.borrar_inscripciones,name='borrar_inscripcion'),
    path('borrar_confirmado_inscripcion',views.borrar_confirmado_inscripcion,name='borrar_confirmado_inscripcion'),
    path('crear_inscripcion',views.crear_inscripcion,name='crear_inscripcion'),
    path('crear_inscripcion_all',views.crear_inscripcion_all,name='crear_inscripcion_all'),
    path('crear_desinscripcion_all',views.crear_desinscripcion_all,name='crear_desinscripcion_all'),

    path('editar_usuario',views.edit_user,name='editar_usuario'),
    path('modificar_usuario',views.modificar_user,name='modificar_usuario'),

    path('edit_passwd',views.edit_passwd,name='edit_passwd'),

    path('listado_observaciones',views.listado_observaciones,name='listado_observaciones'),
    path('listado_observatorios',views.listado_observatorios,name='listado_observatorios'),
    path('listado_notificaciones',views.listado_notificaciones,name='listado_notificaciones'),
    path('ver_observacion',views.ver_observacion,name='ver_observacion'),
    path('ver_observatorio',views.ver_observatorio,name='ver_observatorio'),
    path('ver_observatorio_all',views.ver_observatorio_all,name='ver_observatorio_all'),

    path('solicitudAstro',views.solicitudAstro,name='solicitudAstro'),
    path('aceptar_notifi_Astro',views.aceptar_notifi_Astro,name='aceptar_notifi_Astro'),
    path('denegar_notifi_Astro',views.denegar_notifi_Astro,name='denegar_notifi_Astro'),

    path('borrar_confirmado_notifi_Astro',views.borrar_confirmado_notifi_Astro,name='borrar_confirmado_notifi_Astro'),

] 

