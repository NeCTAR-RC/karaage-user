# Django settings for kgreg project.
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

TEMPLATE_CONTEXT_PROCESSORS += ('karaage.common.context_processors.registration',)

import sys
if 'test' in sys.argv:
    execfile(path.join(path.dirname(__file__), "test_settings.py"))
else:
    execfile("/etc/karaage/user_settings.py")

INSTALLED_APPS = INSTALLED_APPS + ('bootstrap3', 'django_gravatar',)

if DEBUG:
    TEMPLATE_DIRS = (
        path.abspath(path.join(path.dirname(__file__), '..', '..', 'templates')),
        path.abspath(path.join(path.dirname(__file__), '..', 'templates')),
    ) + TEMPLATE_DIRS
