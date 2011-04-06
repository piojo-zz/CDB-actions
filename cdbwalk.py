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

class cdb_error(Exception):
    '''Exception for errors dealing with CDB'''
    def __init__(self, descro, process):
        self.msg = descro
        self.process = process

    def __str__(self):
        lines = [self.msg, "\nStandard output:\n"]
        lines.extend(l for l in self.process.stdout)
        lines.append("\nStandard error:\n")
        lines.extend(l for l in self.process.stderr)
        return "".join(lines)

class log(object):
    '''Log object for displaying information'''
    def __init__(self, verbose=False):
        self.verbose = verbose
    def __call__(self, *kwargs):
        if self.verbose:
            print ' '.join(kwargs)

def init_actions():
    '''Initialises the dictionary of actions'''
    d = {"egroups" : egroup2pan}
    return d

def do_commit(*arg):
    '''Commits the modified templates to CDB'''
    cdbcmd = ('update ' + ' '.join(arg) +
              '; commit -c "Upgrade templates that come from external sources')
    cdbcall = [ 'cdbop', '--server', 'cdbserv', '--cfgfile', '/dev/fd/0',
                '--command',  cdbcmd]

    p = subprocess.Popen(cdbcall, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    if not os.environ.has_key('CDB_USER'):
        p.stdin.write('use-krb5=1\n')
    p.stdin.close()
    if p.wait() != 0:
        raise cdb_error("Failed to commit to CDB", p)

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
