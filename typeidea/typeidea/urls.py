"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from custom_site import custom_site
from blog.views import post_list
from blog.views import (IndexView, CategoryView, TagView, PostDetailView)
from config.views import links
from blog.views import PostDetailView, SearchView, AuthorView
# import xadmin
from config.views import LinkListView
from django.contrib.sitemaps import views as sitemap_views
from django.views.decorators.cache import cache_page

from blog.sitemap import PostSitemap

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),
    # url(r'^post/(?P<pk>\d+).html$', PostDetailView.as_view(), name='post-detail'),
    url(r'^links/$', LinkListView.as_view(), name='links'),
    url(r'^search/$', SearchView.as_view(), name='search'),

    url(r'^super_admin/', admin.site.urls, name='super-admin'),
    url(r'^admin/', custom_site.urls, name='admin'),
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^sitemap\.xml$', cache_page(60 * 20, key_prefix='sitemap_cache_')(sitemap_views.sitemap),
        {'sitemaps': {'posts': PostSitemap}}),
    url(r'^captcha/', include('captcha.urls')),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'__debug__/',include(debug_toolbar.urls)),
        url(r'^silk/', include('silk.urls', namespace='silk'))
    ] + urlpatterns

