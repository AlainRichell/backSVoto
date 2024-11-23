from rest_framework import serializers
from .models import Usuario, Persona, Imagen

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['idusuario', 'nombre', 'contrasena']

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = [
            'idpersona', 'nombre', 'ci', 'carrera', 'facultad', 'grupo',
            'anno_academico', 'solapin', 'provincia', 'municipio', 'activo',
            'acceso', 'fecha'
        ]

class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = ['idpersona', 'imagen']
