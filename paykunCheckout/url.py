from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^(?P<pay_id>[0-9]+)/$', views.payNow, name='payNow'),
	#url(r'^pay/redirect', views.process_pay, name='process_pay'),
]