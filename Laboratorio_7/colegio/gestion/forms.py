from django import forms
from .models import Alumno, Curso, NotaAlumnosPorCurso

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'email']

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'descripcion']

class NotaAlumnosPorCursoForm(forms.ModelForm):
    class Meta:
        model = NotaAlumnosPorCurso
        fields = ['alumno', 'curso', 'nota']
