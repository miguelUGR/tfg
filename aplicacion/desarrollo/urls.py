# creo el fichero urls.py desde cero cero
from django.urls import path
from . import views

urlpatterns = [
    path('/hola/<nombre>/', views.hola, name='hola'),
]