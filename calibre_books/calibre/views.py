from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, RedirectView

from .models import Book, Data


class BookListView(ListView):
    model = Book
    template_name = 'calibre/list.html'
    paginate_by = 10


class DownloadView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        book_file = get_object_or_404(Data, pk=self.kwargs.get('pk'))
        return book_file.download_url
