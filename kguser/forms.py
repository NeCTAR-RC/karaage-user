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

from django import forms
from django.conf import settings

from karaage.datastores import machine_category_account_exists
from karaage.people.models import Person
from karaage.projects.models import Project

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['username']

    username = forms.RegexField(
        r'^[a-z0-9][a-z0-9.\-_]+$', required=True, label=u"Username",
        help_text=u"The username that will be used to authenticate to services.",
        error_messages={'invalid': 'Usernames must start with a lowercase letter or number and can only contain lowercase letters or numbers \'.\', \'-\' or \'_\''})

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 31:
            raise forms.ValidationError(u'Your username can\'t be longer that 31 characters.')

        for ua in self.instance.account_set.filter(date_deleted__isnull=True):

            if ua.username == username:
                continue
            if account_exists(username, ua.machine_category):
                raise forms.ValidationError(u'This username is already taken.')

        return username

    def save(self, commit=True):
        data = self.cleaned_data
        # Update all the users accounts before saving the person
        # model.  This isn't ideal because there is no way to roll
        # back the changes to the datastores if one of the changes
        # fails.
        for ua in self.instance.account_set.filter(date_deleted__isnull=True):
            ua.username = data['username']
            ua.save()

        return super(UsernameChangeForm, self).save(commit=commit)



class ProjectNameForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['pid', 'name']

    name = forms.CharField(label='Project Title', widget=forms.TextInput(attrs={'size': 60}))
    pid = forms.RegexField(
        r'^[a-z0-9][a-z0-9.\-_]+$', required=True, label=u"Project Id",
        help_text=u"The simplified name of the project that will be used as an identifier.",
        error_messages={'invalid': 'Project ids must start with a lowercase letter or number and can only contain lowercase letters or numbers \'.\', \'-\' or \'_\''})

    def clean_pid(self):
        pid = self.cleaned_data['pid']
        if len(pid) > 20:
            raise forms.ValidationError(u'Your project id can\'t be longer that 20 characters.')

        return pid

    def save(self):
        group = self.instance.group
        group.name = self.cleaned_data['pid']
        group.save()

        return super(ProjectNameForm, self).save()
