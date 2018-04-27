# encoding:utf8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
#import myproject.api
from app.views import *

urlpatterns = patterns('',
    url(r'^admin/', admin.site.urls),
 url(r'cmdb/postinfo/$', 'cmdb.views.postinfo'),
 url(r'cmdb/list/$', 'cmdb.views.list'),
 url(r'cmdb/show/$', 'cmdb.views.show'),
 url(r'cmdb/update/$', 'cmdb.views.update'),
 url(r'cmdb/idc_list/$', 'cmdb.views.idc_list'),
 url(r'cmdb/project_list/$', 'cmdb.views.project_list'),
 url(r'index/$', index),
 url(r'select/$', select),
 url(r'code/$', code),
 url(r'code_update/$', code_update),
 url(r'cmd/$', cmd),
 url(r'cmd_result/$', cmd_result),
 url(r'edit/$', edit_config),
 url(r'paging/$', paging),
 url(r'^$', index),
 url(r'login/$', login),
 url(r'test/$', test),
 url(r'upload/$', upload_file),
 url(r'navi/$', navi),
 url(r'play_book/$', play_book),
 url(r'page_front/$', page_front),
 url(r'^hours_ahead/(\d{1,2}$)', index4),
 url(r'^current_datetime/$', index5),
                       )
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

#urlpatterns += patterns(
#    '',
#    url(r'^api/', include(myproject.api.router.urls)),
#    url(r'^api-auth/', include('rest_framework.urls',
#                               namespace='rest_framework')),
#)
