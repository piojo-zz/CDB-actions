'''Module querying LDAP for e-group combinations'''

import os
import sys

def egroup_filter_generator(*egroups, **params):
    '''Generates an LDAP filter string for the list of egroups
    given. It accepts an optional parameter, specifying whether the
    query should recurse over nested e-groups or not.'''
    if params.get('recursive'):
        rs = ':1.2.840.113556.1.4.1941:'
    else:
        rs = ''
    q = []
    for i in egroups:
        entry='memberOf%s=CN=%s,OU=e-groups,OU=Workgroups,DC=cern,DC=ch' % (
            rs, i)
        q.append(entry)
    return q

def egroup_filter_combiner(**kwargs):
    included = []
    excluded = []
    if kwargs.has_key('include'):
        l = egroup_filter_generator(kwargs['include'])
        included.extend(l)
    if kwargs.has_key('recursive-include'):
        l = egroup_filter_generator(kwargs['recursive-include'], recursive=True)
        include.extend(l)

    if kwargs.has_key('exclude'):
        l = egroup_filter_generator(kwargs['exclude'])
        excluded.extend(l)
    if kwargs.has_key('recursive-exclude'):
        l = egroup_filter_generator(kwargs['recursive-exclude'], recursive=True)
        excluded.extend(l)

    fl = '&(|%s)(!(|%s))' % ( ''.join(['(%s)' % (i) for i in included]),
                              ''.join(['(%s)' % (i) for i in excluded]))
    return fl
