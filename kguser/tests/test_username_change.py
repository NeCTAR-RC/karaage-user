
# Setup the broken Karaage test suite path
import sys
from os import path
import karaage
KARAAGE_TEST_PATH = path.join(path.dirname(karaage.__file__), '..', 'tests')
if KARAAGE_TEST_PATH not in sys.path:
    sys.path.append(KARAAGE_TEST_PATH)

from django.test import TestCase
from django.core.management import call_command
import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from tldap.test import slapd
import karaage.institutes.models
import karaage.people.models

from initial_ldap_data import test_ldif


class InstituteFactory(DjangoModelFactory):
    FACTORY_FOR = karaage.institutes.models.Institute
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = FuzzyText(prefix='inst-')


class PersonFactory(DjangoModelFactory):
    FACTORY_FOR = karaage.people.models.Person
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)

    username = FuzzyText(prefix='user-')
    password = 'test'
    full_name = factory.LazyAttribute(lambda a: a.username.title())
    short_name = factory.LazyAttribute(lambda a: a.username.title())
    email = factory.LazyAttribute(lambda a: '{0}@example.com'.format(a.username).lower())
    institute = factory.SubFactory(InstituteFactory)


class UsernameChangeTestCase(TestCase):
    def setUp(self):
        server = slapd.Slapd()
        server.set_port(38911)
        server.start()
        server.ldapadd("\n".join(test_ldif)+"\n")
        call_command('loaddata', 'karaage_data', **{'verbosity': 0})

        self.server = server

    def tearDown(self):
        self.server.stop()

    def test_view(self):
        person = PersonFactory()
        self.client.login(username=person.username, password='test')
        response = self.client.get('/profile/username')
