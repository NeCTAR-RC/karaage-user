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

def is_renamed(project):
    """Return True if the project has been renamed as part of it's
    migration from Keystone.

    """
    # If the project wasn't created in the initial migration then it
    # should be treated as if it has already been renamed.
    if project.approved_by and project.approved_by.username != 'tom-karaage':
        return True
    renamed, created = project.has_been_renamed.get_or_create()
    return renamed.renamed

def check_project_name(project):
    if not is_renamed(project):
        return {'title': 'Project name confirmation',
                'action': 'Confirm Project Name',
                'action_url': reverse('confirm_project_name', kwargs={'project_id': project.pid}),
                'description': 'To completely this projects creation you\'ll need to take a moment to confirm it\'s name.'}

def get_improvement(project):
    if check_project_name(project):
        return check_project_name(project)
    return None


def has_improvement(project):
    if check_project_name(project):
        return True
    return False
