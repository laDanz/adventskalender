from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('',
    # Examples:
    url(r'^$', 'base.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^manage/(?P<key>.+)?', 'base.views.manage_reward', name='manage_reward'),
    url(r'^success/', 'base.views.upoadsuccess', name='upoadsuccess'),
    #static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    url(r'^images/(?P<blob_key>.+)', 'base.views.images', name='images'),
    url(r'^files/(?P<blob_key>.+)', 'base.views.files', name='files'),
    
    url(r'^(?P<key>[^_].+)/$', 'base.views.reward', name='reward'),
    # url(r'^adventskalender/', include('adventskalender.foo.urls')),

    
    
)
