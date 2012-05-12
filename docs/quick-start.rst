Getting Started
====================================

Below are the basic steps need to get django-ad-code integrated into your
Django project.


Installation
------------------------------------

It is easiest to install django-ad-code from PyPi using pip::

    pip install django-ad-code


Configure Settings
------------------------------------

You need to include ``adcode`` to your installed apps as well as include a
context processor in your project settings.

.. code-block:: python

    INSTALLED_APPS = (
        # Other installed apps would go here
        'adcode',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        # Other context processors would go here
        'adcode.context_processors.current_placements',
    )

Note that ``TEMPLATE_CONTEXT_PROCESSORS`` is not included in the default settings
created by ``startproject``. You should take care to ensure that the default
context processors are included in this list. For a list of default
``TEMPLATE_CONTEXT_PROCESSORS`` please see 
`the official Django docs <https://docs.djangoproject.com/en/1.3/ref/settings/#template-context-processors>`_.

For the context processor to have any effect you need to make sure that the template
is rendered using a RequestContext. This is done for you with the
`render <https://docs.djangoproject.com/en/1.4/topics/http/shortcuts/#render>`_ shortcut.


Create Database Tables
------------------------------------

You'll need to create the necessary database tables for storing ad sections and
placements. This is done with the ``syncdb`` management command built into Django::

    python manage.py syncdb

django-ad-code uses `South <http://south.aeracode.org/>`_ to handle database migrations. 
If you are also using South then you should run ``migrate`` instead::

    python manage.py migrate adcode


Using Ad Data in the Template
------------------------------------

The django-ad-code includes two template tags to help rendering ad placements.
``render_section_header`` would be included in your html <head> and would include
and step JS needed. In your <body> you would render individual placements with
``render_placement`` which takes the slug for the placement.

    .. code-block:: html

    {% load adcode_tags %}
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <!-- Other meta, css, js -->
        {% render_section_header %}
    </head>
    <body>
        <!-- Various body content -->
        {% render_placement 'footer' %}
    </body>
    </html>

Continue on to learn about customizing how these tags render and how to use
django-ad-code with a few common providers.

