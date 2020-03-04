from django.db import models
from django.db.models import Model 
from django.core.exceptions import ValidationError
# Create your models here.
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser #Para heredar del usuario ya creado de django
from django.conf import settings # hacer referencia a nuestro modelo podemos apoyarnos de la constante AUTH_USER_MODEL.
from django.utils import timezone
# para crear el modelo plato ponemos en el terminal: 
# - python manage.py makemigrations restaurantes
# para migrarlo y poder verlo desde el navegador (http://localhost:8080/admin/) ponemos en el terminal primero:
# - python manage.py migrate

# CASCADE: Cuando se elimina el objeto referenciado, también elimine los objetos que tienen referencias a él 
# (cuando elimina una publicación de blog, por ejemplo, es posible que también desee eliminar los comentarios). Equivalente SQL: CASCADE.
# PROTECT: Prohibir la eliminación del objeto referenciado. Para eliminarlo, deberá eliminar todos los objetos 
# que lo referencian manualmente. Equivalente SQL: RESTRICT.



class Usuario(AbstractUser):
    # blank=False es para que por narices metamos un numero, si lo ponemos a True, indicamos que puede meterse campo vacio
    ATRO = 'AT'
    AFICIONADO = 'AF'
    
    TIPO_USUARIO = (
    (ATRO , "Atro"),
    (AFICIONADO , "Aficionado"))
    tipoUsuario= models.CharField(max_length = 9, choices = TIPO_USUARIO, default=AFICIONADO )
    image = models.ImageField(upload_to='usuarios/',default='usuarios/default_image.png', height_field=None, width_field=None, max_length=100)# me pide que haga pip install Pillow
    solicitudAstro = models.BooleanField(verbose_name=('Solicitud Usuario Astrofisico '),default=False)
    def __str__(self):
         return self.username #Esto es para que apareciese en el navegador (lugar Admin de django), el nombre de los platos , en vez de objeto1,2...s


class Observatorio(models.Model):
    nombre = models.CharField(max_length=150,blank = False,unique=True)
    camara = models.CharField(max_length=50,blank = False)# blank=False es para que por narices metamos un numero, si lo ponemos a True, indicamos que puede meterse campo vacio
    apertura = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],blank= False) 
    filtros = models.CharField(max_length=50,blank = False)
    latitude = models.DecimalField(max_digits=100, decimal_places=6)
    longitude = models.DecimalField(max_digits=100, decimal_places=6)
    distanciaFocal = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],blank= False) 
    
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Observacion(models.Model):
    nombre = models.CharField(max_length=150,blank = False,unique=True)
    fecha_observacion= models.DateField() 
    latitude = models.DecimalField(max_digits=100, decimal_places=6)
    longitude = models.DecimalField(max_digits=100, decimal_places=6)
    duracion_ocultacion = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)],blank= False) 
    hora_inicio = models.DateTimeField(null=True, blank=True) #indico que puedes meter nulo 
    hora_final = models.DateTimeField(null=True, blank=True)
    descripcion = models.TextField()
    image = models.ImageField(upload_to='observacion/', height_field=None, width_field=None, max_length=100,blank=True,null=True)
    user = models.ForeignKey(Usuario,limit_choices_to={'tipoUsuario':'AT'},on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name_plural='Observaciones'

class Inscripciones(models.Model):
    id_inscripcion = models.AutoField(primary_key=True)
    # nombre = models.CharField(max_length=100,blank = False,unique=True,)
    observaciones = models.ForeignKey(Observacion,on_delete=models.CASCADE)#ForeignKey
    observatorios = models.ForeignKey(Observatorio,on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to='inscripciones/', height_field=None, width_field=None, max_length=100,blank= True,null=True)
    
    OPCION_INSCRIPCION = (
    ('POS' , "Positivo"),
    ('NEU' , "Neutro"),
    ('NEGA' , "Negativo"))
    opcionInscripcion= models.CharField(max_length = 9, choices = OPCION_INSCRIPCION, default='NEU' )
    
    class Meta:#para crear clave primaria de dos campos
        unique_together  = ["observaciones", "observatorios"]
        
    def clean(self):
        direct = Inscripciones.objects.filter(observaciones = self.observaciones, observatorios = self.observatorios)
        reverse = Inscripciones.objects.filter(observatorios = self.observatorios, observaciones = self.observaciones) 

        if direct.exists() or reverse.exists():
            raise ValidationError({'observaciones':'observatorios'})
    
    def __str__(self):
        return str(self.id_inscripcion)+"_["+str(self.observaciones)+"]_["+str(self.observatorios)+"]"
        # return str(self.id_inscripcion)
    class Meta:
        verbose_name_plural='Inscripciones'

class Notificaciones(models.Model):
    id_notificacion = models.AutoField(primary_key=True)
    user = models.ForeignKey(Usuario,limit_choices_to={'tipoUsuario':'AF'},on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField(blank=True) #indicar que observacion se ha modificado con un texto 
    observacion = models.ForeignKey(Observacion,on_delete=models.CASCADE,null=True, blank=True)
    
    def __str__(self):
        cadena = str(self.id_notificacion)+"_"+str(self.user)
        return cadena
    class Meta:
        verbose_name_plural='Notificaciones'





    


    
    





