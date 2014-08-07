from django.conf.urls import patterns, url

from .views import BookListView

urlpatterns = patterns('',
    url(r'^$', BookListView.as_view(), name='list'),
)
