
django-shrink
=============
A js compiler & css minifier with sass compatibility


Requirements
------------
* Django 1.3+
* 2.6 <= Python <= 3
* ``django.contrib.staticfiles`` in ``INSTALLED_APPS``


Installation
------------
::

    pip install django-shrink


Configuration
-------------
::

    INSTALLED_APPS = (
        ...
        'django.contrib.staticfiles',
        ...
        'shrink',
        ...
    )

Optionally if you want to use `Sass`_ you need to add the comilation view to
your urls::

    # urls.py
    (r'^', include('shrink.urls')),

.. note::
    The compilation view is only avalailable when ``DEBUG = True``


Usage
-----
Define your javascripts and css files in your template as in this example::

    {% import shrink %}
    {% styles css/myproject-min.css %}
        css/reset.css
        css/forms.css
        css/myproject.scss
    {% endstyles %}
    {% scripts js/myproject-min.js %}
        js/jquery.js
        js/plugin.js
        js/myproject.js
    {% endscripts %}

When ``DEBUG = True`` this will end up as::

    <link rel="stylesheet" href="{{ STATIC_URL }}css/reset.css">
    <link rel="stylesheet" href="{{ STATIC_URL }}css/forms.css">
    <link rel="stylesheet" href="{{ SHRINK_SCSS_URL }}css/myproject.css">
    <script src="{{ STATIC_URL }}js/jquery.js"></script>
    <script src="{{ STATIC_URL }}js/plugin.js"></script>
    <script src="{{ STATIC_URL }}js/myproject.js"></script>

When ``DEBUG = False`` this will end up as::

    <link rel="stylesheet" href="{{ STATIC_URL }}css/myproject-min.css?timestamp">
    <script src="{{ STATIC_URL }}js/myproject-min.js?timestamp"></script>

When deploying you want to compile your javascripts, compile your scss (`Sass`_)
and compress the css files. django-shrink overrides the ``collectstatic``
management command and after collecting the static files it does the compiling
and compressing. Thus you need to execute the management command
``collectstatic`` in your deployment environment.


Settings
--------

SHRINK_SCSS_URL
^^^^^^^^^^^^^^^
What url path to be used as prefix for the scss compiler view.

* Default: ``'/scss/'``

SHRINK_TIMESTAMP
^^^^^^^^^^^^^^^^
Controls if you want to timestamp the compressed/compiled assets.

* Default: ``True``

SHRINK_STORAGE
^^^^^^^^^^^^^^
Storage for the compressed/compiled assets.

* Default: ``settings.STATICFILES_STORAGE``

SHRINK_CLOSURE_COMPILER
^^^^^^^^^^^^^^^^^^^^^^^
Path to Google Closure Compiler jar.

* Default: Google Closure Compiler jar provided.

SHRINK_CLOSURE_COMPILER_COMPILATION_LEVEL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Google Closure Compiler optimization level.

* Default: ``'SIMPLE_OPTIMIZATIONS'``

SHRINK_YUI_COMPRESSOR
^^^^^^^^^^^^^^^^^^^^^
Path to YUI Compressor

* Default: YUI compressor jar provided.


.. _Sass: http://sass-lang.com/

