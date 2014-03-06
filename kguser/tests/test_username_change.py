
# Setup the broken Karaage test suite path
import sys
from os import path
import karaage
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.contrib.auth.hashers import make_password
import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText
from tldap.test import slapd
import karaage.institutes.models
import karaage.people.models

from karaage.tests.initial_ldap_data import test_ldif


class InstituteFactory(DjangoModelFactory):
    FACTORY_FOR = karaage.institutes.models.Institute
    FACTORY_DJANGO_GET_OR_CREATE = ('name',)

    name = FuzzyText(prefix='inst-')


class PersonFactory(DjangoModelFactory):
    FACTORY_FOR = karaage.people.models.Person
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)

    username = FuzzyText(prefix='user-', chars='abcdefghijklmnopqrstuvwxyz')
    password = make_password('test')
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

    def test_valid_username(self):
        person = PersonFactory()
        authenticated = self.client.login(username=person.username, password='test')
        self.assertTrue(authenticated)
        response = self.client.get(reverse('username_change'))
        self.assertEqual(response.status_code, 302,
                         "User with name %s should have been redirected." % person.username)

    def test_username_change(self):
        person = PersonFactory(username="test@example.com")
        print person.username
        self.client.login(username=person.username, password='test')

        # A user with an invalid username should be able to visit the
        # username change page.
        response = self.client.get(reverse('username_change'))
        self.assertEqual(response.status_code, 200)

        # Submitting an empty form should result in the same page
        # being displayed again.
        response = self.client.post(reverse('username_change'), {'username': ''})
        self.assertEqual(response.status_code, 200)

        # After changing a user name the user should be redirected to
        # the profile page.
        response = self.client.post(reverse('username_change'), {'username': 'valid-user'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('http://testserver/profile/', 302)])
