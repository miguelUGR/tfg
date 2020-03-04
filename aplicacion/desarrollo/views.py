from django.shortcuts import render
from django import forms 
from django.http import HttpResponseRedirect, HttpResponse ,JsonResponse
from .models import Observacion, Observatorio, Inscripciones, Usuario, Notificaciones
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

class Counter:
    count = 0

    def increment(self):
        self.count += 1
        return ''

    def decrement(self):
        self.count -= 1
        return ''

    def double(self):
        self.count *= 2
        return ''

def base(request):
  
    if request.user.is_authenticated:
        global user,usuario_registrado
        user = request.user # PARA el template indice.html que permanezca el usuario registrado YA NO ME HACEN FALTA
        usuario_registrado=user.id # Para view.py y poder hacer filtrado de objetos del propio usuario YA NO ME HACEN FALTA
        print(request.user.solicitudAstro)
    
    
    solicitudAstro,notificaciones=comun()
    
    return render (request,"index.html",{'solicitudAstro':solicitudAstro,'notificacion':notificaciones})
#--------------------  ----------------  ----------------  ----------------  ----------------  ----------------  ----------------  
def comun():
    usuarios= Usuario.objects.all().filter(tipoUsuario = 'AF')
    ifSoliAstro = False
    for i in usuarios:
        if i.solicitudAstro == True:
                ifSoliAstro = True
                break
    notificaciones = Notificaciones.objects.all()
    
   
    return (ifSoliAstro,notificaciones)  

#----------------  ----------------  ----------------  LISTADO ----------------  ----------------  ----------------  
def observaciones(request):
    solicitudAstro,notificaciones=comun()
    # observaciones=Observacion.objects.all()
    # observaciones= observaciones.filter(user_id = usuario_registrado)
    # ----las dos lineas anteriores hacen lo mismo que la siguiente ----
    observaciones=Observacion.objects.all().filter(user= request.user.id)
    return render (request,"observaciones.html",{'observacion':observaciones,'solicitudAstro':solicitudAstro,'notificacion':notificaciones})

def listado_observaciones(request):
    solicitudAstro,notificaciones=comun()
    observaciones=Observacion.objects.all()
    return render(request,"listado_observaciones.html",{'observaciones':observaciones,'solicitudAstro':solicitudAstro,'notificacion':notificacioness})

def ver_observacion(request):
    solicitudAstro,notificaciones=comun()
    data = request.POST.copy() #cogo todo lo que me viene 
    nom_observacion = data['observacion']
    observacion = Observacion.objects.get(nombre = nom_observacion) #cogo de mi base de datos el que previamente habia seleccionado
    form = ObservacionForm(instance = observacion) #envio a la nueva pag.html el formulario pero rellenado con el plato seleccionado previamente
    notificaciones_a_borrar=Notificaciones.objects.all().filter(user=request.user,observacion=observacion)
    for i in notificaciones_a_borrar:
        i.delete()
        

    return render(request, 'observacion_show.html', {"form":form,"nom_observacion":nom_observacion,'solicitudAstro':solicitudAstro,'notificacion':notificaciones})#tambien envio nombre del plato pk me hace falta

def observatorios(request):
    solicitudAstro,notificaciones=comun()
    observatorios=Observatorio.objects.all().filter(user = request.user.id)
    # observatorios=ObservatorioForm.objects.all().filter(user= usuario_registrado)
    return render (request,"observatorios.html",{'observatorio':observatorios,'solicitudAstro':solicitudAstro,'notificacion':notificaciones})

