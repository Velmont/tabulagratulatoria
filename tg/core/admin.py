import autocomplete_light
import reversion
from django.contrib import admin
from django.db import models

from core import admin_actions
from core import filters
from core.models import Entry
from core.models import Group
from core.widgets import NumberWidget


@admin.register(Entry)
class EntryAdmin(reversion.VersionAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'status',
                'shown_name',
                'first_name',
                'last_name',
                ('address', 'full_address', 'full_pay_address'),
                'postnummer',
                'place',
                ('email', 'phone'),
                ('num_issues', 'want_tg'),
                'groups',
                'notes',
            )
        }),
        ('Payment data', {
            'fields': (
                'pay_name',
                'pay_address',
                'pay_postnummer',
            )
        }),
    )
    readonly_fields = ['full_address', 'full_pay_address']
    filter_horizontal = ('groups',)
    form = autocomplete_light.modelform_factory(Entry, fields='__all__')
    formfield_overrides = {
        models.PositiveSmallIntegerField: {'widget': NumberWidget},
    }
    list_display = ('__unicode__', 'shown_name', 'first_name', 'last_name',
                    'status', 'want_tg', 'num_issues', 'address', 'email',
                    'postnummer')
    list_filter = ('status', ('groups', filters.AdditiveSubtractiveFilter),
                   'want_tg', 'num_issues')
    list_editable = ('want_tg', 'num_issues')
    save_on_top = True
    search_fields = ('shown_name', 'first_name', 'last_name',
                     'place', 'email', 'address',
                     '=postnummer__postnr',
                     'pay_name', 'pay_address', '=pay_postnummer__postnr',
                     'notes')
    actions = [
        admin_actions.simplified_csv_list,
        admin_actions.csv_list,
    ]

    def get_changelist_form(self, request, **kwargs):
        """
        Hack list_editable num_issues to be a html5 number widget
        """
        form = super(EntryAdmin, self).get_changelist_form(request, **kwargs)
        setattr(form.Meta, 'widgets', {'num_issues': NumberWidget()})
        return form


@admin.register(Group)
class GroupAdmin(reversion.VersionAdmin):
    list_display = ('__unicode__',)
