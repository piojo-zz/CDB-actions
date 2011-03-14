'''Module querying LDAP for e-group combinations'''
import sys
import os
import re
from pan_file import pan_exception, wrap_in_variable
from egroup_filter_generator import egroup_querier

def egroup_string_to_ldap_query(string):
    rx = re.compile("(\w+)=(\S+)")
    d = dict()
    var_name = []
    for i in string.split(' '):
        m = rx.match(i)
        if not m:
            raise pan_exception("Misconfigured egroup generator: " + i)
        d[m.group(1)] = m.group(2).split(',')
        var_name.extend(d[m.group(1)])

    var_name = ''.join(var_name)
    @wrap_in_variable(var_name)
    def f():
        egroup_querier(**d)

    return f()
