from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Pais(models.Model):
    nombre = models.CharField(max_length=75)

    def __str__(self):
        return self.nombre
class Provincia(models.Model):
    nombre = models.CharField(max_length=75)
    pais =   models.ForeignKey(Pais, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Departamento(models.Model):
    nombre = models.CharField(max_length=75)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Distrito(models.Model):
    nombre = models.CharField(max_length=75)
    coordenadas = models.CharField(max_length=75)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Barrio(models.Model):
    nombre = models.CharField(max_length=75)
    coordenadas = models.CharField(max_length=75)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Calle(models.Model):
    nombre = models.CharField(max_length=75)

    def __str__(self):
        return self.nombre

class Casa(models.Model):
    nombre = models.CharField(max_length=75)
    calle = models.ForeignKey(Calle, on_delete=models.CASCADE)
    numero = models.CharField(max_length=10)
    barrio = models.ForeignKey(Barrio, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Rol(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
    
class Padecimientos(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Amenaza(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.nombre


class Amenaza_Casa(models.Model):
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE)
    amenaza = models.ForeignKey(Amenaza, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField()

class Persona(models.Model):
    nombre = models.CharField(max_length=75)
    apellido = models.CharField(max_length=75)
    foto_perfil = models.ImageField(upload_to='profile_pics/', blank=True)
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE)
    primario = models.BooleanField(default=False)
    secundario = models.BooleanField(default=False)
    terciario = models.BooleanField(default=False)
    pedecimientos = models.ManyToManyField(Padecimientos, default='Ninguno', blank=True)
    fecha_nac = models.DateField(null=True)
    dni = models.CharField(max_length=20)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre


class CambioContraseña(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cambio = models.BooleanField(default=True)
    es_admin = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.name} - Primer login: {self.cambio}'
    
class UsuarioAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contraseña_personal = models.CharField(max_length=100)