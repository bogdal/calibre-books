from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import BookListView, DownloadView

urlpatterns = patterns('',
    url(r'^$', login_required(BookListView.as_view()), name='list'),
    url(r'^download/(?P<pk>\d+)/', login_required(DownloadView.as_view()), name='download')
)