def inscripciones(request):
    solicitudAstro,notificaciones=comun()
    OBSERVATORIOS=Observatorio.objects.all().filter(user = request.user.id)
    inscripciones_totales = [] 
    inscripcion = []            #puede ser que en el if me devuelva mas de una, pk un observatorio este inscrito en mas de una observacion
    for i in OBSERVATORIOS:
        # print("Observatorios = ",i)
        if  Inscripciones.objects.all().filter(observatorios = i).exists(): # al poner un AutoField puede dar el caso de que tenga dos observaciones con distinto observatorio y me peta
            inscripcion=Inscripciones.objects.all().filter(observatorios = i) #Ojo si ponemos objects.get() si devuelve dos, da problemas
            for i in inscripcion: # IMPORTANTISIMO hacer un for, pk si inscripcion tiene mas de un elemento, es un querySet y no se representa bien luego en el html, e individualmente [se me ponian en bloque al devover mas de uno]
                # print("Inscripcion = ",i) 
                inscripciones_totales.append(i) 
        else:
            pass
    return render(request,"inscripciones.html",{'inscripciones':inscripciones_totales,'solicitudAstro':solicitudAstro,'notificacion':notificaciones})
   
def solicitudAstro(request):
    solicitudAstro,notificaciones=comun()
    usuarios= Usuario.objects.all().filter(solicitudAstro = True)
    return render(request,"notificacion_solicitud.html",{'usuario':usuarios,'solicitudAstro':solicitudAstro,'notificacion':notificaciones})


#----------------  ----------------  ----------------  EDICION ----------------  ----------------  ----------------  
def edit_observaciones(request):
    solicitudAstro,notificaciones=comun()
    data = request.POST.copy() #cogo todo lo que me viene 
    nom_observacion = data['observacion']
    # print(nom_observacion)
    observacion = Observacion.objects.get(nombre = nom_observacion) #cogo de mi base de datos el que previamente habia seleccionado
    form = ObservacionForm(instance = observacion) #envio a la nueva pag.html el formulario pero rellenado con el plato seleccionado previamente
    return render(request, 'observaciones_edit.html', {"form":form,"nom_observacion":nom_observacion,'solicitudAstro':solicitudAstro,'notificacion':notificaciones})#tambien envio nombre del plato pk me hace falta

def edit_observatorios(request):
    solicitudAstro,notificaciones=comun()
    data = request.POST.copy() #cogo todo lo que me viene 
    request.session['observatorio_viejo']=data['observatorio'] #creo variable de sesion del observatorio seleccionado para editar y asi evito el enviar y recibir campos ocultos (hidde)con datos  para modificar_observatorio
    # print('----HOLA----')
    observatorio= Observatorio.objects.get(nombre = request.session['observatorio_viejo'])
    form = ObservatorioForm(instance = observatorio )
    return render(request, 'observatorios_edit.html',{'name_user':user,'form':form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones} )

def edit_user(request):
    solicitudAstro,notificaciones=comun()
    # user=Usuario.objects.get(user = usuario_registrado) # PONIENDO USER, me da error y me da todos los id que tiene user en la consola [[ email, emailaddress, first_name, groups, id, image, is_active, is_staff, is_superuser, last_login, last_name, logentry, observacion, observatorio, password, socialaccount, solicitudAstro, tipoUsuario, user_permissions, username ]]
    # user=Usuario.objects.get(id = usuario_registrado)
    # print (user) # user no es iterable
    form =UsuarioChangeForm (instance = request.user)
    return render(request,'usuarios_edit.html',{'name_user':user,'form':form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones})

def aceptar_notifi_Astro(request):
    solicitudAstro,notificaciones=comun()
    data = request.POST.copy()
    usuario= Usuario.objects.get(id = data['notificacion'])
    usuario.tipoUsuario='AT'
    usuario.solicitudAstro= False
    usuario.save()

    #invalid literal for int() with base 10: 'leonora'  
    # notificacion=Notificaciones.objects.get(user= str(data['notificacion'])) #field. Choices are: date, id, tipoNotificacion, user, user_id
    # COMO ME DA ERROR en la linea anterior DE QUE LOS CAMPOS NO SON IGUALES, realizo lo siguiente
    # dato=usuario.id
    # notificacion=Notificaciones.objects.get(user_id= dato)
    # notificacion.delete()
    # del request.session['notificaciones'] # lo hago en base()
    return redirect(solicitudAstro)


