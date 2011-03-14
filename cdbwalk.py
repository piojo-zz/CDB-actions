#!/usr/bin/python
# -*- encode: utf-8 -*-
'''Script that walks over a CDB Pan checkout, performs actions on
templates that declare them, and commits any changes, if needed.

TODO:

- Configure which actions map to which headers without modifying the
  code.

Author: Luis Fernando Muñoz Mejías
'''
import sys
import os
from pan_file import pan_file
from optparse import OptionParser

def init_actions():
    '''Initialises the dictionary of actions'''
    d = dict()

def do_commit(*arg):
    pass

if __name__ == '__main__':
    o = OptionParser()
    o.add_option("-d", "--dir", dest="top",
                 help="Top level of the CDB checkout")
    o.add_option("-e", "--extension", dest="extension"
                 help="Extension of the Pan templates (defaults to %default)",
                 default=".tpl")
    (opts, args) = o.parse_args()
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
                    p = pan_file(fullpath, **actions)
                    p.processs()
                    if p.write_file():
                        changed.append(fullpath)
                except pan_exception, e:
                    print e
        do_commit(changed)
    
