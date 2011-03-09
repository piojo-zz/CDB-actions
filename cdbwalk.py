#!/usr/bin/python
'''Script that walks over a CDB Pan graph and commits any changes, if
needed.

TODO:

- Configure which actions map to which headers without modifying the
  code.
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
                 help="Top level of the CDB checkout",
                 "-e", "--extension", dest="extension"
                 help="Extension of the Pan templates (defaults to %default)",
                 default=".tpl")
    (opts, args) = o.parse_args()
    changed = False
    actions = init_actions()
    for root, dirs, files in os.walk(opts.top):
        print "root", root
        for rm in 'CVS', '.svn', '.git':
            if rm in dirs:
                dirs.remove(rm)
        for f in files:
            if f.endswith(opts.extension):
                p = pan_file(os.path.join(root, f), **actions)
                p.processs()
                if p.write_file():
                    changed = True
    if changed:
        do_commit(blah)
    
