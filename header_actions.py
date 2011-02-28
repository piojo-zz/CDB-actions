import os
import sys
import re

class pan_file_header(object):
    '''Iterable object, able to return each of the special tags, and
    their parameters.'''
    tpl_name_re = re.compile('^\w*\s*template\s+([-\w]+)\s*;$')
    act_re = re.compile('^@{\s*(\S+)\s*=\s*(.*)}$')

    def __init__(self, f):
        self.file = f

    def __iter__(self):
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

class pan_file(object):
    '''Pan file to be automatically regenerated'''
    def __init__(self, filename, **actions)
        '''Class constructor. Takes the name of the Pan file to open,
        and the a dictionary with the actions registered to each
        possible header.'''
        self.file = open("filename", "r+")
        self.actions = actions

    def preprocess(self):
        header = pan_file_header(self.filename)
        for act, arg in header:
            if self.actions.has_key(act):
                self.actions[act].preprocess(args)

    def process(self):

        self.file.truncate()

        contents = [x.process() for x in self.actions.itervalues()]
        self.file.write('\n'.join(contents))
        self.file.close()

    def postprocess(self):
        for i in self.actionsitervalues():
            i.postprocess()
