import posixpath
import sys
import urllib
from django.conf import settings
from django.contrib.staticfiles import finders
from django.utils.functional import LazyObject


class LazyStorage(LazyObject):
    def _setup(self):
        self._wrapped = import_string(settings.SHRINK_STORAGE)()
storage = LazyStorage()


def handle_extensions(extensions=('html',)):
    """
    organizes multiple extensions that are separated with commas or passed by
    using --extension/-e multiple times.

    for example: running 'django-admin makemessages -e js,txt -e xhtml -a'
    would result in a extension list: ['.js', '.txt', '.xhtml']

    >>> handle_extensions(['.html', 'html,js,py,py,py,.py', 'py,.py'])
    ['.html', '.js']
    >>> handle_extensions(['.html, txt,.tpl'])
    ['.html', '.tpl', '.txt']
    """
    ext_list = []
    for ext in extensions:
        ext_list.extend(ext.replace(' ','').split(','))
    for i, ext in enumerate(ext_list):
        if not ext.startswith('.'):
            ext_list[i] = '.%s' % ext_list[i]
    return set(ext_list)


def find_static(path):
    normalized_path = posixpath.normpath(urllib.unquote(path)).lstrip('/')
    absolute_path = finders.find(normalized_path)
    if absolute_path:
        return absolute_path.decode(settings.FILE_CHARSET)


def import_string(dot_name):
    """
    Imports an object based on a string.

    :param dot_name: the dot_name name for the object to import.
    :return: imported object
    """
    # force the import dot_name to automatically convert to strings
    if isinstance(dot_name, unicode):
        dot_name = str(dot_name)
    if '.' in dot_name:
        mod_name, attr = dot_name.rsplit('.', 1)
    else:
        return __import__(dot_name)
    # __import__ is not able to handle unicode strings in the fromlist if the
    # mod_name is a package
    if isinstance(attr, unicode):
        attr = attr.encode('utf-8')
    try:
        return getattr(__import__(mod_name, None, None, [attr]), attr)
    except (ImportError, AttributeError):
        # support importing mod_names not yet set up by the parent mod_name (or
        # package for that matter)
        mod_name = '%s.%s' % (mod_name, attr)
        try:
            __import__(mod_name)
        except ImportError, e:
            raise ImportError('Failed to import %s: %s' % (mod_name, e))
        return sys.mod_names[mod_name]

