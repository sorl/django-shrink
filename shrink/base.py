import datetime
import os
import tempfile
from django.conf import settings
from shrink.helpers import storage
from os.path import isdir, getmtime, dirname
from scss import Scss
from subprocess import Popen


class Shrink(object):
    already_treated = ''

    def __init__(self, node):
        self.node = node
        self.template = node.source[0].name
        self.absolute_paths = self.node.get_paths(absolute=True)
        self.destination_path = storage.path(self.node.destination_name)

    def therapy(self):
        raise NotImplemented

    def update(self):
        latest = sorted(self.absolute_paths, key=getmtime, reverse=True)[0]
        if (
            not storage.exists(self.node.destination_name) or
            storage.modified_time(self.node.destination_name) <
            datetime.datetime.fromtimestamp(getmtime(latest))
            ):
            dest_dir = dirname(self.destination_path)
            if not isdir(dest_dir):
                os.makedirs(dest_dir)
            self.therapy()
        else:
            print self.already_treated


class ScriptCompiler(Shrink):
    already_treated = 'Scripts:\tup-to-date.'

    def therapy(self):
        args = ['java', '-jar', settings.SHRINK_CLOSURE_COMPILER,
                '--compilation_level',
                settings.SHRINK_CLOSURE_COMPILER_COMPILATION_LEVEL]
        for absolute_path in self.absolute_paths:
            args.append('--js=%s' % absolute_path)
        args.append('--js_output_file=%s' % self.destination_path)
        print ('Compiling scripts in `%s` to `%s`' %
            (self.template, self.destination_path))
        p = Popen(args)
        p.wait()


class StyleCompressor(Shrink):
    already_treated = '(s)css files:\tup-to-date.'

    def therapy(self):
        css = []
        parser = Scss()
        for absolute_path in self.absolute_paths:
            with open(absolute_path, 'r') as fp:
                if absolute_path.endswith('.scss'):
                    css.append(parser.compile(fp.read()))
                else:
                    css.append(fp.read())
        tmp = tempfile.mkstemp()[1]
        with open(tmp, 'w') as fp:
            fp.write('\n'.join(css))
        args = ['java', '-jar', settings.SHRINK_YUI_COMPRESSOR,
                '--type', 'css', '-o', self.destination_path, tmp]
        print ('Compressing (s)css in `%s` to `%s`' %
            (self.template, self.destination_path))
        p = Popen(args)
        p.wait()
        os.remove(tmp)

