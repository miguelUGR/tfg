from django.shortcuts import render
from django import forms 
from django.http import HttpResponseRedirect, HttpResponse ,JsonResponse
from .models import Observacion
from .forms import ObservacionForm

# Create your views here.
def hola(request , nombre): #tiene dos parameteos el request para coger datos y el nombre que le pasamos <>
    return render (request,"hola.html",{'nombre': nombre}) # nos vamos ha hola.html 

def iniciar(request):
    # return render (request,"login.html")
    return HttpResponseRedirect("/accounts/login/")
    
def base(request):
    # form = PostForm()
    # return render (request,"inicio.html",{'form': form})
    
    if request.user.is_authenticated:
        global user 
        user = request.user

    # for i in user:
    #     print (i)
    
    return render (request,"index.html",{'name_user': user})

def observaciones(request):
    
    # NOSE PK TENGO QUE ENVIAR EL USUARIO TAMBIEN PARA QUE ME APARZCA ARRIBA
    # CREO QUE NO EXTIENDE BIEN LA COSA
    observaciones=Observacion.objects.all()
    # for i in observaciones:
    #     print(i.nombre)
    return render (request,"observaciones.html",{'name_user': user,'observacion':observaciones})

def edit_observaciones(request):
    
    data = request.POST.copy() #cogo todo lo que me viene 
    nom_observacion = data['observacion']
    # print(nom_observacion)
    observacion = Observacion.objects.get(nombre=nom_observacion) #cogo de mi base de datos el que previamente habia seleccionado
    form = ObservacionForm(instance = observacion) #envio a la nueva pag.html el formulario pero rellenado con el plato seleccionado previamente
    
    return render(request, 'observaciones_edit.html', {'name_user': user,"form":form,"nom_observacion":nom_observacion})#tambien envio nombre del plato pk me hace falta

def modificar_observacion(request):
    
    data = request.POST.copy() #cogo todo lo que me viene
    if request.method == "POST":
        observacion_vieja = Observacion.objects.get(nombre=data['observacion_vieja']) #cojo el plato con el nombre digamos viejo, para que cuando le demos a guardar, GUARDE TODO LO RECIBIDO EN EL PLATO DIGAMOS YA EXISTENTE, pk imagina que cambiamos el nombre, pues para que no te cree uno nuevo,O QUE AL CAMBIAR EL NOMBRE, EN OTRO CAMPO ME HE EQUIVOCADO y repito, entonces debo tener el nombre viejo, pk aun no he modificado nada
        form = ObservacionForm(request.POST, instance=observacion_vieja) #Indicamos que el formulario que ha creado , tenga los datos que hemos rellenado y lo subcriba  en la instancia que le pasamos
        if form.is_valid():#aqui comprovamos que todo  son datos validados correctamente y lo guardamos
            form.save()  
            Listado_observaciones = Observacion.objects.all()
            return render(request,'observaciones.html',{'name_user': user,'observacion':Listado_observaciones})
    return render(request,'observaciones_edit.html',{'name_user': user,'form':form,"nom_observacion":data['observacion_vieja']})


