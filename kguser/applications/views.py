# Copyright 2007-2014 VPAC
# Copyright 2014 The University of Melbourne
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

""" This file shows the application views.  """

import datetime
import logging

from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from karaage.common.decorators import login_required
from karaage.common import is_admin
import karaage.applications.forms as forms
import karaage.applications.views.base as base
import karaage.applications.views.project as project_views
from karaage.projects.models import Project
from karaage.applications.views.project import get_applicant_from_email

from kguser.models import trial_application_get_or_create


LOG = logging.getLogger('kguser.applications')


@login_required
def complete_profile(request):
    """ An authenticated *applicant* is trying to access an application. """
    application = trial_application_get_or_create(request.user.pk)
    state_machine = base.get_state_machine(application)
    return state_machine.process(request, application,
                                 expected_state=None,
                                 label=None)


@login_required
def invitation_token(request, token, state=None, label=None):
    """An authenticated user is trying to access an application using
    a token."""
    application = base.get_application(
        secret_token=token, expires__gt=datetime.datetime.now())

    # If the applicant is a real Person, don't allow the application
    # to be stolen.
    if application.content_type.model != 'applicant':
        return redirect('index')

    # redirect user to real url if possible.
    if request.user.is_authenticated():
        if request.user == application.applicant:
            url = base.get_url(request, application, {'is_applicant': True},
                               label)
            return HttpResponseRedirect(url)

    state_machine = base.get_state_machine(application)
    return state_machine.process(request, application, state, label,
                                 {'is_applicant': True})


def _send_invitation(request, project, invite_form):
    """ The logged in project leader OR administrator wants to invite somebody.
    """
    form = invite_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            applicant, existing_person = get_applicant_from_email(email)

            if existing_person and 'existing' not in request.POST:
                return render_to_response(
                    'applications/project_common_invite_existing.html',
                    {'form': form, 'person': applicant},
                    context_instance=RequestContext(request))

            application = form.save(commit=False)
            application.applicant = applicant
            if project is not None:
                application.project = project
            application.save()
            state_machine = project_views.get_application_state_machine()
            state_machine.start(request, application)
            # Just redirect to project detail page.
            return redirect('kg_project_detail',
                            project_id=project.pid)

    return render_to_response(
        'applications/project_common_invite_other.html',
        {'form': form, 'project': project, },
        context_instance=RequestContext(request))


@login_required
def send_invitation(request, project_id=None):
    """ The logged in project leader wants to invite somebody to their project.
    """

    if is_admin(request):
        project = None
        if project_id is not None:
            project = get_object_or_404(Project, pid=project_id)
        form = forms.AdminInviteUserApplicationForm
    else:
        person = request.user
        project = get_object_or_404(Project, pid=project_id)

        if project_id is None:
            return HttpResponseBadRequest("<h1>Bad Request</h1>")

        if person not in project.leaders.all():
            return HttpResponseBadRequest("<h1>Bad Request</h1>")
        form = forms.LeaderInviteUserApplicationForm

    return _send_invitation(request, project, form)
