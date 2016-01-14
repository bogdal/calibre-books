Calibre Books
=============

Calibre web server based on the library data located on Dropbox.

.. image:: https://img.shields.io/circleci/project/bogdal/calibre-books/master.svg
    :target: https://circleci.com/gh/bogdal/calibre-books/tree/master
    
.. image:: https://requires.io/github/bogdal/calibre-books/requirements.svg?branch=master
    :target: https://requires.io/github/bogdal/calibre-books/requirements/?branch=master

Usage
-----


1. Install the project in development mode
::
  
    python setup.py develop
    
2. Set your ``SECRET_KEY`` in the environment variable
::

    export SECRET_KEY=''

3. Prepare the database
::

    python manage.py migrate

4. Integration with `dropbox` service

Get your access token using the following command
::
  
    python manage.py get_dropbox_token

Configure your `dropbox` application::

    export DROPBOX_CONSUMER_KEY=''
    export DROPBOX_CONSUMER_SECRET=''
    export DROPBOX_ACCESS_TOKEN=''
    export DROPBOX_ACCESS_TOKEN_SECRET=''
    
    # default is standard calibre directory `CalibreLibrary`
    export DROPBOX_CALIBRE_DIR='' 

Go to the dropbox app console_ and set your webook url `https://your-domain/dropbox-webhook/`
  
.. _console: https://www.dropbox.com/developers/apps/info/
  
5. Synchronize `calibre` data
::

    python manage.py synchronize

Each time when you change something in the `Calibre` application, `Dropbox` will send callback to synchronize data.
  
