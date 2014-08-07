from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('calibre_books.calibre.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
