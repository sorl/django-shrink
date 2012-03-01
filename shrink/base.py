import datetime
import os
from django.core.files.base import ContentFile
from os.path import getmtime
from shrink.helpers import storage
from slimmer import css_slimmer
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
        paths = sorted(self.absolute_paths, key=getmtime, reverse=True)
        if not paths:
            return
        if (
            not storage.exists(self.node.destination) or
            storage.modified_time(self.node.destination) <
            datetime.datetime.fromtimestamp(getmtime(paths[0]))
            ):
            if storage.exists(self.node.destination):
                storage.delete(self.node.destination) # or else we get next available name
            self.therapy()
        else:
            print self.already_treated


class ScriptShrink(Shrink):
    already_treated = 'Scripts:\tup-to-date.'

    def therapy(self):
        a_handle, a = mkstemp()
        b_handle, b = mkstemp()
        with open(a, 'wb') as a_fp:
            for fn in self.absolute_paths:
                with open(fn, 'r') as fp:
                    a_fp.write(fp.read())
                    a_fp.write(';')
        p = Popen(['uglifyjs', '-o', b, a], stdout=PIPE)
        p.wait()
        with open(b, 'r') as b_fp:
            storage.save(self.node.destination, ContentFile(b_fp.read()))
        os.close(a_handle)
        os.close(b_handle)
        os.remove(a)
        os.remove(b)


class StyleShrink(Shrink):
    already_treated = 'ss files:\tup-to-date.'

    def therapy(self):
        css = []
        for fn in self.absolute_paths:
            with open(fn, 'r') as fp:
                css.append(fp.read())
        css = css_slimmer(''.join(css))
        storage.save(self.node.destination, ContentFile(css))

