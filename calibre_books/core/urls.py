from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

from .views import DropboxWebhookView

urlpatterns = patterns('',
    url(r'^dropbox-webhook/$', csrf_exempt(DropboxWebhookView.as_view()), name='dropbox-webhook'),
)
