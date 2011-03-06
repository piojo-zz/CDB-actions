import os
import sys
import re

class pan_file(object):
    '''Pan file to be automatically regenerated'''
    tpl_name_re = re.compile('^\w*\s*template\s+([-\w]+)\s*;$')
    act_re = re.compile('^@{\s*(\S+)\s*=\s*(.*)}$')
    def __init__(self, filename, **actions)
        '''Class constructor. Takes the name of the Pan file to open,
        and the a dictionary with the actions registered to each
        possible header.'''
        self.file = open("filename", "r+")
        self.actions = actions
        self.body = []

    def __iter__(self):
        '''The object iterates over its header.'''
        self.file.seek(0,os.SEEK_SET)
        return self

    def next(self):
        if not self.open:
            raise StopIteration
        for i in self.file:
            m = self.tpl_name_re.match(i)
            if m:
                self.open = False
                return (m.group(1), )
            m = self.act_re.match(i)
            if m:
                return m.group(1), m.group(2)
        self.open = False
        raise StopIteration

    def process(self):
        '''Processes the header of a Pan file, performing any
        registered actions'''
        for (action, args) in self:
            if args:
                try:
                    self.body.extend(self.actions[action](*args))
                except KeyError, e:
                    pass
            else:
                break

    def write_file(self):
        if not self.body:
            return False
        pos = self.file.tell()
        new = '\n'.join(self.body)
        old = ''.join(self.file)
        if new == old:
            return False
        self.file.seek(pos, os.SEEK_SET)
        self.file.truncate()
        self.file.write(new)
        self.file.close()
        return True
