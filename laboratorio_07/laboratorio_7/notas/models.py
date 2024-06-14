from django.db import models

# Create your models here.
class Alumno(models.Model):
    CUI = models.IntegerField()
    nombres = models.TextField()
    apellidos = models.TextField()

class Curso(models.Model):
    id_curso = models.IntegerField()
    nombre_curso = models.TextField()

class NotasAlumnosPorCurso(models.Model):
    cui_alumno = models.IntegerField()
    id_curso = models.IntegerField()
    nota = models.IntegerField()
    
