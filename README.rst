Calibre Books
=============


Usage
-----


1. Install the project in development mode::
  
    python setup.py develop
    
2. Set your ``SECRET_KEY`` in the environment variable::

    export SECRET_KEY=''

3. Prepare the database::

    python manage.py syncdb
    
    
4. Configure your `dropbox` application::

    export DROPBOX_CONSUMER_KEY=''
    export DROPBOX_CONSUMER_SECRET=''
    export DROPBOX_ACCESS_TOKEN=''
    export DROPBOX_ACCESS_TOKEN_SECRET=''
