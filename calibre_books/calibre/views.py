import logging

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, RedirectView

from .models import Book, Data

logger = logging.getLogger(__name__)


class BookListView(ListView):
    model = Book
    template_name = 'calibre/list.html'
    paginate_by = 12


class DownloadView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        book_file = get_object_or_404(Data, pk=self.kwargs.get('pk'))
        logger.info(u"Book '%s' has been downloaded by the user '%s'", book_file.book, self.request.user,
                    extra={'request': self.request})
        return book_file.download_url
