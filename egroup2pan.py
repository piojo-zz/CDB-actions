import os
import sys
import ldap


class ldap_session(object):
    '''LDAP session, to be decorated. Function f will process the results
of the ldap query.'''
    cache = dict()
    def __init__(self, server,
                 base = 'ou=users,ou=organic units,dc=cern,dc=ch',
                 scope = ldap.SCOPE_SUBTREE,
                 retrieve_all = None):
        if server not in ldap_session.cache:
            ldap_session.cache[server] = ldap.open(server)
        self.connection = ldap_session.cache[server]
        self.base = base
        self.scope = scope
        self.retrieve_all = retrieve_all

    def __call__(self, query_generator):
        '''Decorates the query generator, which should return the LDAP query
string, that will be called.'''
        def decorated_generator(*args, **kwargs):
            r = self.connection.search(self.base, 
                                       self.scope,
                                       query_generator(*args, **kwargs),
                                       self.retrieve_all)
            return self.connection.result(r)
        return decorated_generator

def ldap_list_field(t, r, field = 'sAMAccountName'):
    '''Returns a list of the selected field from the LDAP result list.'''
    l = []
    for i in r:
        l.append(i[1][field][0])
    return l

def ldap_query_generator(**subgenerators):
    def generate_ldap_queries(**queries):
        query = []
        for i, j in queries.items():
            query.append(subgenerators.get(i))(j)
        return ''.join(query)
    return generate_ldap_queries
    
        

class ldap_query_generator(object):
    def __init__(self, **subgenerators):
        

        

def egroup_querier(*egroups, **params):

    if params.get('recursive'):
        rs = ':1.2.840.113556.1.4.1941:'
    else:
        rs = ''

    q = []
    for i in egroups:
        entry = ['memberOf', rs, '=CN=', i,
                 ',OU=e-groups,OU=Workgroups,DC=cern,DC=ch']
        q.append(''.join(entry))
    if len(q) > 1:
        query =  '(|' + ''.join(['(%s)' % i for i in q]) + ')'
    else:
        query = q[0]

    print query
    return query

if __name__ == '__main__':
    r, d = egroup_querier('cert-sec', 'Computer.Security', recursive = True)
    print '\n'.join(ldap_list_field(r, d))

