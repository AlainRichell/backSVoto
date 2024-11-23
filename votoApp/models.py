from django.db import models

class Usuario(models.Model):
    idusuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    contrasena = models.CharField(max_length=8, unique=True)
    def __str__(self):
        return self.nombre

class Persona(models.Model):
    idpersona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=True)
    ci = models.CharField(max_length=255, unique=True, null=True)
    carrera = models.CharField(max_length=255, null=True)
    facultad = models.CharField(max_length=255, null=True)
    grupo = models.CharField(max_length=255, null=True)
    anno_academico = models.CharField(max_length=255, null=True)
    solapin = models.CharField(max_length=255, unique=True)
    provincia = models.CharField(max_length=255, null=True)
    municipio = models.CharField(max_length=255,null=True)
    activo = models.BooleanField(default=True, null=True)
    acceso = models.BooleanField(default=False, null=True)
    fecha = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.nombre} ({self.ci})"

class Imagen(models.Model):
    idpersona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name="imagen")
    imagen = models.BinaryField()

    def __str__(self):
        return f"Imagen de {self.idpersona.nombre}"

