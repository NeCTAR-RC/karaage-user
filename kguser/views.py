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

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib import messages

from karaage.people.forms import PasswordChangeForm
from karaage.projects.models import Project
from karaage.machines.models import Account
from kguser.forms import UsernameChangeForm, ProjectNameForm
from kguser.user_improvements import get_improvement as get_user_improvements, valid_username
from kguser.project_improvements import (get_improvement as get_project_improvements,
                                         is_renamed as project_is_renamed)
from karaage.common.decorators import login_required
from karaage.common import log

@login_required
def username_change(request):

    # Return the user to the profile page if their username is already
    # valid.
    if valid_username(request.user.username):
        return HttpResponseRedirect(reverse('kg_user_profile'))

    if request.POST:
        form = UsernameChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Username changed successfully")
            return HttpResponseRedirect(reverse('kg_user_profile'))
    else:
        form = UsernameChangeForm()

    return render_to_response('people/user_username_form.html',
            {'form': form}, context_instance=RequestContext(request))


@login_required
def personal_details(request):

    if request.POST:
        form = PasswordChangeForm(request.POST)

        if form.is_valid():
            form.save(request.user)
            messages.success(request, "Password changed successfully")
            return HttpResponseRedirect(reverse('kg_user_profile'))
    else:
        form = PasswordChangeForm()

    return render_to_response('people/profile.html',
                              {'form': form},
                              context_instance=RequestContext(request))


@login_required
def make_project_default(request, account_id, project_id):
    person = request.user
    account = get_object_or_404(Account, pk=account_id, person=person)
    project = get_object_or_404(Project, pid=project_id)

    if request.method != 'POST':
        return HttpResponseRedirect(reverse('kg_user_profile'))

    account.default_project = project
    account.save()
    log(request.user, account, 2, 'Changed default project to %s' % project.pid)
    messages.success(request, "Default project changed succesfully")
    return HttpResponseRedirect(request.POST.get('next', reverse('kg_user_profile')))


@login_required
def confirm_project_name(request, project_id):
    project = get_object_or_404(Project, pid=project_id)

    # Return the user to the profile page if their project has already
    # had it's name confirmed.
    if project_is_renamed(project):
        return HttpResponseRedirect(reverse('kg_project_detail', kwargs={'project_id': project.pid}))

    # TODO (RS) this is bullshit
    if not request.user in project.leaders.all():
        return HttpResponseForbidden('<h1>Access Denied</h1>')

    if request.POST:
        form = ProjectNameForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            renamed = project.has_been_renamed.get()
            renamed.renamed = True
            renamed.save()
            messages.success(request, "Project name confirmed.")
            return HttpResponseRedirect(reverse('kg_project_detail', kwargs={'project_id': project.pid}))
    else:
        initial_pid = project.pid.lower()
        initial_pid = re.sub('[^a-z0-9.\-_]', '_', initial_pid)
        form = ProjectNameForm(instance=project, initial={'pid': initial_pid})

    return render_to_response('projects/project_confirmation_form.html',
                              {'form': form, 'project': project},
                              context_instance=RequestContext(request))


@login_required
def index(request):
    return render_to_response('index.html', {},
                              context_instance=RequestContext(request))
