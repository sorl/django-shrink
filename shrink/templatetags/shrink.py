import re
from ..conf import settings
from ..helpers import storage, find_static
from django.forms.widgets import flatatt
from django.utils.datastructures import SortedDict
from django.template import Library, Node, TemplateSyntaxError


register = Library()
kw_pat = re.compile(r'^(?P<key>[\w]+)=(?P<value>.+)$')


class ShrinkNode(Node):
    error_message = ''
    endtag = ''
    template = ''

    def __init__(self, parser, token):
        bits = token.split_contents()
        if len(bits) < 2:
            raise TemplateSyntaxError(self.error_message)
        self.destination = bits[1].strip('\'"')
        attrs = SortedDict()
        for bit in bits[2:]:
            m = kw_pat.match(bit)
            if not m:
                raise TemplateSyntaxError(self.error_message)
            attrs[m.group('key')] = m.group('value')
        self.attrs = flatatt(attrs)
        self.nodelist = parser.parse((self.endtag,))
        parser.delete_first_token()

    def get_prefix(self, path):
        return settings.STATIC_URL

    def get_paths(self, context={}, absolute=False):
        block = self.nodelist.render(context)
        paths = []
        for path in block.replace('\r\n', '\n').split('\n'):
            path = path.strip()
            if path and absolute:
                path = find_static(path)
            if path and path not in paths:
                paths.append(path)
        return paths

    def render(self, context):
        if settings.DEBUG:
            tags = []
            for path in self.get_paths(context):
                tag = self.template.format(prefix=self.get_prefix(path),
                    path=path, attrs=self.attrs)
                tags.append(tag)
            return '\n'.join(tags)
        else:
            path = storage.url(self.destination)
            if settings.SHRINK_TIMESTAMP:
                try:
                    timetamp = storage.modified_time(
                        self.destination).isoformat()
                    path = '%s?%s' % (path, timetamp)
                except Exception:
                    pass
            return self.template.format(prefix='', path=path, attrs=self.attrs)


@register.tag('scripts')
class ScriptNode(ShrinkNode):
    error_message = 'Usage: scripts destination [keyword arguments]'
    endtag = 'endscripts'
    template = '<script src="{prefix}{path}"{attrs}></script>'

    def __repr__(self):
        return '<ScriptNode>'


@register.tag('styles')
class StyleNode(ShrinkNode):
    error_message = 'Usage: styles destination [keyword arguments]'
    endtag = 'endstyles'
    template = '<link rel="stylesheet" href="{prefix}{path}"{attrs}>'

    def __repr__(self):
        return '<StyleNode>'

