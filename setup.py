# -*- encoding: utf-8 -*-
import os
import sys
from distutils.core import setup

version=open('.version').readline().strip()

setup(name='cdbwalk',
      version=version,
      py_modules=['cdb', 'egroup2pan', 'egroup_filter_generator',
                  '__init__', 'ldap_session', 'misc_utils', 'pan_file'],
      url='http://www.quattor.org',
      author='Luis Fernando Muñoz Mejías',
      author_email='lfmunozmejias@gmail.com'
      )
