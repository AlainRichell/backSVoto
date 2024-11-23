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
    list_display = ('nombre', 'contrasena')
    search_fields = ('nombre',)

    def get_fields(self, request, obj=None):
        if not obj:  # Si se está creando un nuevo afiliado
            return ['nombre']  # Mostrar solo el campo 'nombre'
        else:  # Si se está editando, mostrar 'nombre' y 'codigo'
            return ['nombre', 'contrasena']

    def save_model(self, request, obj, form, change):
        if not change:  # Solo si es un nuevo registro
            # Genera un código único
            obj.contrasena = self.generate_unique_code()
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si se está editando
            return ['contrasena']
        else:
            return []

    # Función para generar un código único
    def generate_unique_code(self):
        import uuid
        while True:
            contrasena = str(uuid.uuid4()).split('-')[0]  # Genera un código de 8 caracteres
            if not Usuario.objects.filter(contrasena=contrasena).exists():  # Verifica si ya existe
                return contrasena
            
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
