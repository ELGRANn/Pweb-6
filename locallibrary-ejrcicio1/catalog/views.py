from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
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
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_visits':num_visits,
    }


    # Renderizar la plantilla HTML index.html con los datos en la variable de contexto
    return render(request, 'index.html', context=context)
from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10    

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Vista genérica basada en clases que enumera los libros prestados al usuario actual.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')