from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from .models import Usuario, Persona, Imagen
from .serializers import UsuarioSerializer, PersonaSerializer, ImagenSerializer

# Usuario API ViewSet
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    # Endpoint para obtener persona y su imagen por solapin
    @action(detail=False, methods=['get'])
    def persona_con_imagen(self, request):
        solapin = request.query_params.get('solapin')
        if not solapin:
            return Response({'error': 'Se requiere el parámetro solapin'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            persona = Persona.objects.get(solapin__iexact=solapin)
            persona_data = PersonaSerializer(persona).data

            # Verificar si la persona tiene una imagen asociada
            try:
                imagen = Imagen.objects.get(idpersona=persona)
                imagen_data = ImagenSerializer(imagen).data
            except Imagen.DoesNotExist:
                imagen_data = None

            return Response({'persona': persona_data, 'imagen': imagen_data})
        except Persona.DoesNotExist:
            return Response({'error': 'Persona no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    # Endpoint para cambiar el estado activo de una persona
    @action(detail=False, methods=['post'])
    def cambiar_estado_activo(self, request):
        solapin = request.data.get('solapin')
        if not solapin:
            return Response({'error': 'Se requiere el parámetro solapin'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            persona = Persona.objects.get(solapin__iexact=solapin)
            persona.activo = not persona.activo
            persona.save()
            return Response({'status': 'Estado activo cambiado', 'activo': persona.activo})
        except Persona.DoesNotExist:
            return Response({'error': 'Persona no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    # Endpoint para cambiar el estado de acceso de una persona
    @action(detail=False, methods=['post'])
    def cambiar_estado_acceso(self, request):
        solapin = request.data.get('solapin')
        if not solapin:
            return Response({'error': 'Se requiere el parámetro solapin'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            persona = Persona.objects.get(solapin__iexact=solapin)
            persona.acceso = not persona.acceso
            persona.save()
            return Response({'status': 'Estado de acceso cambiado', 'acceso': persona.acceso})
        except Persona.DoesNotExist:
            return Response({'error': 'Persona no encontrada'}, status=status.HTTP_404_NOT_FOUND)

# Imagen API ViewSet
class ImagenViewSet(viewsets.ModelViewSet):
    queryset = Imagen.objects.all()
    serializer_class = ImagenSerializer

    # Ejemplo de acción personalizada: obtener imagen por persona
    @action(detail=False, methods=['get'])
    def por_persona(self, request):
        idpersona = request.query_params.get('idpersona')
        if not idpersona:
            return Response({'error': 'Se requiere el parámetro idpersona'}, status=400)
        try:
            imagen = Imagen.objects.get(idpersona=idpersona)
            serializer = self.get_serializer(imagen)
            return Response(serializer.data)
        except Imagen.DoesNotExist:
            return Response({'error': 'Imagen no encontrada'}, status=404)
