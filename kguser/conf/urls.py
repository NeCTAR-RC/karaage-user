from django.conf.urls import *
from django.conf import settings
from karaage.common import get_urls

from kguser.applications.trial import register
register()



urlpatterns = patterns('',
)

try:
    execfile("/etc/karaage/registration_override_urls.py")
except IOError:
    pass

profile_urlpatterns = patterns('',
    url(r'^$', 'kguser.views.personal_details', name='kg_user_profile'),
    url(r'^username', 'kguser.views.username_change', name='username_change'),
    url(r'^projects/$', 'kguser.views.profile', name='kg_user_profile_projects'),
    url(r'^edit/$', 'karaage.people.views.profile.edit_profile', name='kg_profile_edit'),
    url(r'^login/(?P<username>%s)/$' % settings.USERNAME_VALIDATION_RE, 'karaage.people.views.profile.login', name="login"),
    url(r'^logout/$', 'karaage.common.views.profile.logout', name='logout'),
    url(r'^logout_redirect/$', 'django.contrib.auth.views.logout', name='logout_redirect'),
)

for urls in get_urls("profile_urlpatterns"):
    profile_urlpatterns += urls
else:
    del urls

urlpatterns += patterns('',
    url(r'^$', 'kguser.views.index', name='index'),
    url(r'^persons/accounts/(?P<account_id>\d+)/makedefault/(?P<project_id>%s)/$' % settings.PROJECT_VALIDATION_RE,
        'kguser.views.make_project_default', name='kg_account_set_default'),
    url(r'^profile/', include(profile_urlpatterns)),
    url(r'^projects/(?P<project_id>%s)/$' % settings.PROJECT_VALIDATION_RE,
        'karaage.projects.views.project_detail', name='kg_project_detail'),
    url(r'^projects/(?P<project_id>%s)/confirm_name/' % settings.PROJECT_VALIDATION_RE,
        'kguser.views.confirm_project_name', name='confirm_project_name'),
    url(r'^projects/$', 'kguser.views.profile', name='kg_user_profile_projects'),
    url(r'^xmlrpc/$', 'django_xmlrpc.views.handle_xmlrpc',),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^lookup/', include('ajax_select.urls')),
)


for urls in get_urls("urlpatterns"):
    urlpatterns += urls
    del urls


urlpatterns += patterns('',
    url(r'^invitations/$', 'kguser.views.invitation_list', name='kg_application_list'),
    url(r'^invitations/(\d+)/$', 'kguser.views.invitation', name='kg_application_detail'),
    url(r'^invitations/(?P<application_id>\d+)/(?P<state>[-.\w]+)/$', 'kguser.views.invitation',
        name='kg_application_detail'),
    url(r'^invitations/(?P<application_id>\d+)/(?P<state>[-.\w]+)/(?P<label>[-.\w]+)/$', 'kguser.views.invitation',
        name='kg_application_detail'),
    url(r'^invitations/claim/(?P<token>[0-9a-f]+)/$',
        'kguser.applications.views.invitation_token', name='kg_application_unauthenticated'),
    url(r'^invitations/claim/(?P<token>[0-9a-f]+)/(?P<state>[-.\w]+)/$',
        'kguser.applications.views.invitation_token', name='kg_application_unauthenticated'),
    url(r'^invitations/claim/(?P<token>[0-9a-f]+)/(?P<state>[-.\w]+)/(?P<label>[-.\w]+)/$',
        'kguser.applications.views.invitation_token', name='kg_application_unauthenticated'),
    url(r'^projects/(?P<project_id>%s)/invite_user/$'
        % settings.PROJECT_VALIDATION_RE,
        'kguser.applications.views.send_invitation', name='kguser_invite_user'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^kgreg_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^karaage_graphs/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.GRAPH_ROOT}),
    )

try:
    execfile("/etc/karaage/user_urls.py")
except IOError:
    pass
