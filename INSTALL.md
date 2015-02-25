Pinpit
======

Free clone of pinterest.

Install
-------

### Install dependencies ###

On a debian like system, run as root:

    # apt-get update
    # apt-get safe-upgrade
    # apt-get install python3 python3-virtualenv python3-pip python3-setuptools libpng12-dev libjpeg8-dev git libmagickwand-dev

### Set environement up ###

Run as root:

    # mkdir -p /var/www/pinpict_env
    # chown <my_user> /var/www/pinpict_env

Run as `<my_user>`:
    
    $ cd /var/www/pinpict_env
    $ virtualenv .

    New python executable in pinpict_env/bin/python
    Installing distribute..............done.
    Installing pip.....................done.

    $ source bin/activate
    $ git clone https://github.com/Fenykepy/pinpict.git
    $ cd pinpict
    $ git checkout master
    $ pip3 install -r requirements.txt



### Quick install for testing or development ###

__!!! DO NOT USE THESE INSTRUCTIONS IN PRODUCTION !!!__

Use these instructions if you plan to use pinpict in local for testing or to develop it.

#### Set up database ####

Run as root:
    
    # apt-get install python-sqlite

Run as `<my_user>`:
    
    $ cd /var/www/pinpict_env/pinpict
    $ python3 manage.py migrate

#### Create a superuser ####

Run as `<my_user>`:

    $ python3 manage.py createsuperuser

 * Answer questions to create a superuser.


#### To run unit tests ####

    $ pip3 manage.py test


#### To set up search engine ####

    $ python3 manage.py rebuild_index



#### Launch development server ####

Run as `<my_user>`:
    
    $ cd /var/www/pinpict_env/pinpict
    $ python3 manage.py runserver

 * You can use this instead if you want to access from different hosts:

    $ python3 manage.py runserver 0.0.0.0:8000

Open http://127.0.0.1:8000 in your favorite browser.




### Install for production ###

If you plan to use phiroom in local for testing it
or to develop it, go to **"Quick install for testing or development"**


#### Set up database ####

Run as root:

    # aptitude install postgresql postgresql-contrib python3-postgresql libpq-dev python-dev
    # su - postgres
    $ createdb pinpict
    $ createuser --interactive -P
    Enter name of role to add: pinpict
    Enter password for new role: 
    Enter it again: 
    Shall the new role be a superuser? (y/n) n
    Shall the new role be allowed to create databases? (y/n) n
    Shall the new role be allowed to create more new roles? (y/n) n

    $ psql

    postgres@server:~$ psql
    psql (9.1.9)
    Type "help" for help.

    postgres=# GRANT ALL PRIVILEGES ON DATABASE pinpict TO pinpict;
    GRANT
    postgres=# \q
    postgres@server:~$ logout


Fix those options in `/etc/postgresql/9.4/main/postgresql.conf`:

     # vim /etc/postgresql/9.4/main/postgresql.conf

     #----------------------
     # DJANGO CONFIGURATION
     #----------------------

     client_encoding = 'UTF8'
     default_transaction_isolation = 'read committed'
     timezone = 'UTC'

Fix those options in `/etc/postgresql/9.4/main/pg_hba.conf`:

     # vim /etc/postgresql/9.4/main/pg_hba.conf

     local   all             all                                     trust
     host    all             all             127.0.0.1/32            trust


Relaunch postgresql:

    # /etc/init.d/postgresql restart


Run as `<my_user>`:

 * Rename and complete as follow `pinpict/prod_settings.py.example`:

        $ mv pinpict/prod_settings.py.example pinpict/prod_settings.py
        $ vim pinpict/prod_settings.py

 * Change for your name and mail:

        ADMINS = (
            # ('Your Name', 'your_email@example.com'),
            ('Lavilotte-Rolle Frédéric', 'pro@lavilotte-rolle.fr'),
        )

 * Change default from email:

        DEFAULT_FROM_EMAIL = 'pro@lavilotte-rolle.fr'

* Change `PASSWORD` for database, `NAME` and `USER` too if needed:

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': 'pinpict',
                # The following settings are not used with sqlite3:
                'USER': 'pinpict',
                'PASSWORD': 'my_wonderful_db_password',
                'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
                'PORT': '',                      # Set to empty string for default.
            }
        }


 * Change `SECRET_KEY` for a new strong one:

        # Make this unique, and don't share it with anybody.
        SECRET_KEY = '#v04u18pw)rsgry7fhw*7)t0^)nm!l6fod90fb7y8ckbu0u8yx'

 * Change `ALLOWED_HOSTS` for your own domains:

        ALLOWED_HOSTS = ['pinpict.com', 'www.pinpict.com']

 * You can also change `TIME_ZONE` and `LANGUAGE_CODE` if necessary.

 * Edit `phiroom/local_settings.py` :

        $ vim phiroom/local_settings.py

 * Change it's content for :

        #from pinpict.devel_settings import *
        from pinpict.prod_settings import *


 * Now create tables:
        
        $ pip3 install psycopg2
        $ python3 manage.py syncdb

 * Answer questions to create a superuser.


* Launch development server:

    $ python3 manage.py runserver <my_domain.com>:8000

You should be able to access to it from http://my_domain.com:8000 in your favorite browser.
Use ctrl + c to quit when you're done.


#### Set up gunicorn ####

Run as `<user>`:
    
    $ pip3 install gunicorn

You can test it running:

    $ gunicorn pinpict.wsgi:application --bind my_domain.com:8001

