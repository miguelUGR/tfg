# creo el fichero urls.py desde cero cero
from django.urls import path
from . import views



urlpatterns = [
    #path('accounts/', include('allauth.urls')),  #p6
    path('hola/<nombre>/', views.hola, name='hola'),
] 

