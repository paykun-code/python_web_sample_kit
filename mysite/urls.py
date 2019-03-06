from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^payNow/', include('paykunCheckout.url')),
	#url(r'^pay/', include('paykunCheckout.url')),
]
