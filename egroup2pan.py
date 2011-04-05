# -*- encoding: utf-8 -*-
'''Module querying LDAP for e-group combinations and producing a Pan
variable.

Author: Luis Fernando Muñoz Mejías
'''
import sys
import os
import re
from pan_file import pan_exception, wrap_in_variable
from egroup_filter_generator import egroup_querier

RX = re.compile("(\w+)\s*=\s*(\S+)")
MAX_VAR_LENGTH = 30
SUBST = re.compile("\W+")

def egroups_in_string(string):
    '''Returns a dictionary with the e-groups included (or excluded)
    from the in the argument string.'''
    d = dict()
    for i in string.split(' '):
        m = RX.match(i)
        if not m:
            raise pan_exception("Misconfigured egroup generator: " + i)
        d[m.group(1)] = m.group(2).split(',')

    return d

def var_name(**kwargs):
    '''Returns a PAN variable name from the egroups passed as
    arguments. This name is the set of egroups in the dictionary,
    joined by '_', in uppercase, and with all non-word characters
    turned into '_'. The resulting identifir is trimmed to
    MAX_VAR_LENGHT characters'''
    l = []
    for x in kwargs.values():
        l.extend(x)
    l.sort()
    var = '_'.join(l)
    var = var[:MAX_VAR_LENGTH]
    var = var.upper()
    return SUBST.sub("_", var)

def egroup_string_to_pan_variable(line):
    '''Returns a string representing a Pan variable with the contents
    of the egroups included (or excluded) in the line given as an
    argument.'''
    actions = egroups_in_string(line)
    @wrap_in_variable(var_name(**actions))
    def f():
        rs, members = egroup_querier(**actions)
        return [ x[1]['sAMAccountName'][0] for x in members]
    return f()
