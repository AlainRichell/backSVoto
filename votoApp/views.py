from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework import viewsets, status
from .models import Usuario, Persona, Imagen
from .serializers import UsuarioSerializer, PersonaSerializer, ImagenSerializer, PersonaSerializerStat
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken,TokenError, AccessToken, UntypedToken

import io
import csv



class PersonPagination(PageNumberPagination):
     #page_size_query_param = 6  # Número de elementos por páginas
     page_size =10
# Usuario API ViewSet
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    
    
    # Endpoint para obtener persona y su imagen por codigo barra
    @action(detail=False, methods=['get'])
    def persona_con_imagen(self, request):
        codigobarra = request.query_params.get('codigobarra')
        if not codigobarra:
            return Response({'error': 'Se requiere el parámetro codigo barra'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            persona = Persona.objects.get(codigobarra__iexact=codigobarra)
            if not persona.activo:
                persona_data = PersonaSerializer(persona).data
                return Response({'error': 'Estudiante inactivo','persona': persona_data}, status=status.HTTP_400_BAD_REQUEST)
            if persona.acceso:
                return Response({'error': 'El Estudiante ya realizó su voto'}, status=status.HTTP_400_BAD_REQUEST)
            persona.acceso = True
            persona.fecha = timezone.now()
            persona.save()
            persona_data = PersonaSerializer(persona).data
            # Verificar si la persona tiene una imagen asociada
            try:
                imagen = Imagen.objects.get(idpersona=persona)
                imagen_data = ImagenSerializer(imagen).data
            except Imagen.DoesNotExist:
                imagen_data = None

            return Response({'persona': persona_data, 'imagen': imagen_data})
            
        except Persona.DoesNotExist:
            return Response({'error': 'Estudiante no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Endpoint para cambiar el estado activo de una persona
    @action(detail=False, methods=['get'])
    def cambiar_estado_activo(self, request):
        solapin = request.query_params.get('solapin')
        if not solapin:
            return Response({'error': 'Se requiere el parámetro solapin'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            persona = Persona.objects.get(solapin__iexact=solapin)
            persona.activo = True #not persona.activo
            persona.acceso = True
            persona.fecha = timezone.now()
            persona.save()
            persona_data = PersonaSerializer(persona).data
            try:
                imagen = Imagen.objects.get(idpersona=persona)
                imagen_data = ImagenSerializer(imagen).data
            except Imagen.DoesNotExist:
                imagen_data = None
            return Response({'persona': persona_data,'imagen': imagen_data})
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
    
    
    #Listado de votos registrados por facultad
    @action(detail=False, methods=['get'])
    def personas_con_acceso(self, request):
        facultad = request.query_params.get('facultad')
        if not facultad:
            return Response({'error': 'Se requiere el parámetro facultad'}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar personas por facultad, activo=True y acceso=True
        personas = Persona.objects.filter(facultad=facultad, activo=True, acceso=True)

        # Serializar los datos
        personas_data = PersonaSerializer(personas, many=True).data

        # Responder con los datos
        return Response({
            'personas': personas_data
        }, status=status.HTTP_200_OK)
       


    #Listado de personas sin votar por facultad
    @action(detail=False, methods=['get'])
    def personas_sin_acceso(self, request):
        facultad = request.query_params.get('facultad')
        if not facultad:
            return Response({'error': 'Se requiere el parámetro facultad'}, status=status.HTTP_400_BAD_REQUEST)

        # Filtrar personas por facultad, activo=True y acceso=False
        personas = Persona.objects.filter(facultad=facultad, activo=True, acceso=False)

        # Serializar los datos
        personas_data = PersonaSerializer(personas, many=True).data

        # Responder con los datos
        return Response({
            'personas': personas_data
        }, status=status.HTTP_200_OK)

    #listado de todos los estudiantes activos por facultad
    @action(detail=False, methods=['get'])
    def personas_activas(self, request):
        facultad = request.query_params.get('facultad')
        if not facultad:
            return Response({'error': 'Se requiere el parámetro facultad'}, status=status.HTTP_400_BAD_REQUEST)
    
        # Filtrar personas por facultad y activo=True
        personas = Persona.objects.filter(facultad=facultad, activo=True)
    
        # Serializar los datos
        personas_data = PersonaSerializer(personas, many=True).data
    
       
        return Response({
            'personas': personas_data
        }, status=status.HTTP_200_OK)

#listados generales
    #Listado de votos generales registrados 
    @action(detail=False, methods=['get'])
    def personas_con_acceso_general(self, request):
        # Filtrar personas por facultad, activo=True y acceso=True
        personas = Persona.objects.filter(activo=True, acceso=True)

        # Serializar los datos
        personas_data = PersonaSerializer(personas, many=True).data

        # Responder con los datos
        return Response({
            'personas': personas_data
        }, status=status.HTTP_200_OK)
       


    #Listado general de personas sin votar
    @action(detail=False, methods=['get'])
    def personas_sin_acceso_general(self, request):
        # Filtrar personas por facultad, activo=True y acceso=False
        personas = Persona.objects.filter(activo=True, acceso=False)

        # Serializar los datos
        personas_data = PersonaSerializer(personas, many=True).data

        # Responder con los datos
        return Response({
            'personas': personas_data
        }, status=status.HTTP_200_OK)

    #listado de todos los estudiantes activos
    @action(detail=False, methods=['get'])
    def personas_activas_general(self, request):
        # Filtrar personas por facultad y activo=True
        personas = Persona.objects.filter(activo=True)
    
        # Serializar los datos
        personas_data = PersonaSerializer(personas, many=True).data
    
       
        return Response({
            'personas': personas_data
        }, status=status.HTTP_200_OK)
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


class FacultadStatsAPIView(APIView):
    def get(self, request, facultad):
        
        personas = Persona.objects.filter(facultad=facultad, activo=True)

        # Total de personas en la facultad
        total_personas = personas.count()
        
        personas_fecha = personas.filter(acceso=True).order_by('-fecha')
        personas_data = PersonaSerializerStat(personas_fecha, many=True).data
        # Total de personas con acceso=True en esa facultad
        con_acceso = personas_fecha.count()

        # Calcular el porcentaje, manejando posibles divisiones por cero
        porciento = (con_acceso / total_personas * 100) if total_personas > 0 else 0
        # Construir la respuesta
        data = {
            "facultad": facultad,
            "total": total_personas,
            "con_acceso": con_acceso,
            "sin_acceso":total_personas - con_acceso,
            "porciento": round(porciento, 2),
            "porciento_restante": round(100 - porciento, 2),
            "personas":personas_data
        }
        return Response(data, status=status.HTTP_200_OK)
class GeneralStatsAPIView(APIView):
    def get(self, request):
        
        personas = Persona.objects.filter(activo=True)

        # Total de personas en la facultad
        total_personas = personas.count()
        
        personas_fecha = personas.filter(acceso=True).order_by('-fecha')
        personas_data = PersonaSerializerStat(personas_fecha, many=True).data
        # Total de personas con acceso=True en esa facultad
        con_acceso = personas_fecha.count()

        # Calcular el porcentaje, manejando posibles divisiones por cero
        porciento = (con_acceso / total_personas * 100) if total_personas > 0 else 0
        # Construir la respuesta
        data = {
            "total": total_personas,
            "con_acceso": con_acceso,
            "sin_acceso":total_personas - con_acceso,
            "porciento": round(porciento, 2),
            "porciento_restante": round(100 - porciento, 2),
            "personas":personas_data
        }
        return Response(data, status=status.HTTP_200_OK)
class CsvView(viewsets.ViewSet):
    queryset = Persona.objects.all()
    @action(detail=False, methods=["get"])
    def csv_listado_facultad(self,request,pk= None):
        facultad = request.query_params.get('facultad')
        if not facultad:
            return Response({'error': 'Debe Proporcionar una facultad'}, status=400)
        personas = Persona.objects.exclude(activo=False)
        personas = personas.filter(facultad=facultad)
        response = HttpResponse(content_type ='text/csv')
        response['Content-Disposition'] = f'attachment; filename="ciudadanos_UCI.csv"'

        writer = csv.writer(response)
        writer.writerow(['Id', 'Nombre','Ci','Carrera', 'Facultad',
         'Grupo', 'Solapin','Año Académico','Provincia','Municipio',
         'Fecha'])
      
        for persona in personas:
            fecha = None
            if(persona.fecha):
             fecha = persona.fecha.strftime('%d-%m-%Y')
            writer.writerow([persona.idpersona, persona.nombre,persona.ci,
            persona.carrera, persona.facultad, persona.grupo,
             persona.solapin,persona.anno_academico,persona.provincia,persona.municipio,
             fecha ])
        return response

    @action(detail=False, methods=["get"])
    def csv_listado_facultad_con_acceso(self,request,pk= None):
        facultad = request.query_params.get('facultad')
        if not facultad:
            return Response({'error': 'Debe Proporcionar una facultad'}, status=400)
        personas = Persona.objects.exclude(activo=False)
        personas = personas.filter(facultad=facultad, acceso=True)
        response = HttpResponse(content_type ='text/csv')
        response['Content-Disposition'] = f'attachment; filename="ciudadanos_UCI.csv"'

        writer = csv.writer(response)
        writer.writerow(['Id', 'Nombre','Ci','Carrera', 'Facultad',
         'Grupo', 'Solapin','Año Académico','Provincia','Municipio',
         'Fecha'])
      
        for persona in personas:
            fecha = None
            if(persona.fecha):
             fecha = persona.fecha.strftime('%d-%m-%Y')
            writer.writerow([persona.idpersona, persona.nombre,persona.ci,
            persona.carrera, persona.facultad, persona.grupo,
             persona.solapin,persona.anno_academico,persona.provincia,persona.municipio,
             fecha ])
        return response


    @action(detail=False, methods=["get"])
    def csv_listado_facultad_sin_acceso(self,request,pk= None):
        facultad = request.query_params.get('facultad')
        if not facultad:
            return Response({'error': 'Debe Proporcionar una facultad'}, status=400)
        personas = Persona.objects.exclude(activo=False)
        personas = personas.filter(facultad=facultad,acceso=False)
        response = HttpResponse(content_type ='text/csv')
        response['Content-Disposition'] = f'attachment; filename="ciudadanos_UCI.csv"'

        writer = csv.writer(response)
        writer.writerow(['Id', 'Nombre','Ci','Carrera', 'Facultad',
         'Grupo', 'Solapin','Año Académico','Provincia','Municipio',
         'Fecha'])
      
        for persona in personas:
            fecha = None
            if(persona.fecha):
             fecha = persona.fecha.strftime('%d-%m-%Y')
            writer.writerow([persona.idpersona, persona.nombre,persona.ci,
            persona.carrera, persona.facultad, persona.grupo,
             persona.solapin,persona.anno_academico,persona.provincia,persona.municipio,
             fecha ])
        return response 
 ##Listado general
    @action(detail=False, methods=["get"])
    def csv_listado_sin_acceso(self,request,pk= None):
        personas = Persona.objects.exclude(activo=False)
        personas = personas.filter(acceso=False)
        response = HttpResponse(content_type ='text/csv')
        response['Content-Disposition'] = f'attachment; filename="ciudadanos_UCI.csv"'

        writer = csv.writer(response)
        writer.writerow(['Id', 'Nombre','Ci','Carrera', 'Facultad',
         'Grupo', 'Solapin','Año Académico','Provincia','Municipio',
         'Fecha'])
      
        for persona in personas:
            fecha = None
            if(persona.fecha):
             fecha = persona.fecha.strftime('%d-%m-%Y')
            writer.writerow([persona.idpersona, persona.nombre,persona.ci,
            persona.carrera, persona.facultad, persona.grupo,
             persona.solapin,persona.anno_academico,persona.provincia,persona.municipio,
             fecha ])
        return response

    @action(detail=False, methods=["get"])
    def csv_listado_con_acceso(self,request,pk= None):
        personas = Persona.objects.exclude(activo=False)
        personas = personas.filter(acceso=True)
        response = HttpResponse(content_type ='text/csv')
        response['Content-Disposition'] = f'attachment; filename="ciudadanos_UCI.csv"'

        writer = csv.writer(response)
        writer.writerow(['Id', 'Nombre','Ci','Carrera', 'Facultad',
         'Grupo', 'Solapin','Año Académico','Provincia','Municipio',
         'Fecha'])
      
        for persona in personas:
            fecha = None
            if(persona.fecha):
             fecha = persona.fecha.strftime('%d-%m-%Y')
            writer.writerow([persona.idpersona, persona.nombre,persona.ci,
            persona.carrera, persona.facultad, persona.grupo,
             persona.solapin,persona.anno_academico,persona.provincia,persona.municipio,
             fecha ])
        return response


    @action(detail=False, methods=["get"])
    def csv_listado_completo(self,request,pk= None):
        personas = Persona.objects.exclude(activo=False)
        
        response = HttpResponse(content_type ='text/csv')
        response['Content-Disposition'] = f'attachment; filename="ciudadanos_UCI.csv"'

        writer = csv.writer(response)
        writer.writerow(['Id', 'Nombre','Ci','Carrera', 'Facultad',
         'Grupo', 'Solapin','Año Académico','Provincia','Municipio',
         'Fecha'])
      
        for persona in personas:
            fecha = None
            if(persona.fecha):
             fecha = persona.fecha.strftime('%d-%m-%Y')
            writer.writerow([persona.idpersona, persona.nombre,persona.ci,
            persona.carrera, persona.facultad, persona.grupo,
             persona.solapin,persona.anno_academico,persona.provincia,persona.municipio,
             fecha ])
        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Llamar al método de la clase base para obtener el par de tokens
        response = super().post(request, *args, **kwargs)

        # Obtener el usuario
        username = request.data.get("username")
        try:
            user = Usuario.objects.get(username=username)  # O usa tu modelo de Usuario personalizado
            area = user.area  # Obtener el campo 'area' del usuario
        except Usuario.DoesNotExist:
            return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Añadir el campo 'area' a la respuesta
        data = response.data
        data["area"] = area  # Agregar 'area' al diccionario de respuesta

        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def validateToken(request):
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Se requiere un token en la solicitud.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        UntypedToken(token)
        return Response(status=status.HTTP_200_OK)
    except TokenError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)