"""vaporengine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

import visualizer.views

urlpatterns = [
    url(r'^$', visualizer.views.index, name='home'),
    url(r'^venncloud_json_for_document', visualizer.views.venncloud_json_for_document, name='venncloud_json_for_document'),
    url(r'visualizer/', include('visualizer.urls')),
    url(r'^admin/', admin.site.urls),
]
