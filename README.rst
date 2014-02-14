Django Dashboard App
====================

A reusable Django app for displaying a dashboard with a fluid grid of widgets.

Let's say you control 20 different web apps and you want to have a dashboard
that shows the user count of each app as a graph. The graphs should be updated
every minute so that you can see immediately when a sudden spike of new user
signups happens.

There are two ways:

1. Your apps provide an API endpoint for your dashboard so that the dashboard
   can poll that endpoint every minute and get the current user count.
2. Your dashboard provides an endpoint that can be called by your apps whenever
   a new user signs up.

Both methods should be possible with this app.

The dashboard itself will consist of many plugins. Each plugin is a reusable
Django app of it's own. This allows you to write any kind of plugin for any
kind of service.

Note: A while ago I already created
https://github.com/bitmazk/django-metrics-dashboard to solve this exact problem
but I wanted to have socket.io support, which was a bad idea. It didn't really
work out nicely and kept crashing so that I abandoned the project in the end.
This is my second try, this time I'm using old-school polling once per minute
via AJAX.


Installation
============

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-dashboard-app

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/bitmazk/django-dashboard-app.git#egg=dashboard_app

TODO: Describe further installation steps (edit / remove the examples below):

Add ``dashboard_app`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'dashboard_app',
    )

Add the ``dashboard_app`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^dashboard/', include('dashboard_app.urls')),
    )

Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate dashboard_app


Usage
-----

TODO: Describe usage or point to docs. Also describe available settings and
templatetags.


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-dashboard-app
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch
