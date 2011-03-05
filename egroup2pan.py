'''Module querying LDAP for e-group combinations'''

import os
import sys
import ldap
from ldap_session import ldap_session
        
@ldap_session('xldap.cern.ch')
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
    if len(q) > 1:
        fl =  '(|' + ''.join(['(%s)' % i for i in q]) + ')'
    else:
        fl = q[0]
    return fl

if __name__ == '__main__':
    import doctest
    doctest.testfile('test/test_egroups.txt)

