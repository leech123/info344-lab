from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns 
from . import views

urlpatterns = [
	url(r'^$', views.post_list, name='post_list'),
	url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
	url(r'^post/new/$', views.post_new, name='post_new'),
	url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
	url(r'^post/(?P<pk>[0-9]+)/remove/$', views.post_remove, name='post_remove'),
	url(r'^post/(?P<pk>[0-9]+)/recap/$', views.post_recapture, name='post_recapture'),
	url(r'^post_rest_api/$', views.post_list_rest_api),
	url(r'^post_rest_api/(?P<pk>[0-9]+)/$', views.post_detail_rest_api),


]
urlpatterns = format_suffix_patterns(urlpatterns)