from django.contrib import admin
from .models import NotasAlumnosPorCurso
from .models import Curso
from .models import Alumno


# Register your models here.
admin.site.register(Alumno)
admin.site.register(Curso)
admin.site.register(NotasAlumnosPorCurso)