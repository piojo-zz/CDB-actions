import os
import sys
import re

def field_from_dictionary_list(field):
    '''Decorates a function that returns a list of complex data
    structures (tipically dictionaries), to iterate only over its
    interesting values.'''
    def wrap(f):
        def extract_field_from_f(*args, **kw):
            for i in f(*args, **kw):
                yield i[field]
        return extract_field_from_f
    return wrap

RX = re.compile('[,\s]+')

def words_to_args(f):
    def run(args):
        l = RX.split(args)
        return f(*l)
    return run
