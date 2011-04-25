from django.core.cache import cache
from django.http import HttpResponse, Http404
from os.path import getmtime
from scss import Scss
from shrink.helpers import find_static


SCSS_CACHE_TIMEOUT = 3600


def scss(request, path):
    absolute_path = find_static(path)
    if not absolute_path:
        raise Http404("'%s' could not be found" % path)
    mtime = getmtime(absolute_path)
    cached = cache.get(path)
    if not cached or mtime > cached['mtime']:
        parser = Scss()
        with open(absolute_path, 'r') as fp:
            css = parser.compile(fp.read())
        response = HttpResponse(css, mimetype='text/css')
        cache.set(path, {
            'response': response,
            'mtime': mtime,
            }, SCSS_CACHE_TIMEOUT)
        return response
    return cached['response']