You should be able to access to it from http://my_domain.com:8001 in your favorite browser.
Use ctrl + c to quit when you're done.


Create a shell script to launch gunicorn with some parameters:

    $ vim /var/www/pinpict_env/bin/gunicorn_start

 * Complete it as follow:

    #!/bin/bash
    NAME="pinpict"                            # Name of the application
    DJANGODIR=/var/www/pinpict_env/pinpict    # Django project directory
    SOCKFILE=/var/www/pinpict_env/run/gunicorn.sock  # we will communicte using this unix socket
    USER=<my_user>                            # the user to run as
    GROUP=<my_group>                          # the group to run as
    NUM_WORKERS=3                             # how many worker processes should Gunicorn spawn
    DJANGO_SETTINGS_MODULE=pinpict.settings   # which settings file should Django use
    DJANGO_WSGI_MODULE=pinpict.wsgi           # WSGI module name

    echo "Starting $NAME as `whoami`"

    # Activate the virtual environment
    cd $DJANGODIR
    source ../bin/activate
    export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
    export PYTHONPATH=$DJANGODIR:$PYTHONPATH

    # Create the run directory if it doesn't exist
    RUNDIR=$(dirname $SOCKFILE)
    test -d $RUNDIR || mkdir -p $RUNDIR

    # Start your Django Unicorn
    # Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
    exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
        --name $NAME \
        --workers $NUM_WORKERS \
        --user=$USER --group=$GROUP \
        --bind=unix:$SOCKFILE \
        --log-level=debug \
        --log-file=-

    ## this script comes from: http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/

 * Give execution rights to our script:

    # chmod u+x /var/www/pinpict_env/bin/gunicorn_start


#### Set up supervisor ####

Run as root:

    # aptitude install supervisor

 * Create configuration file:

    # vim /etc/supervisor/conf.d/pinpict.conf

 * Complete it as follow:

    [program:pinpict]
    command = /var/www/pinpict_env/bin/gunicorn_start
    user = <my_user>
    autostart = true
    autorestart = true
    stdout_logfile = /var/www/pinpict_env/bin/gunicorn-supervisor.log
    redirect_stderr = true


 * Edit configuration file:

    # vim /etc/supervisor/supervisord.conf

 * Add or change these lines (according to your locale):

    [supervisord]
    environment = LANG=fr_FR.UTF-8, LC_ALL=fr_FR.UTF-8, LC_LANG=fr_FR.UTF-8

 * Relaunch supervisor:

    # supervisorctl reread
    # supervisorctl update

 * Now you can manage supervisor with following commands:

    # supervisorctl status pinpict
    # supervisorctl stop pinpict
    # supervisorctl start pinpict
    # supervisorctl restart pinpict



#### Set up nginx ####

Run as root

    # aptitude install nginx

 * Create new nginx configuration file:

    # vim /etc/nginx/sites-available/pinpict

 * Complete it as follow:

    upstream pinpict_app_server {
        # fail_timeout=0 means we always retry an upstream even if it failed
        # to return a good HTTP response (in case the Unicorn master nukes a
        # single worker for timing out).

        server unix:/var/www/pinpict_env/run/gunicorn.sock fail_timeout=0;

    }


    server {
        listen 80;
        server_name pinpict.com;
        
        client_max_body_size 1G;
        
        access_log /var/log/nginx/pinpict-access.log;
        error_log /var/log/nginx/pinpict-error.log;
        
        location /static/ {
            alias /var/www/pinpict_env/pinpict/pinpict/assets-root/;
        }   
        
        location /media/ {
            alias /var/www/sites/pinpict_env/pinpict/pinpict/data/;
        }   
        
     
        location / {
            # an HTTP header important enough to have its own Wikipedia entry:
            #   http://en.wikipedia.org/wiki/X-Forwarded-For
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     
            # enable this if and only if you use HTTPS, this helps Rack
            # set the proper protocol for doing redirects:
            # proxy_set_header X-Forwarded-Proto https;
     
            # pass the Host: header from the client right along so redirects
            # can be set properly within the Rack application
            proxy_set_header Host $http_host;
     
            # to avoid timeout when processing pictures:
            proxy_read_timeout 300000;
     
            # we don't want nginx trying to do something clever with
            # redirects, we set the Host: header above already.
            proxy_redirect off;
     
            # set "proxy_buffering off" *only* for Rainbows! when doing
            # Comet/long-poll stuff.  It's also safe to set if you're
            # using only serving fast clients with Unicorn + nginx.
            # Otherwise you _want_ nginx to buffer responses to slow
            # clients, really.
            # proxy_buffering off;
     
            # Try to serve static files from nginx, no point in making an
            # *application* server like Unicorn/Rainbows! serve static files.
            if (!-f $request_filename) {
                proxy_pass http://pinpict_app_server;
                break;
            }
        }
    }


 * Enable new configuration file:

    # ln -s /etc/nginx/sites-available/pinpict /etc/nginx/sites-enabled/pinpict

 * Restart nginx:

    # /etc/init.d/nginx restart

Open http://pinpict.com (replacing `pinpict.com` by your domain, here and in each configuration files) in your favorite browser.



#### To set up search engine ####

    $ python3 manage.py rebuild_index

By default index get update at each Pin model save or delete.
To set up a Timelaps between updates:

 * comment this line in your `pinpict/prod_settings.py`

    HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

 * Add a cron job as often as you want :
    
    $ python3 manage.py update_index

#### To get static files ####

    $ python3 manage.py collectstatic
