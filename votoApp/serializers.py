from rest_framework import serializers
from .models import Usuario, Persona, Imagen

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'area']

class PersonaSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Persona
        fields = '__all__'


class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = ['idpersona', 'imagen']

class PersonaStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    con_acceso = serializers.IntegerField()
    porciento = serializers.FloatField()

class PersonaSerializerStat(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'