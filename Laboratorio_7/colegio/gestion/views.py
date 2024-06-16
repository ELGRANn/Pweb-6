from django.shortcuts import render, redirect
from .forms import AlumnoForm, CursoForm, NotaAlumnosPorCursoForm
from .models import Alumno, Curso, NotaAlumnosPorCurso

def agregar_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_alumnos')
    else:
        form = AlumnoForm()
    return render(request, 'gestion/agregar_alumno.html', {'form': form})

def listar_alumnos(request):
    alumnos = Alumno.objects.all()
    return render(request, 'gestion/listar_alumnos.html', {'alumnos': alumnos})

def agregar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_cursos')
    else:
        form = CursoForm()
    return render(request, 'gestion/agregar_curso.html', {'form': form})

def listar_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'gestion/listar_cursos.html', {'cursos': cursos})

def agregar_nota(request):
    if request.method == 'POST':
        form = NotaAlumnosPorCursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_notas')
    else:
        form = NotaAlumnosPorCursoForm()
    return render(request, 'gestion/agregar_nota.html', {'form': form})

def listar_notas(request):
    notas = NotaAlumnosPorCurso.objects.all()
    return render(request, 'gestion/listar_notas.html', {'notas': notas})
