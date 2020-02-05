from django.shortcuts import render
from django import forms 
from django.http import HttpResponseRedirect, HttpResponse ,JsonResponse
from .models import Observacion, Observatorio
from .forms import ObservacionForm, ObservatorioForm
from django.shortcuts import redirect #para redireccionar
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
        global user,usuario_registrado
        user = request.user # PARA el template indice.html que permanezca el usuario registrado
        usuario_registrado=user.id # Para view.py y poder hacer filtrado de objetos del propio usuario

    # for i in user:
    #     print (i)
    
    return render (request,"index.html",{'name_user': user})

def observaciones(request):

    # observaciones=Observacion.objects.all()
    # observaciones= observaciones.filter(user_id = usuario_registrado)

    # ----las dos lineas anteriores hacen lo mismo que la siguiente ----
    observaciones=Observacion.objects.all().filter(user= usuario_registrado)
    # print (user.id)
    # for i in observaciones:
    #     print(i.user)
    return render (request,"observaciones.html",{'name_user': user,'observacion':observaciones})


def observatorios(request):
    observatorios=Observatorio.objects.all().filter(user = usuario_registrado)
    # observatorios=ObservatorioForm.objects.all().filter(user= usuario_registrado)
    return render (request,"observatorios.html",{'name_user': user,'observatorio':observatorios})
   
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def edit_observaciones(request):
    data = request.POST.copy() #cogo todo lo que me viene 
    nom_observacion = data['observacion']
    # print(nom_observacion)
    observacion = Observacion.objects.get(nombre = nom_observacion) #cogo de mi base de datos el que previamente habia seleccionado
    form = ObservacionForm(instance = observacion) #envio a la nueva pag.html el formulario pero rellenado con el plato seleccionado previamente
    return render(request, 'observaciones_edit.html', {'name_user': user,"form":form,"nom_observacion":nom_observacion})#tambien envio nombre del plato pk me hace falta

def edit_observatorios(request):
    data = request.POST.copy() #cogo todo lo que me viene 
    request.session['observatorio_viejo']=data['observatorio'] #creo variable de sesion del observatorio seleccionado para editar y asi evito el enviar y recibir campos ocultos (hidde)con datos  para modificar_observatorio
    # print('----HOLA----')
    observatorio= Observatorio.objects.get(nombre = request.session['observatorio_viejo'])
    form = ObservatorioForm(instance = observatorio )
    return render(request, 'observatorios_edit.html',{'name_user':user,'form':form,'nom_observatorio':request.session['observatorio_viejo']} )

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def modificar_observacion(request):
    data = request.POST.copy() #cogo todo lo que me viene
    if request.method == "POST":
        observacion_vieja = Observacion.objects.get(nombre=data['observacion_vieja']) #cojo el plato con el nombre digamos viejo, para que cuando le demos a guardar, GUARDE TODO LO RECIBIDO EN EL PLATO DIGAMOS YA EXISTENTE, pk imagina que cambiamos el nombre, pues para que no te cree uno nuevo,O QUE AL CAMBIAR EL NOMBRE, EN OTRO CAMPO ME HE EQUIVOCADO y repito, entonces debo tener el nombre viejo, pk aun no he modificado nada
        form = ObservacionForm(request.POST, instance=observacion_vieja) #Indicamos que el formulario que ha creado , tenga los datos que hemos rellenado y lo subcriba  en la instancia que le pasamos
        if form.is_valid():#aqui comprovamos que todo  son datos validados correctamente y lo guardamos
            form.save()  
            return redirect(observaciones)
    return render(request,'observaciones_edit.html',{'name_user': user,'form':form,'nom_observacion':data['observacion_vieja']})
    
def modificar_observatorio(request):
    if request.session['observatorio_viejo']: #ME AHORRO el hacer observatorio_viejo etc como en observaciones
        data = request.POST.copy() #cogo todo lo que me viene
        if request.method == "POST":
            observatorio_viejo=Observatorio.objects.get(nombre=request.session['observatorio_viejo'])
            form = ObservatorioForm(request.POST, instance=observatorio_viejo )
            if form.is_valid():
                form.save()
                return redirect(observatorios)
            return render(request,'observatorios_edit.html',{'name_user':user,'form':form})




#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def crear_observaciones(request):
    #la primera vez que entra a qui, como no hay digamos nada(POST), 
    # se va al else: , crea el formulario y redireccionamos
    print ('hola1')
    if request.method == 'POST':
        print ('hola3')
        form = ObservacionForm(request.POST)
        if form.is_valid():
            print ('hola4')
            observacion = form.save()#coge todo lo del formulario y lo guarda. El nombre he puesto plato, pero puedo poner lo que quiera, ya que el form.save esta referenciado al formulario de PlatoForm
            return redirect(observaciones)
        # else:
        #     return redirect(observaciones)
    else:
        form = ObservacionForm()
        print ('hola2')
    return render(request,'observaciones_register.html',{'name_user': user,'form':form})


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def borrar_observaciones(request):
    data = request.POST.copy()
    request.session['observacion_borrar']=data['observacion']
    return render(request,'observaciones_borrado.html',{'name_user': user})

def borrar_confirmado_observacion(request):
    if request.session['observacion_borrar']:
        observacion=Observacion.objects.get(nombre=request.session['observacion_borrar'])
        observacion.delete()
        return redirect(observaciones)

def borrar_observatorio(request):
    data = request.POST.copy()
    request.session['observatorio_borrar']= data['observatorio']
    return render(request,'observatorios_borrado.html',{'name_user':user})

def borrar_confirmado_observatorio(request):
    if request.session['observatorio_borrar']:
        observatorio=Observatorio.objects.get(nombre=request.session['observatorio_borrar'])
        observatorio.delete()
        return redirect(observatorios)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




        



