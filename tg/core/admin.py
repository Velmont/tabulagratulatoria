import reversion
from django.contrib import admin

from core.models import Entry


@admin.register(Entry)
class EntryAdmin(reversion.VersionAdmin):
    search_fields = ('shown_name', 'first_name', 'last_name', 'place', 'email', 'address',)
    list_display = ('__str__', 'first_name', 'last_name', 'status',
                    'address', 'email', 'postnummer')
