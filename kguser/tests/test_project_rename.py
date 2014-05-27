from django.core.urlresolvers import reverse
from karaage.tests.unit import UnitTestCase
from karaage.projects.models import Project

from fixtures import (PersonFactory, AccountFactory,
                      ProjectQuotaFactory, ProjectRenamedFactory)


class ProjectRenameTestCase(UnitTestCase):

    def test_project_renamed(self):
        """Create a new project that has been renamed correctly."""
        account = AccountFactory()
        person = account.person
        project = account.default_project

        # If the project is approved by anyone other than tom-karaage
        approver = PersonFactory(username='tom-karaage')
        project.approved_by = approver
        project.save()

        ProjectQuotaFactory(project=project, machine_category=account.machine_category)
        ProjectRenamedFactory(project=project, renamed=True)

        authenticated = self.client.login(username=person.username, password='test')
        self.assertTrue(authenticated)
        response = self.client.get(reverse('confirm_project_name', kwargs={'project_id': project.pid}))
        self.assertEqual(response.status_code, 302,
                         "Projects shouldn't be allowed to rename more than once.")

    def test_new_project_renamed(self):
        """Create a new project that was not part of the initial migration."""
        account = AccountFactory()
        project = account.default_project
        person = account.person
        ProjectQuotaFactory(project=project, machine_category=account.machine_category)

        authenticated = self.client.login(username=person.username, password='test')
        self.assertTrue(authenticated)
        response = self.client.get(reverse('confirm_project_name', kwargs={'project_id': project.pid}))
        self.assertEqual(response.status_code, 302,
                         "Projects shouldn't be allowed to rename more than once.")

    def test_project_name_change(self):
        account = AccountFactory(machine_category=self.machine_category)
        project = account.default_project
        person = account.person
        ProjectQuotaFactory(project=project,
                            machine_category=self.machine_category)

        # Set the project app approve by to the tom account
        approver = PersonFactory(username='tom-karaage')
        project.approved_by = approver
        project.leaders.add(person)
        project.save()

        self.client.login(username=person.username, password='test')
        self.resetDatastore()

        # A user should be able to visit the project name change page
        # if the project is part of the initial migration and it
        # hasn't been renamed already.
        response = self.client.get(reverse('confirm_project_name',
                                           kwargs={'project_id': project.pid}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.datastore.save_project.called)

        # Submitting an empty form should result in the same page
        # being displayed again.
        response = self.client.post(reverse('confirm_project_name',
                                            kwargs={'project_id': project.pid}),
                                    {'name': '',
                                     'pid': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.datastore.save_project.called)

        # After changing a project name the user should be redirected to
        # the new project page.
        new_pid = 'my_project'
        old_pid = project.pid
        response = self.client.post(reverse('confirm_project_name',
                                            kwargs={'project_id': project.pid}),
                                    {'name': 'My Project',
                                     'pid': new_pid}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain,
                         [('http://testserver/projects/my_project/', 302)])

        self.datastore.save_project.assert_called_with(project)
        self.datastore.set_project_pid.assert_called_with(project, old_pid, new_pid)
        self.datastore.set_group_name.assert_called_with(
            Project.objects.get(pid=new_pid).group, old_pid, new_pid)

        project = Project.objects.get(id=project.id)
        self.assertEqual(project.name, 'My Project')
        self.assertEqual(project.pid, 'my_project')
        self.assertEqual(project.group.name, 'my_project')
        self.assertTrue(project.has_been_renamed.get().renamed)
