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

from os import path
import re
import sys

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.management import call_command
from tldap.test import slapd
from karaage.tests.initial_ldap_data import test_ldif
from karaage.projects.utils import add_user_to_project

from fixtures import AccountFactory, ProjectFactory, ProjectQuotaFactory

class ChangeDefaultProjectTestCase(TestCase):
    def setUp(self):
        server = slapd.Slapd()
        server.set_port(38911)
        server.start()
        server.ldapadd("\n".join(test_ldif)+"\n")
        call_command('loaddata', 'karaage_data', **{'verbosity': 0})

        self.server = server

    def tearDown(self):
        self.server.stop()

    def test_default_project(self):
        project_orig = ProjectFactory()
        account = AccountFactory(default_project=project_orig)
        ProjectQuotaFactory(project=project_orig, machine_category=account.machine_category)
        project = ProjectFactory()
        ProjectQuotaFactory(project=project, machine_category=account.machine_category)

        # TODO (RS) why the hell isn't this account a member of the
        # default project?
        add_user_to_project(account.person, project_orig)
        add_user_to_project(account.person, project)

        self.client.login(username=account.person.username, password='test')
        response = self.client.get(reverse('kg_user_profile_projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(re.search(r'<strong>Default:</strong>[\s]+%s' % project_orig.name,
                                  response.content, re.MULTILINE))

        response = self.client.post(reverse('kg_account_set_default', args=(account.id, project.pid)),
                                    {'next': reverse('kg_user_profile_projects')},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('http://testserver/profile/projects/', 302)])
        self.assertTrue(re.search(r'<strong>Default:</strong>[\s]+%s' % project.name,
                                  response.content, re.MULTILINE))
