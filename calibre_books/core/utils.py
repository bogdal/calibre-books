from django_dropbox.storage import DropboxStorage
from dropbox.rest import ErrorResponse


def get_dropbox_url(path):
    client = DropboxStorage().client
    try:
        return client.media(path).get('url')
    except ErrorResponse:
        pass
