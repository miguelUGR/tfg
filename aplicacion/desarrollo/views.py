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

def base(request):
  
    if request.user.is_authenticated:
        global user,usuario_registrado
        user = request.user # PARA el template indice.html que permanezca el usuario registrado YA NO ME HACEN FALTA
        usuario_registrado=user.id # Para view.py y poder hacer filtrado de objetos del propio usuario YA NO ME HACEN FALTA
        print(request.user.solicitudAstro)
    

    solicitudAstro,notificaciones,contador=comun(request)
    
    return render (request,"index.html",{'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})
#--------------------  ----------------  ----------------  ----------------  ----------------  ----------------  ----------------  
def comun(request):
    contador=0
    ifSoliAstro = False
    usuario_registrado=request.user
    if usuario_registrado.tipoUsuario == "AT": # Porque este incremento solo lo quiero en los usuarios AT
        usuarios= Usuario.objects.all().filter(solicitudAstro = True) # Cojo los que haya con solicitud 
        if usuarios.count() > 0:
            ifSoliAstro = True
            contador+=1
    
    notificaciones = Notificaciones.objects.all().filter(user=usuario_registrado).order_by('-date')#Filtro  solo las notificaciones del user registrado, para que no aparezcan de otros usuarios y ordenasas de mas nueva a mas vieja
    contador+=notificaciones.count()
    
    # print("CONTADOR=",contador)
    # print("Usuario Registrado tipo:",usuario_registrado.tipoUsuario)
   
    return (ifSoliAstro,notificaciones,contador)  

#----------------  ----------------  ----------------  LISTADO ----------------  ----------------  ----------------  
def observaciones(request):
    solicitudAstro,notificaciones,contador=comun(request)
    # observaciones=Observacion.objects.all()
    # observaciones= observaciones.filter(user_id = usuario_registrado)
    # ----las dos lineas anteriores hacen lo mismo que la siguiente ----
    print("----PEDRO--")
    observaciones=Observacion.objects.all().filter(user=request.user.id)
    for i in observaciones:
        print("OBservacion: ",i.nombre)
    return render (request,"observaciones.html",{'observacion':observaciones,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})

def listado_observaciones(request):
    solicitudAstro,notificaciones,contador=comun(request)
    observaciones=Observacion.objects.all()
    return render(request,"listado_observaciones.html",{'observaciones':observaciones,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})

def listado_observatorios(request):
    solicitudAstro,notificaciones,contador=comun(request)
    observatorios=Observatorio.objects.all().filter(user= request.user.id)
    return render(request,"listado_observatorios.html",{'observatorios':observatorios,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})

def listado_notificaciones(request):
    solicitudAstro,notificaciones,contador=comun(request)
    return render(request,"listado_notificaciones.html",{'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})

def ver_observacion(request):
    usuario_registrado=request.user
    data = request.POST.copy() #cogo todo lo que me viene 
    # print("DATOS=",data)
    nom_observacion = data['observacion']
    request.session['observacion']=nom_observacion # Lo hago para crear_inscripcion_all()
    observacion = Observacion.objects.get(nombre = nom_observacion) #cogo de mi base de datos el que previamente habia seleccionado
    form = ObservacionForm(instance = observacion) #envio a la nueva pag.html el formulario pero rellenado con el plato seleccionado previamente
    # -------- Notificaciones ----------
    notificaciones_a_borrar=Notificaciones.objects.all().filter(user=request.user,observacion=observacion)
    for i in notificaciones_a_borrar:
        i.delete()
    #-----------  Fin  ---------------
   
    #----ESTO es para mostrar los observatorios en el mapa inscritos en la observacion a ver --------- 
    datos = [] 
    observatorios = []
    observatorios_noInscritos = []
    if usuario_registrado.tipoUsuario == "AT":
        # print("Somos SUPER USER")
        inscripciones= Inscripciones.objects.all().filter(observaciones=observacion)
        for i in inscripciones:
            
            dato=[i.observatorios.longitude,i.observatorios.latitude,i.observatorios.radioMovilidad,i.observatorios.nombre]
            # print(dato)
            datos.append(dato)
    #-----------  Fin  ---------------
    
    #---Obstener todos los observatorios no inscritos en la observacion      
    observatorios=Observatorio.objects.all().filter(user= request.user.id) 
    for i in observatorios:
        if Inscripciones.objects.filter(observaciones=observacion,observatorios=i).exists() == False:         
            observatorios_noInscritos.append(i)
    #-----------  Fin  ---------------
    coordenadas=observacion.coordenadas
    # print("Coordenadas:"+coordenadas)
    solicitudAstro,notificaciones,contador=comun(request)#Lo pongo aqui abajo pk no se actualiza
    return render(request, 'observacion_show.html', {"form":form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador,'datos':datos,'observatorios':observatorios_noInscritos,'coordenadas':coordenadas})

def ver_observatorio(request):
    data = request.POST.copy() #cogo todo lo que me viene 
    nom_observatorio = data['observatorio']
    observatorio = Observatorio.objects.get(nombre = nom_observatorio) #cogo de mi base de datos el que previamente habia seleccionado
    form = ObservatorioForm(instance = observatorio) #envio a la nueva pag.html el formulario pero rellenado con el plato seleccionado previamente
    
    longuitud= observatorio.longitude
    latitud= observatorio.latitude 
    nombre=observatorio.nombre
    radio=observatorio.radioMovilidad
    print("logintud=",longuitud)
    print("latitud=",latitud)
    solicitudAstro,notificaciones,contador=comun(request)#Lo pongo aqui abajo pk no se actualiza
    return render(request, 'observatorio_show.html', {"form":form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador,'latitud':latitud,'longuitud':longuitud,'radio':radio,'nombre':nombre})


def ver_observatorio_all(request):
    observatorios=Observatorio.objects.all().filter(user= request.user.id)
    print("VAMOS A IMPRIMIR")
    datos = [] 
    for i in observatorios:
        
        dato=[i.longitude,i.latitude,i.radioMovilidad,i.nombre]
        # dato=[{"longitud":i.longitude,"latitude":i.latitude,"radio":i.radioMovilidad}]
    
        datos.append(dato)
    
    print(len(datos)) #Para saber cuantos datos tiene LA LISTA
    solicitudAstro,notificaciones,contador=comun(request)#Lo pongo aqui abajo pk no se actualiza
    return render(request, 'observatorio_show_all.html', {'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador,'datos':datos})


def observatorios(request):
    solicitudAstro,notificaciones,contador=comun(request)
    observatorios=Observatorio.objects.all().filter(user = request.user.id)
    # observatorios=ObservatorioForm.objects.all().filter(user= usuario_registrado)
    return render (request,"observatorios.html",{'observatorio':observatorios,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})

def inscripciones(request):
    solicitudAstro,notificaciones,contador=comun(request)
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
    return render(request,"inscripciones.html",{'inscripciones':inscripciones_totales,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})

def solicitudAstro(request):
    solicitudAstro,notificaciones,contador=comun(request)
    usuarios= Usuario.objects.all().filter(solicitudAstro = True)
    return render(request,"notificacion_solicitud.html",{'usuario':usuarios,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})


#----------------  ----------------  ----------------  EDICION ----------------  ----------------  ----------------  
def edit_observaciones(request):
    solicitudAstro,notificaciones,contador=comun(request)
    data = request.POST.copy() #cogo todo lo que me viene 
    nom_observacion = data['observacion']
    # print(nom_observacion)
    observacion = Observacion.objects.get(nombre = nom_observacion) #cogo de mi base de datos el que previamente habia seleccionado
    form = ObservacionForm(instance = observacion) #envio a la nueva pag.html el formulario pero rellenado con el plato seleccionado previamente
    coordenadas=observacion.coordenadas
    return render(request, 'observaciones_edit.html', {"form":form,"nom_observacion":nom_observacion,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador,'coordenadas':coordenadas})#tambien envio nombre del plato pk me hace falta

def edit_observatorios(request):
    solicitudAstro,notificaciones,contador=comun(request)
    data = request.POST.copy() #cogo todo lo que me viene 
    request.session['observatorio_viejo']=data['observatorio'] #creo variable de sesion del observatorio seleccionado para editar y asi evito el enviar y recibir campos ocultos (hidde)con datos  para modificar_observatorio
    # print('----HOLA----')
    observatorio= Observatorio.objects.get(nombre = request.session['observatorio_viejo'])
    form = ObservatorioForm(instance = observatorio )
    longuitud= observatorio.longitude
    latitud= observatorio.latitude 
    nombre=observatorio.nombre
    radio=observatorio.radioMovilidad
    
    return render(request, 'observatorios_edit.html', {"form":form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador,'latitud':latitud,'longuitud':longuitud,'radio':radio,'nombre':nombre})


def edit_user(request):
    solicitudAstro,notificaciones,contador=comun(request)
    # user=Usuario.objects.get(user = usuario_registrado) # PONIENDO USER, me da error y me da todos los id que tiene user en la consola [[ email, emailaddress, first_name, groups, id, image, is_active, is_staff, is_superuser, last_login, last_name, logentry, observacion, observatorio, password, socialaccount, solicitudAstro, tipoUsuario, user_permissions, username ]]
    # user=Usuario.objects.get(id = usuario_registrado)
    # print (user) # user no es iterable
    form =UsuarioChangeForm (instance = request.user)
    return render(request,'usuarios_edit.html',{'name_user':user,'form':form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})

def aceptar_notifi_Astro(request):
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
    solicitudAstro,notificaciones,contador=comun(request)
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
                       if i.user not in user:  # elimino repetidos, para no generar notificaciones repetidas
                           user.append(i.user)
                for i in user:
                   # Antes de meter notificaciones, tengo que eliminar la o las anteriores. (no deberia de haber mas de una, pk pretendo eliminarlas)
                    if Notificaciones.objects.filter(user=i,observacion=observacion_vieja).exists(): #esto petaria si hay mas de una, pero no debe de haber (PUES NO PETA)
                        print("--PROCEDEMOS A ELIMINAR--")
                        notificacion_eliminar=Notificaciones.objects.filter(user=i,observacion=observacion_vieja)
                        notificacion_eliminar.delete() # Hemos podido elimiar mas de una a la vez

                    new_notificacion=Notificaciones(user=i,descripcion="Modificacion de Observacion",observacion=observacion_vieja)
                    new_notificacion.save()

                
            return redirect(observaciones)

    return render(request,'observaciones_edit.html',{'form':form,'nom_observacion':data['observacion_vieja'],'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})
    
def modificar_observatorio(request):
    solicitudAstro,notificaciones,contador=comun(request)
    if request.session['observatorio_viejo']: #ME AHORRO el hacer observatorio_viejo etc como en observaciones
        # data = request.POST.copy() #cogo todo lo que me viene
        if request.method == "POST":
            observatorio_viejo=Observatorio.objects.get(nombre=request.session['observatorio_viejo'])
            form = ObservatorioForm(request.POST, instance=observatorio_viejo )
            if form.is_valid():
                form.save()
                return redirect(observatorios)
            return render(request,'observatorios_edit.html',{'name_user':request.user,'form':form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})

def modificar_user(request):
    solicitudAstro,notificaciones,contador=comun(request)
    if request.method == "POST":
        user_viejo=Usuario.objects.get(id = usuario_registrado)
        form = UsuarioChangeForm(request.POST, request.FILES, instance=user_viejo) #importante request.FILES y poner el enctype <form enctype="multipart/form-data"> para que se modifique la imagen cuando la cambias
        if form.is_valid():
            form.save()
            return redirect(edit_user)
        return render(request,'usuario_edit.html',{'name_user':request.user,'form':form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})

#----------------  ----------------  ----------------  CREACION ----------------  ----------------  ----------------    
# IMPORTANTE: al presionar el boton de Añadir...  es metodo GET 
# solo cuando guardas,editas,borras envio UN form-->POST(utilizando el post)


def crear_observaciones(request):
    solicitudAstro,notificaciones,contador=comun(request)
    #la primera vez que entra a qui, como no hay digamos nada(POST), 
    # se va al else: , crea el formulario y redireccionamos
    
    if request.method == 'POST':
        form = ObservacionForm(request.POST)
        if form.is_valid():
            observacion = form.save(commit=False)# lo que hago con estros tres pasos es decirle que me guarde el usuario logeado 
            observacion.user = request.user
            observacion.save()
            return redirect(observaciones)
        else:
            err=form.errors
            return render(request,'observaciones_register.html',{'form':form,'errors':err,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})
    else:
        form = ObservacionForm()
        
    return render(request,'observaciones_register.html',{'form':form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})

def crear_observatorio(request):
    solicitudAstro,notificaciones,contador=comun(request)
    if request.method == 'POST':
        form = ObservatorioForm(request.POST)
        if form.is_valid():
            observatorio = form.save(commit=False) # lo que hago con estros tres pasos es decirle que me guarde el usuario logeado
            observatorio.user= request.user
            observatorio.save()
            return redirect(observatorios)   
    else:   
        form = ObservatorioForm(initial={'user':request.user.id})
        
    return render(request,'observatorios_register.html',{'form':form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})

def crear_inscripcion(request):
    solicitudAstro,notificaciones,contador=comun(request)
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
    
    return render(request,'inscripciones_register.html',{'form':form,'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})


def crear_inscripcion_all(request):
    data = request.POST.copy()
    # request.session['observacion']   PROCEDE de ver_observacion()
    observacion=Observacion.objects.get(nombre=request.session['observacion'])
    for i in data:
        #Lo hago pk el form me envia un campo csrf_token entonces me petaria
        if Observatorio.objects.filter(nombre=i).exists():
            observatorio=Observatorio.objects.get(nombre=i)
            print("------Procedemos a generar inscripcion-----")
            new_inscripcion=Inscripciones(observaciones=observacion,observatorios=observatorio)               
            new_inscripcion.save()
        else:
            print("No entra")
            
    return redirect(listado_observaciones)

#----------------  ----------------  ----------------  BORRADO ----------------  ----------------  ----------------  
def borrar_observaciones(request):
    solicitudAstro,notificaciones,contador=comun(request)
    data = request.POST.copy()
    request.session['observacion_borrar']=data['observacion']
    return render(request,'observaciones_borrado.html',{'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})

def borrar_confirmado_observacion(request):
    if request.session['observacion_borrar']:
        observacion=Observacion.objects.get(nombre=request.session['observacion_borrar'])
        observacion.delete()
        return redirect(observaciones)

def borrar_observatorio(request):
    solicitudAstro,notificaciones,contador=comun(request)
    data = request.POST.copy()
    request.session['observatorio_borrar']= data['observatorio']
    return render(request,'observatorios_borrado.html',{'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})

def borrar_confirmado_observatorio(request):
    if request.session['observatorio_borrar']:
        observatorio=Observatorio.objects.get(nombre=request.session['observatorio_borrar'])
        observatorio.delete()
        return redirect(observatorios)

def borrar_inscripciones(request):
    solicitudAstro,notificaciones,contador=comun(request)
    data = request.POST.copy()
    request.session['inscripcion_borrar']= data['inscripcion']
    return render(request,'inscripciones_borrado.html',{'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})

def borrar_confirmado_inscripcion(request):
    if request.session['inscripcion_borrar']:
        inscripcion = Inscripciones.objects.get(id_inscripcion=request.session['inscripcion_borrar'])
        inscripcion.delete()
        return redirect(inscripciones)

def denegar_notifi_Astro(request):
    solicitudAstro,notificaciones,contador=comun(request)
    data = request.POST.copy()
    request.session['notificacion_borrar']=data['notificacion']
    return render(request,'notificaciones_solicitud_borrado.html',{'solicitudAstro':solicitudAstro,'notificacion':notificaciones,'contador':contador})

def borrar_confirmado_notifi_Astro(request):
    if request.session['notificacion_borrar']: 
        usuario= Usuario.objects.get(id = request.session['notificacion_borrar'])
        usuario.solicitudAstro= False
        usuario.save()
        return redirect(solicitudAstro)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





        



