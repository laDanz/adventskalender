from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('',
    # Examples:
    url(r'^$', 'base.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    
    url(r'^manage/$', 'base.views.list_rewards', name='list_rewards'),
    url(r'^delete/(?P<key>.+)?', 'base.views.delete_reward', name='delete_reward'),
    url(r'^manage/(?P<key>.+)?', 'base.views.manage_reward', name='manage_reward'),
    url(r'^success/', 'base.views.upoadsuccess', name='upoadsuccess'),
    #static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    url(r'^images/(?P<blob_key>.+)', 'base.views.images', name='images'),
    url(r'^files/(?P<blob_key>.+)', 'base.views.files', name='files'),
    
    url(r'^(?P<key>[^_].+)/$', 'base.views.reward', name='reward'),
    # url(r'^adventskalender/', include('adventskalender.foo.urls')),

    
    
)
