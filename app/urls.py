from django.conf.urls import patterns, include, url

from django.conf import settings
from app import views

urlpatterns = patterns('',
    url(r'test', views.test, name='test'),

    url(r'get_code', views.get_code, name='get_code'),
    url(r'use_code', views.use_code, name='use_code'),
    
    url(r'get_echos', views.get_echos, name='get_echos'),
    url(r'write_statu', views.write_statu, name='write_statu'),
)
