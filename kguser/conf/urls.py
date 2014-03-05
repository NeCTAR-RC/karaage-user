from django.conf.urls import *
from django.conf import settings
from django.contrib import admin


urlpatterns = patterns('',
)

try:
    execfile("/etc/karaage/registration_override_urls.py")
except IOError:
    pass

profile_urlpatterns = patterns('',
    url(r'^$', 'kguser.views.personal_details', name='kg_user_profile'),
    url(r'^username', 'kguser.views.username_change', name='username_change'),
    url(r'^accounts/$', 'karaage.people.views.user.profile_accounts', name='kg_user_profile_accounts'),
    url(r'^projects/$', 'karaage.people.views.user.profile_projects', name='kg_user_profile_projects'),
    url(r'^edit/$', 'karaage.people.views.user.edit_profile', name='kg_profile_edit'),

    url(r'^slogin/$', 'karaage.people.views.user.saml_login', name='login_saml'),
    url(r'^saml/$', 'karaage.people.views.user.saml_details', name='saml_details'),
    url(r'^login/$', 'karaage.people.views.user.login', name='login'),
    url(r'^login/(?P<username>%s)/$' % settings.USERNAME_VALIDATION_RE, 'karaage.people.views.user.login', name="login"),
    url(r'^logout/$', 'karaage.people.views.user.logout', name='logout'),
    url(r'^password/$', 'karaage.people.views.user.password_change', name='password_change'),
)


urlpatterns += patterns('',
    url(r'^$', 'kguser.views.index', name='index'),
    url(r'^aup/$', 'karaage.legacy.simple.direct_to_template', {'template': 'aup.html'}, name="aup"),
    url(r'^persons/', include('karaage.people.urls.user')),
    url(r'^profile/', include(profile_urlpatterns)),
    url(r'^institutes/', include('karaage.institutes.urls.user')),
    url(r'^projects/', include('karaage.projects.urls.user')),
    url(r'^software/', include('karaage.software.urls.user')),
    url(r'^applications/', include('karaage.applications.urls.user')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^ajax_selects/', include('ajax_select.urls')),
    url(r'^xmlrpc/$', 'django_xmlrpc.views.handle_xmlrpc',),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^kgreg_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^karaage_graphs/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.GRAPH_ROOT}),
    )

execfile("/etc/karaage/registration_urls.py")
