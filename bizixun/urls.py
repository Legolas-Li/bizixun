"""bizixun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from market import views as mkv
from cherry import views as crv

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', mkv.get_index_html),
    url(r'^api/market/data/', mkv.get_market_data),


    url(r'^index/', crv.get_index_html),
    url(r'^market/', crv.get_market_html),
    url(r'^api/set/symbol/', crv.set_symbol_data),
    url(r'^api/get/symbol/', crv.get_symbol_data),
    url(r'^api/set/platform/', crv.set_platform_data),
    url(r'^api/get/platform/', crv.get_platform_data),


    url(r'^login/$', crv.login, name='login'),
    url(r'^logout/$', crv.logout, name='logout'),

]
