from django.contrib import admin
from django import forms
from .models import Imagen, Usuario, Persona
import uuid

admin.site.site_header = 'Administración del sistema'
admin.site.index_title = 'Panel de control'
admin.site.site_title = 'Votación'
admin.site.site_url = 'http://localhost:4200'

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username','area', 'email', 'first_name', 'last_name', 'is_staff','is_active')  # Campos existentes
    search_fields = ('username','area', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    def save_model(self, request, obj, form, change):
        # Verifica si es un cambio en la contraseña
        if not change:  # Si es un nuevo usuario
            if obj.password:
                obj.set_password(obj.password)  # Encripta la contraseña al guardarla
        else:
            if obj.password and obj.password != form.initial['password']:
                obj.set_password(obj.password)  # Encripta si se ha cambiado la contraseña
        super().save_model(request, obj, form, change)

# Crear un formulario personalizado para el modelo Imagen
class ImagenInlineForm(forms.ModelForm):
    archivo = forms.FileField(label="Imagen", required=False)

    class Meta:
        model = Imagen
        fields = ('archivo',)

    def save(self, commit=True):
        instance = super().save(commit=False)
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            instance.imagen = archivo.read()  # Lee el archivo y lo guarda como binario
        if commit:
            instance.save()
        return instance

# Inline para Imagen
class ImagenInline(admin.TabularInline):
    model = Imagen
    form = ImagenInlineForm
    extra = 1
    can_delete = True

# Registro del modelo Persona
@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ci', 'solapin', 'activo', 'acceso', 'fecha')
    search_fields = ('nombre', 'ci', 'solapin')
    list_filter = ('activo', 'acceso', 'provincia', 'municipio')
    inlines = [ImagenInline]
    fieldsets = (
        (None, {
            'fields': ('nombre', 'ci', 'carrera', 'facultad', 'grupo', 'anno_academico', 
                       'solapin', 'provincia', 'municipio', 'activo', 'acceso', 'fecha')
        }),
    )
