from django.contrib.admin.filters import RelatedFieldListFilter
from django.utils.translation import ugettext as _


class AdditiveSubtractiveFilter(RelatedFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.using_params = []
        self.attname = field.get_attname()
        self.paramstart = "adv_" + self.attname

        super(AdditiveSubtractiveFilter, self).__init__(
            field, request, params, model, model_admin, field_path)

    def has_output(self):
        return len(self.lookup_choices) > 0

    def _make_param(self, field_id):
        return self.paramstart + str(field_id)

    def expected_parameters(self):
        for lookup, title in self.lookup_choices:
            self.using_params.append(self._make_param(lookup))
        return self.using_params

    def queryset(self, request, queryset):
        for key, value in self.used_parameters.items():
            id_lookup = '%s__id' % self.attname
            if value == 'exc':
                queryset = queryset.exclude(
                    **{id_lookup: key.replace(self.paramstart, '')})
            elif value == 'inc':
                queryset = queryset.filter(
                    **{id_lookup: key.replace(self.paramstart, '')})
        return queryset

    def choices(self, cl):
        yield {
            'selected': len(set(self.used_parameters).intersection(self.using_params)) == 0,
            'query_string': cl.get_query_string({}, self.using_params),
            'display': _('All'),
        }
        for p in (('inc', _('Show')), ('exc', _('Hide'))):
            for lookup, title in self.lookup_choices:
                # If the link is selected
                if p[0] == self.used_parameters.get(self._make_param(lookup)):
                    yield {
                        'selected': True,
                        'query_string': cl.get_query_string({},
                            [ self._make_param(lookup) ]),
                        'display': "%s %s" % (p[1], title),
                    }
                else:
                    yield {
                        'selected': False,
                        'query_string': cl.get_query_string({
                            self._make_param(lookup): p[0],
                        }, []),
                        'display': "%s %s" % (p[1], title),
                    }
