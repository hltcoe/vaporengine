from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from viz import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^corpus/(?P<corpus_name>\w+)/$', views.corpus_overview, name='corpus_overview'),
)
