# Copyright 2007-2013 VPAC
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

""" This file shows the project application views using a state machine. """

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django import forms as django_forms

from karaage.people.models import Person
from karaage.people.utils import (validate_username_for_rename_person,
                                  UsernameException)
import karaage.applications.forms as app_forms
import karaage.applications.views.base as base
from karaage.applications.views.base import State
from karaage.applications.views import states
from karaage.applications.views.project import StateWithSteps, Step
from kgterms.models import Terms, UserAgreed
from kgterms import forms as terms_forms
from kguser.models import TrialProjectApplication


class StateStepIntroduction(Step):
    """ Invitation has been sent to applicant. """
    name = "Read introduction"

    def view(self, request, application, label, auth, actions):
        """ Django view method. """
        for action in actions:
            if action in request.POST:
                return action
        return render_to_response('applications/trial_aed_introduction.html',
                {'actions': actions, 'application': application, 'auth': auth},
                context_instance=RequestContext(request))


class StateStepAgreeToTerms(Step):
    name = "Agree to terms and conditions"

    def view(self, request, application, label, auth, actions):
        """ Django view method. """
        forms = []
        terms = (Terms.objects
                .exclude(users_agreed__person=application.applicant)
                .exclude(active=False))
        for term in terms:
            user_agreed = UserAgreed(terms=term, person=application.applicant)
            forms.append(terms_forms.AgreeToTermsForm(request.POST or None,
                                                      instance=user_agreed,
                                                      prefix=term.pk))
        if request.method == 'POST':
            all_forms_valid = all(map(lambda f: f.is_valid(), forms))
            if all_forms_valid:
                for form in forms:
                    form.save(commit=True)
            for action in actions:
                if action == 'next' and not all_forms_valid:
                    continue
                if action in request.POST:
                    return action
        return render_to_response('applications/trial_aed_terms.html',
                {'actions': actions, 'application': application, 'auth': auth,
                 'forms': forms},
                context_instance=RequestContext(request))



class PersonForm(django_forms.ModelForm):
    telephone = django_forms.RegexField(
            "^[0-9a-zA-Z\.( )+-]+$", required=True, label=u"Office Telephone",
            help_text=u"Used for emergency contact and password reset service.",
            error_messages={'invalid':
            'Telephone number may only contain digits, letter, hyphens, spaces, braces, and the plus sign.'})
    mobile = django_forms.RegexField(
            "^[0-9a-zA-Z( )+-]+$",
            required=False,
            error_messages={'invalid':
            'Telephone number may only contain digits, letter, hyphens, spaces, braces, and the plus sign.'})
    address = django_forms.CharField(label=u"Mailing Address", required=False, widget=django_forms.Textarea())

    class Meta:
        model = Person
        fields = ['username', 'title', 'short_name', 'full_name', 'telephone', 'position', 'supervisor',
                  'department', 'mobile', 'address']

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True

    def clean_username(self):
        username = self.cleaned_data['username']
        if username:
            try:
                validate_username_for_rename_person(username, self.instance)
            except UsernameException, e:
                raise django_forms.ValidationError(e.args[0])
            return username


class StateStepApplicant(Step):
    """ Application is open and user is can edit it."""
    name = "Open"

    def view(self, request, application, label, auth, actions):
        """ Django view method. """
        # Get the appropriate form
        status = None
        if application.applicant.saml_id is not None:
            username = application.applicant.email
            form = PersonForm(
                request.POST or None,
                instance=application.applicant,
                initial={'username': username})
        else:
            form = app_forms.UserApplicantForm(
                request.POST or None,
                instance=application.applicant)

        # Process the form, if there is one
        if form is not None and request.method == 'POST':
            if form.is_valid():
                form.save(commit=True)
                for action in actions:
                    if action in request.POST:
                        return action
                return HttpResponseBadRequest("<h1>Bad Request</h1>")
            else:
                # if form didn't validate and we want to go back or cancel,
                # then just do it.
                if 'cancel' in request.POST:
                    return "cancel"
                if 'prev' in request.POST:
                    return 'prev'


        # If we don't have a form, we can just process the actions here
        if form is None:
            for action in actions:
                if action in request.POST:
                    return action

        # Render the response
        return render_to_response(
                'applications/trial_aed_applicant.html', {
                'form': form,
                'application': application,
                'status': status, 'actions': actions, 'auth': auth },
                context_instance=RequestContext(request))


class StateApplicantEnteringDetails(StateWithSteps):
    name = "Applicant entering details."

    def __init__(self):
        super(StateApplicantEnteringDetails, self).__init__()
        self.add_step(StateStepIntroduction(), 'intro')
        self.add_step(StateStepAgreeToTerms(), 'terms')
        self.add_step(StateStepApplicant(), 'applicant')


class TransitionAutoApprove(base.Transition):
    """ A transition after application fully approved. """
    def __init__(self, on_approved, on_error):
        self._on_approved = on_approved
        self._on_error = on_error

    def get_next_state(self, request, application, auth):
        """ Retrieve the next state. """
        # Check for serious errors in submission.
        # Should only happen in rare circumstances.
        errors = application.check()
        if len(errors) > 0:
            for error in errors:
                messages.error(request, error)
            return self._on_error

        # approve application
        approver = Person.objects.filter(is_admin=True).first()
        created_person, created_account = application.approve(approver)

        # send email
        #link, is_secret = base.get_email_link(application)
        #emails.send_approved_email(application, created_person, created_account, link, is_secret)

        return self._on_approved


class StateRedirectToHome(State):
    """ This application is archived. """
    name = "Archived"

    def view(self, request, application, label, auth, actions):
        return redirect('index')


def get_application_state_machine():
    """ Get the default state machine for applications. """
    state_machine = base.StateMachine()
    approve_transition = TransitionAutoApprove(on_approved='A',
                                               on_error="R")
    state_machine.add_state(
        StateApplicantEnteringDetails(), 'O',
        {'cancel': 'R', 'reopen': 'O', 'submit':  'P'})
    state_machine.add_state(
        states.StatePassword(), 'P',
        {'submit': states.TransitionSubmit(on_success=approve_transition,
                                           on_error="R")})
    state_machine.add_state(StateRedirectToHome(), 'A', {})
    state_machine.add_state(states.StateDeclined(), 'R', {'reopen': 'O', })
    state_machine.set_first_state('O')
#    NEW = 'N'
#    OPEN = 'O'
#    WAITING_FOR_LEADER = 'L'
#    WAITING_FOR_DELEGATE = 'D'
#    WAITING_FOR_ADMIN = 'K'
#    PASSWORD = 'P'
#    COMPLETED = 'C'
#    ARCHIVED = 'A'
#    DECLINED = 'R'
    return state_machine


def register():
    base.setup_application_type(TrialProjectApplication,
                                get_application_state_machine())
