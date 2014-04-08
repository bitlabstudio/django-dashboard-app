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

Ultimately, both methods should be possible with this app. Currently only the
first way is implemented.

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

Add ``dashboard_app`` and ``django.contrib.humanize`` to your
``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'django.contrib.humanize',
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

When you first visit the main URL for your dashboard, you will see an error
widget saying "No widgets found". This means we need to teach Django which
widgets to display.

In your Django project-app-folder (assuming Django >1.5 project layout) create
a ``dashboard_widgets.py`` file (you can put that file into any app folder that
is part of ``INSTALLED_APPS``).

Add the following code to that file:

.. code-block:: python

    """Widgets for the ACME project."""
    from dashboard_app.dashboard_widgets import DummyWidget
    from dashboard_app.widget_pool import dashboard_widget_pool


    dashboard_widget_pool.register_widget(DummyWidget, position=1)

When you call your main dashboard URL now, you should see the dummy widget
displaying the current date and time. The last update time resembles the time
when the widget did write data to the database last time. Since this widget
never writes any data, this time will always be the time when you first loaded
the widget under this name.

Build Your Widget
-----------------

First you need to decide where your widget code should live. If you are very
sure that your widgets will always be bound to the project and never be
released as open source or re-used in other projects of yours, you can
implement your widgets in the ``dashboard_widgets.py`` file that you have
created in your Django project-app already.

If you think that your widget will be usefull for many projects, you should
create it as a reusable app and therefore create a new app-folder. Let's
assume that your project is called ``ACME`` and you want to create a widget
to display the current user count. First create the following files:

.. code-block:: text

    -- dashboard_acme_users
    ---- __init__.py
    ---- models.py
    ---- dashboard_widgets.py

Your widget apps should always be named like ``dashboard_yourthing`` so that
it is easier to find them all on Google/Github. The ``__init__.py`` file will
turn the app into a Python module and the ``models.py`` file is needed to turn
the module into a potential Django app that can be discovered by the
``INSTALLED_APPS`` setting. The ``dashboard_widgets.py`` file is the file
where you will implement your custom widget.

Put the following code into that file:

.. code-block:: python

    """Widgets for the dashboard_acme_users app."""
    from dashboard_app.widget_base import DashboardWidgetBase

    from django.contrib.auth.models import User


    class UserCountWidget(DashboardWidgetBase):
        """Displays the total amount of users currently in the database."""
        template_name = 'dashboard_acme_users/widgets/user_count.html'

        def get_context_data(self):
            ctx = super(UserCountWidget, self).get_context_data()
            count = User.objects.all().count()
            ctx.update({'value': count, })
            return ctx

You basically just have to decide on a nice widget name (here:
``UserCountWidget``) and a template name. We suggest to put the widgets into
a subfolder called ``your_app_name/widgets`` and name the template after the
widget's class name (here: ``user_count.html``).

Now you want to display something. In our case it is the current user count.
Therefore we must override the ``get_context_data`` method and return the
current user count.

Now you need to register your new widget in the ``dashboard_widgets.py`` file
that you used earlier to register the DummyWidget:

.. code-block:: python

    """Widgets for the ACME project."""
    from dashboard_app.dashboard_widgets import DummyWidget
    from dashboard_app.widget_pool import dashboard_widget_pool

    from dashboard_acme_users import dashboard_widgets as widgets


    dashboard_widget_pool.register_widget(DummyWidget, position=1)
    dashboard_widget_pool.register_widget(widgets.UserCountWidget, position=2)

When you visit your main dashboard URL you should see two widgets now.

TODO: Describe how to save widget data to the database and render charts

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
