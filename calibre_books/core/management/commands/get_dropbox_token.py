from django.conf import settings
from django.core.management.base import NoArgsCommand
import dropbox


class Command(NoArgsCommand):

    def handle_noargs(self, *args, **options):
        session = dropbox.session.DropboxSession(
            settings.DROPBOX_CONSUMER_KEY,
            settings.DROPBOX_CONSUMER_SECRET,
            settings.DROPBOX_ACCESS_TYPE)
        request_token = session.obtain_request_token()

        url = session.build_authorize_url(request_token)
        print "Url:", url
        print "Please visit this website and press the 'Allow' button, " \
              "then hit 'Enter' here."
        raw_input()

        access_token = session.obtain_access_token(request_token)

        print '-' * 20
        print "export DROPBOX_ACCESS_TOKEN='%s'" % access_token.key
        print "export DROPBOX_ACCESS_TOKEN_SECRET='%s'" % access_token.secret
        print '-' * 20
