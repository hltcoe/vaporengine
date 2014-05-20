from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from viz import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
)
