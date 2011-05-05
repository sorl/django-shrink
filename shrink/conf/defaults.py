import os
from os.path import abspath, dirname, join as pjoin
from django.conf import settings


here = abspath(dirname(__file__))
shrinks = pjoin(here, os.pardir, 'shrinks')


SHRINK_TIMESTAMP = True

SHRINK_STORAGE = settings.STATICFILES_STORAGE

SHRINK_CLOSURE_COMPILER = pjoin(shrinks, 'cc', 'compiler.jar')

SHRINK_CLOSURE_COMPILER_COMPILATION_LEVEL = 'SIMPLE_OPTIMIZATIONS'

SHRINK_YUI_COMPRESSOR = pjoin(shrinks, 'yui', 'yuicompressor-2.4.6.jar')

