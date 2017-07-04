from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^add/$', views.adder, name='adder'),
    url(r'^takk/$', views.takk, name='takk'),
]
