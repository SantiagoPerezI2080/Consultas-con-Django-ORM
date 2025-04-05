from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'estudiantes', EstudianteViewset)
router.register(r'cursos', CursoViewset)
router.register(r'inscritos', InscritoViewset)
router.register(r'autor', AutorViewSet)
router.register(r'libro', LibroViewSet)
router.register(r'categoria', CategoriaViewSet)
router.register(r'libroCategoria', LibroCategoriaViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]