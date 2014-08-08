from django_dropbox.storage import DropboxStorage
from dropbox.rest import ErrorResponse


def get_dropbox_url(path, share=False):
    client = DropboxStorage().client
    try:
        if share:
            return client.share(path, short_url=False)['url'] + '?dl=1'
        return client.media(path).get('url')
    except ErrorResponse:
        pass
