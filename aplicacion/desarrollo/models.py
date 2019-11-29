from django.db import models

# Create your models here.
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
# para crear el modelo plato ponemos en el terminal: 
# - python manage.py makemigrations restaurantes
# para migrarlo y poder verlo desde el navegador (http://localhost:8080/admin/) ponemos en el terminal primero:
# - python manage.py migrate

class Usuario(models.Model):
    ASTRONOMO = 'AS'
    AFICIONADO = 'AF'

    TIPO_USUARIO = (
    (ASTRONOMO , "Astronomo"),
    (AFICIONADO , "Aficionado") )

    # blank=False es para que por narices metamos un numero, si lo ponemos a True, indicamos que puede meterse campo vacio
    nombre = models.CharField(max_length=50,blank = False)
    apellido = models.CharField(max_length=50,blank = False)
    correo = models.EmailField(verbose_name='correo electronico',max_length=100, unique=True)
    tipoUsuario = models.CharField(max_length = 9, choices = TIPO_USUARIO,default=AFICIONADO)

    def __str__(self):
        return self.nombre #Esto es para que apareciese en el navegador (lugar Admin de django), el nombre de los platos , en vez de objeto1,2...s

class Observatorio(models.Model):
    nombre = models.CharField(max_length=150,blank = False,unique=True)
    camara = models.CharField(max_length=50,blank = False)
    apertura = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],blank= False) # blank=False es para que por narices metamos un numero, si lo ponemos a True, indicamos que puede meterse campo vacio
    filtros = models.CharField(max_length=50,blank = False)
    latitude = models.DecimalField(max_digits=6, decimal_places=3)
    longitude = models.DecimalField(max_digits=6, decimal_places=3)
    user = models.ForeignKey(Usuario,on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

