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

from karaage.people import models as people_models
from karaage.machines import models as machine_models
from karaage.applications import models as app_models


class TrialProjectApplication(app_models.ProjectApplication):
    type = "trial"

    def info(self):
        return u"Complete account profile"

    def approve(self, approved_by):
        created_person, created_account = super(TrialProjectApplication,
                                                self).approve(approved_by)
        if self.content_type.model == 'person':
            person = self.applicant
            if not person.is_active:
                person.activate(approved_by)
        if self.applicant in self.project.leaders.all():
            self.project.leaders.remove(self.applicant)
        return created_person, created_account
    approve.alters_data = True


def trial_application_get_or_create(applicant_id):
    applicant = people_models.Person.objects.get(pk=applicant_id)
    try:
        applications = app_models.Application.objects.get_for_applicant(
            applicant)
        applications = applications.filter(projectapplication__project=None)
        application = applications[0].get_object()
    except IndexError:
        application = TrialProjectApplication(name="Trial project")
        application.applicant = applicant
        application.institute_id = applicant.institute.pk
        application.make_leader = False
        application.state = 'O'
        application.save()
        mc = machine_models.MachineCategory.objects.filter(name='Keystone')
        application.machine_categories = mc
        application.save()
    return application
