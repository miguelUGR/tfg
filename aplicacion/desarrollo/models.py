from django.db import models
from django.db.models import Model 
# Create your models here.
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser #Para heredar del usuario ya creado de django
from django.conf import settings # hacer referencia a nuestro modelo podemos apoyarnos de la constante AUTH_USER_MODEL.
# para crear el modelo plato ponemos en el terminal: 
# - python manage.py makemigrations restaurantes
# para migrarlo y poder verlo desde el navegador (http://localhost:8080/admin/) ponemos en el terminal primero:
# - python manage.py migrate

class Usuario(AbstractUser):
    # blank=False es para que por narices metamos un numero, si lo ponemos a True, indicamos que puede meterse campo vacio
    ATRO = 'AT'
    AFICIONADO = 'AF'
    
    TIPO_USUARIO = (
    (ATRO , "Atro"),
    (AFICIONADO , "Aficionado"))
    tipoUsuario= models.CharField(max_length = 9, choices = TIPO_USUARIO, default=AFICIONADO )
    def __str__(self):
         return self.username #Esto es para que apareciese en el navegador (lugar Admin de django), el nombre de los platos , en vez de objeto1,2...s

class User_Astronomo(models.Model):
    user = models.ForeignKey(
                settings.AUTH_USER_MODEL,
                null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
         return self.user.username

class User_Aficionado(models.Model):
    user = models.ForeignKey(
                settings.AUTH_USER_MODEL,
                null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
         return self.user.username

# class Coordenadas(models.Model):
#         latitude = models.DecimalField(max_digits=100, decimal_places=6)
#         longitude = models.DecimalField(max_digits=100, decimal_places=6)
#         def getPrintName(self):
#             return self.latitude + ", " + self.longitude

class Observatorio(models.Model):
    nombre = models.CharField(max_length=150,blank = False,unique=True)
    camara = models.CharField(max_length=50,blank = False)# blank=False es para que por narices metamos un numero, si lo ponemos a True, indicamos que puede meterse campo vacio
    apertura = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],blank= False) 
    filtros = models.CharField(max_length=50,blank = False)
    latitude = models.DecimalField(max_digits=100, decimal_places=6)
    longitude = models.DecimalField(max_digits=100, decimal_places=6)
    distanciaFocal = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],blank= False) 
    # coordenadas = models.OneToOneField(Coordenadas,on_delete=models.CASCADE)
    user = models.ForeignKey(User_Aficionado,on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

class Observacion(models.Model):
    nombre = models.CharField(max_length=150,blank = False,unique=True)
    fecha_observacion= models.DateField() 
    # coordenadas = models.OneToOneField(Coordenadas,on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=100, decimal_places=6)
    longitude = models.DecimalField(max_digits=100, decimal_places=6)
    duracion_ocultacion = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)],blank= False) 
    hora_inicio = models.DateTimeField(null=True, blank=True) #indico que puedes meter nulo 
    hora_final = models.DateTimeField(null=True, blank=True)
    descripcion = models.TextField()
    image = models.ImageField(upload_to='covers/%Y/%m/%D/', height_field=None, width_field=None, max_length=100,blank=True,null=True)# me pide que haga pip install Pillow
    user = models.ForeignKey(User_Astronomo,on_delete=models.PROTECT)
    def __str__(self):
        return self.nombre

class Inscripciones(models.Model):
    nombre = models.CharField(max_length=100,blank = False,unique=True)
    Observacion = models.ManyToManyField(Observacion)
    observatorios = models.ManyToManyField(Observatorio)

    
    def __str__(self):
        return self.nombre





