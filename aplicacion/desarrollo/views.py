from django.shortcuts import render
from django import forms 
from django.http import HttpResponseRedirect, HttpResponse ,JsonResponse
from .models import Observacion, Observatorio, Inscripciones, Usuario
from .forms import ObservacionForm, ObservatorioForm, InscripcionesForm, UsuarioChangeForm
from django.contrib import messages 
from django.shortcuts import redirect #para redireccionar
# Create your views here.
def hola(request , nombre): #tiene dos parameteos el request para coger datos y el nombre que le pasamos <>
    return render (request,"hola.html",{'nombre': nombre}) # nos vamos ha hola.html 
def  hola2(request):
    return render(request,"index2.html")
def iniciar(request):
    # return render (request,"login.html")
    return HttpResponseRedirect("/accounts/login/")

def edit_passwd(request):
    return HttpResponseRedirect("/accounts/password/change/")

def base(request):
    # form = PostForm()
    # return render (request,"inicio.html",{'form': form})
    
    if request.user.is_authenticated:
        global user,usuario_registrado
        user = request.user # PARA el template indice.html que permanezca el usuario registrado
        usuario_registrado=user.id # Para view.py y poder hacer filtrado de objetos del propio usuario

    # print(request.user.image)
    return render (request,"index.html")

def observaciones(request):
    # observaciones=Observacion.objects.all()
    # observaciones= observaciones.filter(user_id = usuario_registrado)
    # ----las dos lineas anteriores hacen lo mismo que la siguiente ----
    observaciones=Observacion.objects.all().filter(user= request.user.id)
    return render (request,"observaciones.html",{'name_user': request.user,'observacion':observaciones})


def listado_observaciones(request):
    observaciones=Observacion.objects.all()
    return render(request,"listado_observaciones.html",{'name_user': request.user,'observacion':observaciones})

def observatorios(request):
    observatorios=Observatorio.objects.all().filter(user = request.user.id)
    # observatorios=ObservatorioForm.objects.all().filter(user= usuario_registrado)
    return render (request,"observatorios.html",{'name_user': request.user,'observatorio':observatorios})

def inscripciones(request):
    OBSERVATORIOS=Observatorio.objects.all().filter(user = request.user.id)

    inscripciones = [] 
    for i in OBSERVATORIOS:
        print(i)
        if  Inscripciones.objects.filter(observatorios = i).exists(): # al poner un AutoField puede dar el caso de que tenga dos observaciones con distinto observatorio y me peta
            inscripcion=Inscripciones.objects.get(observatorios = i)
            inscripciones.append(inscripcion)
        else:
            pass
    
    return render(request,"inscripciones.html",{'name_user': request.user,'inscripcion':inscripciones})
   
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def edit_observaciones(request):
    data = request.POST.copy() #cogo todo lo que me viene 
    nom_observacion = data['observacion']
    # print(nom_observacion)
    observacion = Observacion.objects.get(nombre = nom_observacion) #cogo de mi base de datos el que previamente habia seleccionado
    form = ObservacionForm(instance = observacion) #envio a la nueva pag.html el formulario pero rellenado con el plato seleccionado previamente
    return render(request, 'observaciones_edit.html', {'name_user': request.user,"form":form,"nom_observacion":nom_observacion})#tambien envio nombre del plato pk me hace falta

def edit_observatorios(request):
    data = request.POST.copy() #cogo todo lo que me viene 
    request.session['observatorio_viejo']=data['observatorio'] #creo variable de sesion del observatorio seleccionado para editar y asi evito el enviar y recibir campos ocultos (hidde)con datos  para modificar_observatorio
    # print('----HOLA----')
    observatorio= Observatorio.objects.get(nombre = request.session['observatorio_viejo'])
    form = ObservatorioForm(instance = observatorio )
    return render(request, 'observatorios_edit.html',{'name_user':user,'form':form} )

def edit_user(request):
    print ("----hola----")
    # user=Usuario.objects.get(user = usuario_registrado) # PONIENDO USER, me da error y me da todos los id que tiene user en la consola [[ email, emailaddress, first_name, groups, id, image, is_active, is_staff, is_superuser, last_login, last_name, logentry, observacion, observatorio, password, socialaccount, solicitudAstro, tipoUsuario, user_permissions, username ]]
    # user=Usuario.objects.get(id = usuario_registrado)
    # print (user) # user no es iterable
    form =UsuarioChangeForm (instance = request.user)

    return render(request,'usuarios_edit.html',{'name_user':user,'form':form})


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def modificar_observacion(request):
    data = request.POST.copy() #cogo todo lo que me viene
    if request.method == "POST":
        observacion_vieja = Observacion.objects.get(nombre=data['observacion_vieja']) #cojo el plato con el nombre digamos viejo, para que cuando le demos a guardar, GUARDE TODO LO RECIBIDO EN EL PLATO DIGAMOS YA EXISTENTE, pk imagina que cambiamos el nombre, pues para que no te cree uno nuevo,O QUE AL CAMBIAR EL NOMBRE, EN OTRO CAMPO ME HE EQUIVOCADO y repito, entonces debo tener el nombre viejo, pk aun no he modificado nada
        form = ObservacionForm(request.POST, request.FILES, instance=observacion_vieja) #Indicamos que el formulario que ha creado , tenga los datos que hemos rellenado y lo subcriba  en la instancia que le pasamos
        if form.is_valid():#aqui comprovamos que todo  son datos validados correctamente y lo guardamos
            form.save()  
            return redirect(observaciones)
    return render(request,'observaciones_edit.html',{'name_user': request.user,'form':form,'nom_observacion':data['observacion_vieja']})
    
