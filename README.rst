Django Dashboard App
============

A reusable Django app for displaying a dashboard with a fluid grid of widgets.

Installation
------------

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

Before your tags/filters are available in your templates, load them by using

.. code-block:: html

	{% load dashboard_app_tags %}


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
