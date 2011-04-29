import datetime
import os
import tempfile
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.encoding import smart_str
from os.path import isdir, getmtime, dirname
from scss import Scss
from shrink.helpers import storage
from subprocess import Popen, PIPE
from tempfile import mkstemp


class Shrink(object):
    already_treated = ''

    def __init__(self, node, template):
        self.node = node
        self.template = template
        self.absolute_paths = self.node.get_paths(absolute=True)

    def therapy(self):
        raise NotImplemented

    def update(self):
        latest = sorted(self.absolute_paths, key=getmtime, reverse=True)[0]
        if (
            not storage.exists(self.node.destination) or
            storage.modified_time(self.node.destination) <
            datetime.datetime.fromtimestamp(getmtime(latest))
            ):
            if storage.exists(self.node.destination):
                storage.delete(self.node.destination) # or else we get next available name
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
        handle, out = mkstemp()
        args.append('--js_output_file=%s' % out) # for some reason stdout stalls
        args = map(smart_str, args)
        print ('Compiling scripts in `%s` to `%s`' %
            (self.template, self.node.destination))
        p = Popen(args, stdout=PIPE)
        p.wait()
        with open(out, 'r') as fp:
            storage.save(self.node.destination, ContentFile(fp.read()))
        os.close(handle)
        os.remove(out)


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
        handle, tmp = tempfile.mkstemp()
        with open(tmp, 'w') as fp:
            fp.write('\n'.join(css))
        args = ['java', '-jar', settings.SHRINK_YUI_COMPRESSOR,
                '--type', 'css', tmp]
        args = map(smart_str, args)
        print ('Compressing (s)css in `%s` to `%s`' %
            (self.template, self.node.destination))
        p = Popen(args, stdout=PIPE)
        p.wait()
        storage.save(self.node.destination, ContentFile(p.stdout.read()))
        os.close(handle)
        os.remove(tmp)

