from django.contrib import admin

from core.models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'sort_name',
                    'address', 'email', 'postnummer')
