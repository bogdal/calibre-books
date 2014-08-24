import logging

from django.shortcuts import get_object_or_404
from django.utils.http import urlencode
from django.views.generic import ListView, RedirectView

from .models import Book, Data

logger = logging.getLogger(__name__)


class BookListView(ListView):
    model = Book
    template_name = 'calibre/list.html'
    paginate_by = 12

    def get_queryset(self):
        qs = super(BookListView, self).get_queryset()
        qs_kwargs = {}
        if 'author' in self.request.GET:
            qs_kwargs['authors__name__in'] = self.request.GET.getlist('author')
        if 'tag' in self.request.GET:
            qs_kwargs['tags__name__in'] = self.request.GET.getlist('tag')
        return qs.filter(**qs_kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        context['filters'] = urlencode({'author': self.request.GET.getlist('author'),
                                        'tag': self.request.GET.getlist('tag')}, doseq=1)
        return context


class DownloadView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        book_file = get_object_or_404(Data, pk=self.kwargs.get('pk'))
        logger.info(u"Book '%s' has been downloaded by the user '%s'", book_file.book, self.request.user,
                    extra={'request': self.request})
        return book_file.download_url