#----------------  ----------------  ----------------  MODIFICACION ----------------  ----------------  ----------------  


def modificar_observacion(request):
    solicitudAstro,notificaciones=comun()
    data = request.POST.copy() #cogo todo lo que me viene
    if request.method == "POST":
        observacion_vieja = Observacion.objects.get(nombre=data['observacion_vieja']) #cojo el plato con el nombre digamos viejo, para que cuando le demos a guardar, GUARDE TODO LO RECIBIDO EN EL PLATO DIGAMOS YA EXISTENTE, pk imagina que cambiamos el nombre, pues para que no te cree uno nuevo,O QUE AL CAMBIAR EL NOMBRE, EN OTRO CAMPO ME HE EQUIVOCADO y repito, entonces debo tener el nombre viejo, pk aun no he modificado nada
        form = ObservacionForm(request.POST, request.FILES, instance=observacion_vieja) #Indicamos que el formulario que ha creado , tenga los datos que hemos rellenado y lo subcriba  en la instancia que le pasamos
        if form.is_valid():#aqui comprovamos que todo  son datos validados correctamente y lo guardamos
            form.save()  
#----------APARTADO--NOTIFICACIONES-----------
            #--1)Buscar en inscripciones, la observacion_vieja cuantas veces aparece y si esta coger los usuarios 
            inscripciones = [] 
            observatorio = []
            user = []
            if  Inscripciones.objects.all().filter(observaciones_id = observacion_vieja).exists(): # al poner un AutoField puede dar el caso de que tenga dos observaciones con distinto observatorio y me peta
                print("--ESTAMOS En NOTIFICACIONES--")
                inscripciones=Inscripciones.objects.all().filter(observaciones_id = observacion_vieja)
                # print(inscripciones) #Es un queryset, debemos hacer un bucle
                for i in inscripciones: # Obtengo todos los observatorios 
                    observatorio.append(i.observatorios)
                  
                for i in observatorio:#Cojo todos los usuarios eliminando repetido(puede dar el caso, usuario con mas de un observatorio en la misma observacion)
                    # print("usuario = ",i.user)
                       if i.user not in user:  # elimino repetidos, para no generar notificaciones repetidas
                           user.append(i.user)
                for i in user:
                    # print("UsuariosNo = ", i) 
                    new_notificacion=Notificaciones(user=i,descripcion="Modificacion de Observacion",observacion=observacion_vieja)
                    new_notificacion.save()

                
            return redirect(observaciones)

    return render(request,'observaciones_edit.html',{'form':form,'nom_observacion':data['observacion_vieja'],'solicitudAstro':solicitudAstro,'notificacion':notificaciones})
    
def modificar_observatorio(request):
    solicitudAstro,notificaciones=comun()
    if request.session['observatorio_viejo']: #ME AHORRO el hacer observatorio_viejo etc como en observaciones
        # data = request.POST.copy() #cogo todo lo que me viene
        if request.method == "POST":
            observatorio_viejo=Observatorio.objects.get(nombre=request.session['observatorio_viejo'])
            form = ObservatorioForm(request.POST, instance=observatorio_viejo )
            if form.is_valid():
                form.save()
                return redirect(observatorios)
            return render(request,'observatorios_edit.html',{'name_user':request.user,'form':form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones})

def modificar_user(request):
    solicitudAstro,notificaciones=comun()
    if request.method == "POST":
        user_viejo=Usuario.objects.get(id = usuario_registrado)
        form = UsuarioChangeForm(request.POST, request.FILES, instance=user_viejo) #importante request.FILES y poner el enctype <form enctype="multipart/form-data"> para que se modifique la imagen cuando la cambias
        if form.is_valid():
            form.save()
            return redirect(edit_user)
        return render(request,'usuario_edit.html',{'name_user':request.user,'form':form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones})

