from hashlib import sha256
import hmac
import logging
import threading

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import View

from .sync import synchronize_calibre

logger = logging.getLogger(__name__)


class DropboxWebhookView(View):

    def get(self, *args, **kwargs):
        return HttpResponse(self.request.GET.get('challenge'))

    def post(self, *args, **kwargs):
        signature = self.request.META.get('HTTP_X_DROPBOX_SIGNATURE')
        if signature != hmac.new(settings.DROPBOX_CONSUMER_SECRET, self.request.body, sha256).hexdigest():
            return HttpResponseForbidden()

        threading.Thread(target=synchronize_calibre).start()
        logger.info(u"Synchronization has been started", extra={'request': self.request})

        return HttpResponse('')
