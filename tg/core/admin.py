import reversion
from django.contrib import admin

from core import filters
from core.models import Entry
from core.models import Group


@admin.register(Entry)
class EntryAdmin(reversion.VersionAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'status',
                'shown_name',
                'first_name',
                'last_name',
                'address',
                'postnummer',
                'place',
                ('email', 'phone'),
                'groups',
                'notes',
            )
        }),
    )
    filter_horizontal = ('groups',)
    list_display = ('__unicode__', 'first_name', 'last_name', 'status',
                    'address', 'email', 'postnummer')
    list_filter = ('status', ('groups', filters.AdditiveSubtractiveFilter))
    save_on_top = True
    search_fields = ('shown_name', 'first_name', 'last_name',
                     'place', 'email', 'address',
                     '=postnummer__postnr')


@admin.register(Group)
class GroupAdmin(reversion.VersionAdmin):
    list_display = ('__unicode__', 'name', 'category')
    list_filter = ('category',)
