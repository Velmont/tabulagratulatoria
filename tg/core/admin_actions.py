# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 sts=4 expandtab ai

from __future__ import unicode_literals

import csv

from django.forms.models import model_to_dict
from django.http import HttpResponse


def csv_list(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'filename=datalist.csv'

    dc = csv.writer(response, quoting=csv.QUOTE_ALL)
    dc.writerow(model_to_dict(queryset[0]).keys())
    for m in queryset:
        a = model_to_dict(m).values()
        dc.writerow([unicode(s).encode('utf-8') for s in a])
    return response
csv_list.short_description = "Full datalist"


def simplified_csv_list(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'filename=simplified_data.csv'

    dc = csv.writer(response, quoting=csv.QUOTE_ALL)
    dc.writerow([
        "Printed name",
        "Contact name",
        "Want TG",
        "Num issues",
        "Full address",
        "Full pay address",
        "Email",
        "Phone",
        "Status",
        "Groups",
        "Notes",
    ])
    for m in queryset:
        groups = ' '.join(g.slug for g in m.groups.all())
        a = [
            m.printed_name,
            m.contact_full_name,
            m.want_tg,
            m.num_issues,
            m.full_address,
            m.full_pay_address,
            m.email,
            m.phone,
            m.status,
            groups,
            m.notes,
        ]
        dc.writerow([unicode(s).encode('utf-8') for s in a])
    return response
simplified_csv_list.short_description = "Enkel medlemsliste"
