from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generar recuentos de algunos de los objetos principales
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Libros disponibles (estado = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # El 'all()' se sobreentiende de forma predeterminada.
    num_authors = Author.objects.count()

    # Recuento de géneros
    num_genres = Genre.objects.all().count()

    #Recuento de libros que contienen una palabra específica 
    num_books_with_word = Book.objects.filter(title__icontains='python').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_with_word': num_books_with_word,
    }
    # Renderizar la plantilla HTML index.html con los datos en la variable de contexto
    return render(request, 'index.html', context=context)