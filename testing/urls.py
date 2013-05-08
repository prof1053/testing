from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.main_page', name='main-page'),
    url(r'^show-model/$', 'core.views.show_model', name='show-model'),
    url(r'^edit-field/$', 'core.views.edit_field', name='edit-field'),
    url(r'^add-object/$', 'core.views.add_object', name='add-object'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )
