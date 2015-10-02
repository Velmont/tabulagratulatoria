from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.adder, name='adder'),
    url(r'^home/$', views.home, name='home'),
    url(r'^takk/$', views.takk, name='takk'),
]
