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


class TestCase(BaseTestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        self.machine_category = MachineCategoryFactory(datastore='mock')
        self.resetDatastore()

    def tearDown(self):
        super(TestCase, self).tearDown()
        datastores._DATASTORES['mock'] = []

    def resetDatastore(self):
        self.datastore = Mock()
        datastores._DATASTORES['mock'] = [self.datastore]
