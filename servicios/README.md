## Requisitos
- Tener instalado Django y configurado el proyecto.
- Conocer la estructura de los modelos y sus relaciones en el proyecto.
- Familiaridad básica con la shell de Django para ejecutar consultas.

## Guía Paso a Paso para Ejecutar Consultas en la Shell de Django
1. Abrir la Shell de Django
Abre tu terminal y ejecuta el siguiente comando:
    python manage.py shell
2. Importar los Modelos y Herramientas Necesarias
Una vez en la shell, ingresa lo siguiente para importar los modelos y funciones que utilizarás:
    from app.models import Estudiante, Curso, Libro, Categoria, LibroCategoria
    from django.db.models import Q, F

## Ejemplos de Consultas
Consulta Básica en Estudiante
Obtener todos los estudiantes:
    estudiantes = Estudiante.objects.all()
    print(estudiantes)

Consulta Individual
Obtener el estudiante con id 1 (si existe):
    estudiante = Estudiante.objects.get(id=1) if Estudiante.objects.filter(id=1).exists() else None
    print(estudiante)

Filtrado con Q
Filtrar estudiantes con edad menor a 20 o cuyo nombre contenga 'rry':
    estudiantes_q = Estudiante.objects.filter(Q(edad__lt=20) | Q(nombre__icontains="rry"))
    print(list(estudiantes_q))

Consulta Optimizada
Obtener libros con optimización de consulta utilizando select_related y prefetch_related:
    libros_opt = Libro.objects.select_related('autor').prefetch_related('librocategoria_set__categoria').all()
    print(list(libros_opt))

Consulta con F
En el endpoint consulta_F del viewset de Libro se utiliza F('autor__edad') para comparar un campo con otro dentro de la base de datos. Puedes probarlo en la shell de la siguiente manera:
    libros_f = Libro.objects.filter(publicado__lt=F('autor__edad'))
    print(list(libros_f))

Relación Muchos a Muchos entre Libro y Categoria
En el endpoint categorias del viewset de Libro se muestra cómo obtener las categorías asociadas a un libro a través del modelo intermedio LibroCategoria. Para probarlo en la shell:
    libro = Libro.objects.first()  # Por ejemplo, tomar el primer libro
    if libro:
        categorias = Categoria.objects.filter(librocategoria__libro=libro)
        print(list(categorias))