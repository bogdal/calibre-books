import os
from dj_static import Cling, MediaCling

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "calibre_books.settings")

from django.core.wsgi import get_wsgi_application
application = Cling(MediaCling(get_wsgi_application()))
