from django.conf.urls.defaults import *
from pitSimulator.PitSimulator.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^pitSimulator/', include('pitSimulator.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^hello/$', hello),
    (r'^$', intro),
    (r'^teams/$', listTeams),
    (r'^teams/register/$', registerTeam),
    (r'^teams/register/thanks/$', registerTeamThanks),
    (r'^users/$', listUsers),
    (r'^users/login/$', loginUser),
    (r'^users/register/$', registerUser),
    (r'^users/register/thanks/$', registerUserThanks),
    (r'^manager/$', manager),
    (r'^meta/$', displayMeta),
    (r'^ajax/$', ajax),
)
