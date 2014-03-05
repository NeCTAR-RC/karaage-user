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

from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib import messages

from karaage.people.forms import PasswordChangeForm
from kguser.forms import UsernameChangeForm
from kguser.util import valid_username
from karaage.common.decorators import login_required

@login_required
def username_change(request):

    # Return the user to the profile page if their username is already
    # valid.
    if valid_username(request.user):
        return HttpResponseRedirect(reverse('kg_user_profile'))

    if request.POST:
        form = UsernameChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            # form.save()
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
def index(request):
    return render_to_response('index.html', {'improvement': get_improvement(request.user)},
                              context_instance=RequestContext(request))
