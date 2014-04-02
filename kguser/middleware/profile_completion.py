# Copyright 2014 Kieran Spear
#
# This file is part of Karaage.
#
# Karaage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Karaage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Karaage  If not, see <http://www.gnu.org/licenses/>.

import logging
import re

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from kguser.applications import views


logging.basicConfig()
logger = logging.getLogger(__name__)


class ProfileCompletionMiddleware(object):
    """
    Middleware for utilizing Web-server-provided authentication.

    """
    def __init__(self):
        super(ProfileCompletionMiddleware, self).__init__()
        default_whitelist = (
            '/logout/$',
            '/invitations/claim/.*',
            '/shibboleth/.*',
        )
        exceptions = getattr(settings, 'PROFILE_COMPLETION_WHITELIST',
                             default_whitelist)
        self.exceptions = tuple(re.compile(url) for url in exceptions)

    def process_view(self, request, view_func, view_args, view_kwargs):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django SAML user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the SamlUserMiddleware class.")

        for url in self.exceptions:
            if url.match(request.path):
                return

        if request.user.is_authenticated():
            if request.user.date_approved is None:
                resp = views.complete_profile(request)
                if not request.path.startswith(resp['location']):
                    return resp
