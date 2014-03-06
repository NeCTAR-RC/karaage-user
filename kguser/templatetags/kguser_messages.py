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


from django import template
from django.template.loader import get_template
import karaage.projects.models
import karaage.people.models

from kguser.user_improvements import (get_improvement as get_user_improvements,
                                      has_improvement as has_user_improvements)
from kguser.project_improvements import (get_improvement as get_project_improvements,
                                         has_improvement as has_project_improvements)

register = template.Library()

@register.inclusion_tag('kguser/improvement_message.html')
def improvement_message(obj):
    if isinstance(obj, karaage.projects.models.Project):
        return get_project_improvements(obj)
    if isinstance(obj, karaage.people.models.Person):
        return get_user_improvements(obj)
    raise Exception("Unknown obj")

@register.filter
def has_improvement(obj):
    if isinstance(obj, karaage.projects.models.Project):
        return has_project_improvements(obj)
    if isinstance(obj, karaage.people.models.Person):
        return has_user_improvements(obj)
    raise Exception("Unknown obj")
