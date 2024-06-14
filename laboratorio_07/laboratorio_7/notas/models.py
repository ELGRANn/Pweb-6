from django.db import models

# Create your models here.
class Alumno(models.Model):
    CUI = models.IntegerField()#(max_digits=8)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)

class Curso(models.Model):
    id_curso = models.IntegerField()#(max_digits=5)
    nombre_curso = models.CharField(max_length=100)

class NotasAlumnosPorCurso(models.Model):
    cui_alumno = models.IntegerField()#(max_digits=8)
    id_curso = models.IntegerField()#(max_digits=5)
    nota = models.IntegerField()#(max_digits=2)
    
