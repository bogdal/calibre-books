from django.views.generic import TemplateView


class BookListView(TemplateView):
    template_name = 'book/list.html'
