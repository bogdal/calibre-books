from django.views.generic import ListView
from calibre_books.calibre.models import Book


class BookListView(ListView):
    model = Book
    template_name = 'book/list.html'
