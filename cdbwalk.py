#!/usr/bin/python
# -*- encoding: utf-8 -*-
'''Script that walks over a CDB Pan checkout, performs actions on
templates that declare them, and commits any changes, if needed.

TODO:

- Configure which actions map to which headers without modifying the
  code.

- Make it generic enough to work with CDB and SCDB  

Author: Luis Fernando Muñoz Mejías
'''
import sys
import os
from pan_file import pan_file, pan_exception
from optparse import OptionParser
import subprocess
from egroup2pan import egroup_string_to_pan_variable as egroup2pan
from cdb import cdb_error, do_commit
import yaml

def actions(filename):
    y = yaml.load(file(filename))
    d = dict()
    for header, action in y.items():
        try:
            m = sys.modules[action['module']]
        except KeyError:
            m = __import__(action['module'])
        d[header] = m.__dict__[action['callable']]
    return d

class log(object):
    '''Log object for displaying information'''
    def __init__(self, verbose=False):
        self.verbose = verbose
    def __call__(self, *kwargs):
        if self.verbose:
            print ' '.join(kwargs)


if __name__ == '__main__':
    o = OptionParser()
    o.add_option("-d", "--dir", dest="top",
                 help="Top level of the CDB checkout")
    o.add_option("-e", "--extension", dest="extension",
                 help="Extension of the Pan templates (defaults to %default)",
                 default=".tpl")
    o.add_option("-c", "--commit", dest="commit",
                 help="Commit to CDB any changes",
                 action="store_true")
    o.add_option("-v", "--verbose", dest="verbose",
                 help="Verbose",
                 action="store_true")
    (opts, args) = o.parse_args()
    lg = log(opts.verbose)
    changed = []
    actions = init_actions()
    for root, dirs, files in os.walk(opts.top):
        for rm in 'CVS', '.svn', '.git':
            if rm in dirs:
                dirs.remove(rm)
        for f in files:
            if f.endswith(opts.extension):
                try:
                    fullpath = os.path.join(root, f)
                    lg("Processing template:", fullpath)
                    p = pan_file(fullpath, **actions)
                    p.process()
                    if p.write_file():
                        lg("Modified:", fullpath)
                        changed.append(fullpath)
                except pan_exception, e:
                    print e
    if changed and opts.commit:
        do_commit(*changed)
