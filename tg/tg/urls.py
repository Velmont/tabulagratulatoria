from django.conf.urls import include, url
from django.contrib import admin

from ui import urls as ui_urls

admin.site.site_header = 'NO2014-festskrift'


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^', include(ui_urls, app_name='ui', namespace='ui')),
]
