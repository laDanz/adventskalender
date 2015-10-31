from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'base.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^(?P<key>.+)/$', 'base.views.reward', name='reward'),
    # url(r'^adventskalender/', include('adventskalender.foo.urls')),

    
    
)
