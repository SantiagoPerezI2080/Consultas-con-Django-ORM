from rest_framework import serializers
from .models import *

class estudiante_serializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ['id','nombre','edad','vive']

class curso_serializer (serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['nombre', 'horas', 'disponible', 'jornada', 'descripcion']
class inscrito_serializer (serializers.ModelSerializer):
    class Meta:
        model = Inscritos
        fields = ['id_estudiante', 'id_curso','fecha_inscripcion', 'fecha_modificacion']

class autor_serializer (serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['nombre', 'edad']

class libro_serializer (serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'publicado']

class categoria_serializer (serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['nombre']

class libroCategoria_serializer (serializers.ModelSerializer):
    class Meta:
        model = LibroCategoria
        fields = ['libro', 'categoria']