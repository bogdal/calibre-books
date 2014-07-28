from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('calibre_books.book.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
