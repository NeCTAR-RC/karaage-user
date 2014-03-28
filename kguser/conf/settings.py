# Django settings for kguser project.
from os import path
from karaage.conf.settings import *
TEMPLATE_DIRS += (
    '/usr/share/kguser/templates',
)

ROOT_URLCONF = 'kguser.conf.urls'

SITE_ID = 2

STATIC_ROOT = '/var/lib/karaage-user/static'
STATIC_URL = '/kguser_media/'

LOGIN_URL = '/users/accounts/login/'

ALLOW_REGISTRATIONS = False

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

BOOTSTRAP3 = {
    'jquery_url': '//code.jquery.com/jquery.min.js',
    'base_url': '//netdna.bootstrapcdn.com/bootstrap/3.1.1/',
    'css_url': '//netdna.bootstrapcdn.com/bootswatch/3.1.1/simplex/bootstrap.min.css',
    'theme_url': None,
    'javascript_url': None,
    'horizontal_label_class': 'col-md-2',
    'horizontal_field_class': 'col-md-4',
    'set_required': True,
}

INSTALLED_APPS = INSTALLED_APPS + ('kguser', 'bootstrap3', 'django_gravatar',)

import sys
if 'test' in sys.argv:
    execfile(path.join(path.dirname(__file__), "test_settings.py"))
else:
    execfile("/etc/karaage/user_settings.py")


if DEBUG:
    TEMPLATE_DIRS = (
        path.abspath(path.join(path.dirname(__file__), '..', '..', 'templates')),
        path.abspath(path.join(path.dirname(__file__), '..', 'templates')),
    ) + TEMPLATE_DIRS
