# Copyright 2014 The University of Melbourne
#
# This file is part of Karaage-User.
#
# Karaage-User is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Karaage-User is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Karaage-User If not, see <http://www.gnu.org/licenses/>.

from mock import Mock
from django.test import TestCase as BaseTestCase
from karaage import datastores
from fixtures import MachineCategoryFactory

LDAP_CONFIG = {
    'DESCRIPTION': 'Default LDAP datastore',
    'ENGINE': 'karaage.datastores.ldap.AccountDataStore',
    'LDAP': 'default',
    'ACCOUNT': 'karaage.datastores.ldap_schemas.openldap_account',
    'GROUP': 'karaage.datastores.ldap_schemas.openldap_group',
    'PRIMARY_GROUP': "institute",
    'DEFAULT_PRIMARY_GROUP': "dummy",
    'HOME_DIRECTORY': "/test/%(default_project)s/%(uid)s",
    'LOCKED_SHELL': '/usr/local/sbin/insecure',
}

class LDAPTestCase(TestCase):
    def setUp(self):
        super(LDAPTestCase, self).setUp()
        ldap = slapd.Slapd()
        ldap.set_port(38911)
        ldap.start()
        ldap.ldapadd("\n".join(test_ldif)+"\n")
        call_command('loaddata', 'karaage_data', **{'verbosity': 0})

        self._ldap = server

    def tearDown(self):
        super(LDAPTestCase, self).tearDown()
        self._ldap.stop()
