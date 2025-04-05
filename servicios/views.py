from django.shortcuts import render
from django.db.models import Q, F
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Estudiante, Curso, Inscritos, Libro, Categoria, LibroCategoria, Autor
from .serializers import (
    estudiante_serializer,
    curso_serializer,
    inscrito_serializer,
    autor_serializer,
    libro_serializer,
    categoria_serializer,
    libroCategoria_serializer
)

# --- Viewset para Estudiante ---
class EstudianteViewset(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = estudiante_serializer

    # Ejemplo: Consulta básica y avanzada
    @action(detail=False, methods=['get'])
    def ejemplos(self, request):
        # Consulta básica: obtener todos los estudiantes
        estudiantes = Estudiante.objects.all()

        # Consulta básica: obtener estudiante por id
        estudiante = Estudiante.objects.get(id=1) if Estudiante.objects.filter(id=1).exists() else None

        # Consulta filtrada: estudiantes menores de 20 años
        estudiantes_jovenes = Estudiante.objects.filter(edad__lt=20)

        # Consulta con Q: estudiantes menores de 20 o cuyo nombre contiene "rry"
        estudiantes_q = Estudiante.objects.filter(Q(edad__lt=20) | Q(nombre__icontains="ryy"))

        # Optimización: solo obtener 'nombre' y 'edad'
        estudiantes_reducido = Estudiante.objects.only('nombre', 'edad')

        # Se preparan datos de ejemplo para visualizar
        datos = {
            'total_estudiantes': estudiantes.count(),
            'estudiante_id_1': estudiante.nombre if estudiante else 'No existe',
            'estudiantes_jovenes': [est.nombre for est in estudiantes_jovenes],
            'consulta_Q': [est.nombre for est in estudiantes_q],
            'estudiantes_reducido': list(estudiantes_reducido.values('nombre', 'edad')),
        }
        return Response(datos)

# --- Viewset para Curso ---
class CursoViewset(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = curso_serializer

    # Ejemplo: Consultas básicas en Cursos
    @action(detail=False, methods=['get'])
    def ejemplos(self, request):
        # Obtener todos los cursos
        cursos = Curso.objects.all()

        # Obtener curso por id
        curso = Curso.objects.get(id=1) if Curso.objects.filter(id=1).exists() else None

        # Filtrar cursos disponibles
        cursos_disponibles = Curso.objects.filter(disponible=True)

        # Excluir cursos con menos de 10 horas
        cursos_excluidos = Curso.objects.exclude(horas__lt=10)

        # Ordenar cursos por horas
        cursos_ordenados = Curso.objects.order_by('horas')

        datos = {
            'total_cursos': cursos.count(),
            'curso_id_1': curso.nombre if curso else 'No existe',
            'cursos_disponibles': [c.nombre for c in cursos_disponibles],
            'cursos_excluidos': [c.nombre for c in cursos_excluidos],
            'cursos_ordenados': [c.nombre for c in cursos_ordenados],
        }
        return Response(datos)

# --- Viewset para Libro ---
class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = libro_serializer

    # Ejemplo: Consulta optimizada de libros con autor y categorías
    @action(detail=False, methods=['get'])
    def optimizados(self, request):
        # Optimización: select_related para autor y prefetch_related para categorías (vía LibroCategoria)
        libros = Libro.objects.select_related('autor').prefetch_related('librocategoria_set__categoria').all()
        serializer = self.get_serializer(libros, many=True)
        return Response(serializer.data)

    # Ejemplo: Uso de F en una consulta (ilustrativo)
    @action(detail=False, methods=['get'])
    def consulta_F(self, request):
        # Nota: Este ejemplo compara 'publicado' con 'autor__edad' y es solo para ilustrar el uso de F.
        libros_f = Libro.objects.filter(publicado__lt=F('autor__edad'))
        serializer = self.get_serializer(libros_f, many=True)
        return Response(serializer.data)

    # Ejemplo: Consultas sobre la relación muchos a muchos entre Libro y Categoria
    @action(detail=True, methods=['get'])
    def categorias(self, request, pk=None):
        # Obtener un libro específico y luego las categorías asociadas mediante la tabla intermedia LibroCategoria
        try:
            libro = Libro.objects.get(pk=pk)
        except Libro.DoesNotExist:
            return Response({"error": "Libro no encontrado"}, status=404)
        # Consulta: obtener todas las categorías asociadas al libro
        categorias = Categoria.objects.filter(librocategoria__libro=libro)
        # Utilizamos el serializer de Categoria para retornar los datos
        serializer = categoria_serializer(categorias, many=True)
        return Response(serializer.data)

# --- Viewset para Categoria ---
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = categoria_serializer

    # Ejemplo: Obtener libros asociados a una categoría específica (usando LibroCategoria)
    @action(detail=True, methods=['get'])
    def libros(self, request, pk=None):
        # Obtiene la categoría especificada
        try:
            categoria = Categoria.objects.get(pk=pk)
        except Categoria.DoesNotExist:
            return Response({"error": "Categoría no encontrada"}, status=404)
        # Consulta: obtener libros relacionados a esta categoría
        libros = Libro.objects.filter(librocategoria__categoria=categoria)
        serializer = libro_serializer(libros, many=True)
        return Response(serializer.data)

# --- Viewsets para los demás modelos (Inscritos, Autor y LibroCategoria) se mantienen sin cambios ---
class InscritoViewset(viewsets.ModelViewSet):
    queryset =  Inscritos.objects.all()
    serializer_class = inscrito_serializer

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = autor_serializer

class LibroCategoriaViewSet(viewsets.ModelViewSet):
    queryset = LibroCategoria.objects.all()
    serializer_class = libroCategoria_serializer