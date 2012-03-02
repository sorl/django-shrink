import os
from django.conf import settings
from django.contrib.staticfiles.management.commands.collectstatic import Command as CollectStaticCommand
from django.template.loader import get_template
from shrink.helpers import import_string, handle_extensions
from shrink.base import StyleShrink, ScriptShrink
from shrink.templatetags.shrink import ScriptNode, StyleNode
from optparse import make_option
from os.path import isdir, splitext, join as pjoin


def rshrink(node, t):
    """
    Recursive fun
    """
    if isinstance(node, ScriptNode):
        shrink = ScriptShrink(node, t.name)
        shrink.update()
    elif isinstance(node, StyleNode):
        shrink = StyleShrink(node, t.name)
        shrink.update()
    if hasattr(node, 'nodelist'):
        for n in node.nodelist:
            rshrink(n, t)


class Command(CollectStaticCommand):
    help = (
        "Collect static files from apps and other locations in a single"
        "location.\nShrinks javascripts and css defined in templates."
        )

    @property
    def option_list(self):
        opt_list = []
        for opt in CollectStaticCommand.option_list:
            if opt.get_opt_string() == '--noinput':
                opt.default = False
            opt_list.append(opt)
        opt_list.extend([
            make_option('--extension', '-e', dest='extensions', default=['html'],
                help=(
                    'The file extension(s) to examine for scripts and css '
                    '(default: ".html", separate multiple extensions with commas, '
                    'or use -e multiple times)'
                    ),
                action='append'),
            make_option('--noshrink', action='store_false', dest='shrink',
                default=True, help="Do NOT shrink scripts or css."),
        ])
        return opt_list

    def handle_noargs(self,  **options):
        super(Command, self).handle_noargs(**options)
        if not options.get('shrink'):
            return
        extensions = handle_extensions(options['extensions'])
        templates = set()
        for loader_dot in settings.TEMPLATE_LOADERS:
            loader = import_string(loader_dot)()
            if hasattr(loader, 'get_template_sources'):
                for template_dir in loader.get_template_sources(''):
                    if isdir(template_dir):
                        for (dirpath, dirnames, filenames) in os.walk(template_dir):
                            for f in filenames:
                                if splitext(f)[1] in extensions:
                                    templates.add(get_template(pjoin(dirpath, f)))
        for t in templates:
            rshrink(t, t)