#----------------  ----------------  ----------------  CREACION ----------------  ----------------  ----------------    
# IMPORTANTE: al presionar el boton de Añadir...  es metodo GET 
# solo cuando guardas,editas,borras envio UN form-->POST(utilizando el post)


def crear_observaciones(request):
    solicitudAstro,notificaciones=comun()
    #la primera vez que entra a qui, como no hay digamos nada(POST), 
    # se va al else: , crea el formulario y redireccionamos
    
    if request.method == 'POST':
        form = ObservacionForm(request.POST)
        if form.is_valid():
            observacion = form.save(commit=False)# lo que hago con estros tres pasos es decirle que me guarde el usuario logeado 
            observacion.user = user
            observacion.save()
            return redirect(observaciones)
        else:
            err=form.errors
            return render(request,'observaciones_register.html',{'form':form,'errors':err,'solicitudAstro':solicitudAstro,'notificacion':notificaciones})
    else:
        form = ObservacionForm()
        
    return render(request,'observaciones_register.html',{'form':form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones})

def crear_observatorio(request):
    solicitudAstro,notificaciones=comun()
    if request.method == 'POST':
        form = ObservatorioForm(request.POST)
        if form.is_valid():
            observatorio = form.save(commit=False) # lo que hago con estros tres pasos es decirle que me guarde el usuario logeado
            observatorio.user= user
            observatorio.save()
            return redirect(observatorios)   
    else:   
        form = ObservatorioForm(initial={'user':request.user.id})
        
    return render(request,'observatorios_register.html',{'form':form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones})

def crear_inscripcion(request):
    solicitudAstro,notificaciones=comun()
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
    
    return render(request,'inscripciones_register.html',{'form':form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones})

#----------------  ----------------  ----------------  BORRADO ----------------  ----------------  ----------------  
def borrar_observaciones(request):
    solicitudAstro,notificaciones=comun()
    data = request.POST.copy()
    request.session['observacion_borrar']=data['observacion']
    return render(request,'observaciones_borrado.html')

def borrar_confirmado_observacion(request):
    solicitudAstro,notificaciones=comun()
    if request.session['observacion_borrar']:
        observacion=Observacion.objects.get(nombre=request.session['observacion_borrar'])
        observacion.delete()
        return redirect(observaciones)

def borrar_observatorio(request):
    solicitudAstro,notificaciones=comun()
    data = request.POST.copy()
    request.session['observatorio_borrar']= data['observatorio']
    return render(request,'observatorios_borrado.html',{'solicitudAstro':solicitudAstro,'notificacion':notificaciones})

def borrar_confirmado_observatorio(request):
    if request.session['observatorio_borrar']:
        observatorio=Observatorio.objects.get(nombre=request.session['observatorio_borrar'])
        observatorio.delete()
        return redirect(observatorios)

def borrar_inscripciones(request):
    solicitudAstro,notificaciones=comun()
    data = request.POST.copy()
    request.session['inscripcion_borrar']= data['inscripcion']
    return render(request,'inscripciones_borrado.html',{'solicitudAstro':solicitudAstro,'notificacion':notificaciones})

def borrar_confirmado_inscripcion(request):
    if request.session['inscripcion_borrar']:
        inscripcion = Inscripciones.objects.get(id_inscripcion=request.session['inscripcion_borrar'])
        inscripcion.delete()
        return redirect(inscripciones)

def denegar_notifi_Astro(request):
    solicitudAstro,notificaciones=comun()
    data = request.POST.copy()
    request.session['notificacion_borrar']=data['notificacion']
    return render(request,'notificaciones_solicitud_borrado.html',{'solicitudAstro':solicitudAstro,'notificacion':notificaciones})

def borrar_confirmado_notifi_Astro(request):
    if request.session['notificacion_borrar']: 
        usuario= Usuario.objects.get(id = request.session['notificacion_borrar'])
        usuario.solicitudAstro= False
        usuario.save()
        return redirect(solicitudAstro)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





        



