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

TEMPLATE = """
<div class="panel panel-info">
  <div class="panel-heading">
    <h3 class="panel-title">%(title)s</h3>
  </div>
  <div class="panel-body">
    %(description)s
    <a class="btn btn-default" href="%(action_url)s">%(action)s</a>
  </div>
</div>
"""

def valid_username(username):
    """Return True if the users username is a valid one."""
    return bool(re.match(r'^[a-z0-9][a-z0-9.\-_]{0,30}$', username))

def check_username(person):

    if not valid_username(person.username):
        return {'title': 'Username compatibility',
                'action': 'Change Username',
                'action_url': reverse('username_change'),
                'description': 'Your username isn\'t compatible with some systems.  This can be fixed by changing your username.'}

def get_improvement(person):
    if check_username(person):
        return SafeString(TEMPLATE % check_username(person))
    return ""
