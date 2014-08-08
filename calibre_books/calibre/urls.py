from django.conf.urls import patterns, url

from .views import BookListView, DownloadView

urlpatterns = patterns('',
    url(r'^$', BookListView.as_view(), name='list'),
    url(r'^download/(?P<pk>\d+)/', DownloadView.as_view(), name='download')
)
