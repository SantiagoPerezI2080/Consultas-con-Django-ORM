from django.db import models

# Create your models here.

class Estudiante (models.Model):
    nombre  = models.CharField(max_length=50)
    edad    = models.PositiveIntegerField()
    vive    = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class Curso (models.Model):
    nombre = models.CharField(max_length=50)
    horas = models.PositiveIntegerField()
    disponible = models.BooleanField(default=True)
    jornada = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.CharField(max_length=2000)

class Inscritos(models.Model):
    id_estudiante       = models.ForeignKey(Estudiante, on_delete= models.PROTECT)
    id_curso            = models.ForeignKey(Curso, on_delete= models.PROTECT)
    fecha_inscripcion   = models.DateTimeField(auto_now_add=True)
    fecha_modificacion  = models.DateTimeField(auto_now= True, null= True, blank= True)

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    publicado = models.DateField()

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

class LibroCategoria(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    