def modificar_observatorio(request):
    if request.session['observatorio_viejo']: #ME AHORRO el hacer observatorio_viejo etc como en observaciones
        # data = request.POST.copy() #cogo todo lo que me viene
        if request.method == "POST":
            observatorio_viejo=Observatorio.objects.get(nombre=request.session['observatorio_viejo'])
            form = ObservatorioForm(request.POST, instance=observatorio_viejo )
            if form.is_valid():
                form.save()
                return redirect(observatorios)
            return render(request,'observatorios_edit.html',{'name_user':request.user,'form':form})

def modificar_user(request):
    if request.method == "POST":
        user_viejo=Usuario.objects.get(id = usuario_registrado)
        form = UsuarioChangeForm(request.POST, request.FILES, instance=user_viejo) #importante request.FILES y poner el enctype <form enctype="multipart/form-data"> para que se modifique la imagen cuando la cambias
        if form.is_valid():
            form.save()
            return redirect(edit_user)
        return render(request,'usuario_edit.html',{'name_user':request.user,'form':form})


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# IMPORTANTE: al presionar el boton de Añadir...  es metodo GET 
# solo cuando guardas,editas,borras envio UN form-->POST(utilizando el post)


def crear_observaciones(request):
    #la primera vez que entra a qui, como no hay digamos nada(POST), 
    # se va al else: , crea el formulario y redireccionamos
    print ('hola1')
    if request.method == 'POST':
        print ('hola3')
        form = ObservacionForm(request.POST)
        if form.is_valid():
            print ('hola4')
            observacion = form.save(commit=False)# lo que hago con estros tres pasos es decirle que me guarde el usuario logeado 
            observacion.user = user
            observacion.save()
            return redirect(observaciones)
        else:
            print ('hola5')
            err=form.errors
            return render(request,'index2.html',{'name_user': request.user,'form':form,'errors':err})
    else:
        form = ObservacionForm()
        print ('hola2')
    return render(request,'index2.html',{'name_user': request.user,'form':form})

def crear_observatorio(request):
    
    if request.method == 'POST':
        form = ObservatorioForm(request.POST)
        if form.is_valid():
            observatorio = form.save(commit=False) # lo que hago con estros tres pasos es decirle que me guarde el usuario logeado
            observatorio.user= user
            observatorio.save()
            return redirect(observatorios)   
    else:   
        form = ObservatorioForm(initial={'user':request.user.id})
        
    return render(request,'observatorios_register.html',{'name_user': request.user,'form':form})

def crear_inscripcion(request):
    # print('------HOLA1-----')
    if request.method == 'POST':
        form = InscripcionesForm(request.POST)
        if form.is_valid():
            inscripcion = form.save()
            return redirect(inscripciones)
    else:
        print("lalalal")
        form = InscripcionesForm()
        # Lo que digo , es que de  todos los observatorios, solo aparezcan los del propio usuario registrado
        form.fields['observatorios'].queryset=Observatorio.objects.filter(user=request.user.id)
    
    return render(request,'inscripciones_register.html',{'name_user': request.user,'form':form})

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def borrar_observaciones(request):
    data = request.POST.copy()
    request.session['observacion_borrar']=data['observacion']
    return render(request,'observaciones_borrado.html',{'name_user': request.user})

def borrar_confirmado_observacion(request):
    if request.session['observacion_borrar']:
        observacion=Observacion.objects.get(nombre=request.session['observacion_borrar'])
        observacion.delete()
        return redirect(observaciones)

def borrar_observatorio(request):
    data = request.POST.copy()
    request.session['observatorio_borrar']= data['observatorio']
    return render(request,'observatorios_borrado.html',{'name_user':request.user})

def borrar_confirmado_observatorio(request):
    if request.session['observatorio_borrar']:
        observatorio=Observatorio.objects.get(nombre=request.session['observatorio_borrar'])
        observatorio.delete()
        return redirect(observatorios)

def borrar_inscripciones(request):
    data = request.POST.copy()
    request.session['inscripcion_borrar']= data['inscripcion']
    return render(request,'inscripciones_borrado.html',{'name_user':request.user})

def borrar_confirmado_inscripcion(request):
    if request.session['inscripcion_borrar']:
        inscripcion = Inscripciones.objects.get(id_inscripcion=request.session['inscripcion_borrar'])
        inscripcion.delete()
        return redirect(inscripciones)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





        



