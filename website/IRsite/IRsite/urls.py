"""IRsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, re_path
from fulltextSearch import views

urlpatterns = [
    #url(r'^$', views.index),
    #url(r'^index', views.index),
    #url(r'^upload', views.upload),
    re_path('^$', views.index),
    re_path(r'^upload', views.upload),
    re_path(r'^index', views.index),
    re_path(r'^xml', views.Zipf_xml),
    re_path(r'^json', views.Zipf_json),
    re_path(r'^chart', views.chart),
    re_path(r'^tfidf', views.chart),
    path('admin/', admin.site.urls),
]
