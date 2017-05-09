from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'invite_code.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^app/', include('app.urls')),
]
