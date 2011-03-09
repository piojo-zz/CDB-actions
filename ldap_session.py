'''Module for running unauthenticated ldap queries. It provides a
decorator class, that will query an LDAP server with an arbitrarily
complex filter computed by a decorated filter generator.'''

import os
import sys
import ldap

class ldap_session(object):
    '''Decorator class. Receives the basic LDAP parameters (server,
    search base and scope...). It is callable, for use as a Python
    decorator. '''
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

    def __call__(self, filter_generator):
        '''Decorates the filter generator, which should return the
        LDAP filter string, to be used as the LDAP query.'''
        def decorated_generator(*args, **kwargs):
            r = self.connection.search(self.base, 
                                       self.scope,
                                       filter_generator(*args, **kwargs),
                                       self.retrieve_all)
            return self.connection.result(r)
        return decorated_generator

