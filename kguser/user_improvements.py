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

import re

from django.core.urlresolvers import reverse
from django.utils.safestring import SafeString

USERNAME_MSG = """You haven't chosen a username.  To help support new services.  We
would like you to take a moment to choose one."""

def valid_username(username):
    """Return True if the users username is a valid one."""
    return bool(re.match(r'^[a-z0-9][a-z0-9.\-_]{0,30}$', username))

def check_username(person):

    if not valid_username(person.username):
        return {'title': 'Username',
                'action': 'Choose Username',
                'action_url': reverse('username_change'),
                'description': USERNAME_MSG}

def get_improvement(person):
    if check_username(person):
        return check_username(person)
    return None

def has_improvement(person):
    if check_username(person):
        return True
    return False
