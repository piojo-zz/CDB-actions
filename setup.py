# -*- encoding: utf-8 -*-
import os
import sys
from distutils.core import setup
from glob import glob

version=open('.version').readline().strip()

setup(name='cdbwalk',
      version=version,
      py_modules=[x[:-3] for x in glob('*.py')],
      url='http://www.quattor.org',
      author='Luis Fernando Muñoz Mejías',
      author_email='lfmunozmejias@gmail.com',
      scripts=['cdbwalk.py'],
      data_files=[('/etc', glob('*.yaml'))],
      license='Apache2'
      )
