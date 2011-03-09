'''Module querying LDAP for e-group combinations'''

import os
import sys

from ldap_session import ldap_session

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
    '''Creates a single filter string for querying for the members of a
list of e-groups, excepting if they are in a list of excluded
e-groups. Arguments:

include: e-groups to include in the LDAP search
exclude: e-groups whose members should not be returned in this search
recursive_include: e-groups to include in the LDAP search, recursively
recursive_exclude: e-groups whose members (or members of members)
should not be returned in this search'''
    included = []
    excluded = []

    for arg, recurse, dst_list in zip('include recursive_include exclude recursive_exclude'.split(' '),
                                      [False, True, False, True],
                                      [included, included, excluded, excluded]):
        ls = kwargs.get(arg, [])
        kw = { 'recursive': recurse}
        dst_list.extend(egroup_filter_generator(*ls, **kw))

    fl1 = fl2 = ''
    if included:
        fl1 = '(|%s)' % (''.join(['(%s)' %i for i in included]))
        fl = fl1
    if excluded:
        fl2 = '(!(|%s))' % (''.join(['(%s)' %i for i in excluded]))
        fl = fl2
    if included and excluded:
        fl = '(&%s%s)' % (fl1, fl2)
    return fl

@ldap_session('xldap.cern.ch')
def test_simple_filter(f):
    return f    

@ldap_session('xldap.cern.ch')
def egroup_querier(**kwargs):
    f =egroup_filter_combiner(**kwargs)
    return f
