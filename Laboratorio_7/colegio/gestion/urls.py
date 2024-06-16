from django.urls import path
from . import views

urlpatterns = [
    path('agregar_alumno/', views.agregar_alumno, name='agregar_alumno'),
    path('listar_alumnos/', views.listar_alumnos, name='listar_alumnos'),
    path('agregar_curso/', views.agregar_curso, name='agregar_curso'),
    path('listar_cursos/', views.listar_cursos, name='listar_cursos'),
    path('agregar_nota/', views.agregar_nota, name='agregar_nota'),
    path('listar_notas/', views.listar_notas, name='listar_notas'),
]
