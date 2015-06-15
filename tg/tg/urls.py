from django.conf.urls import include, url
from django.contrib import admin

from ui import urls as ui_urls


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(ui_urls, app_name='ui', namespace='ui')),
]
