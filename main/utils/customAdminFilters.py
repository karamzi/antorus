from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _


class ProductArchiveFilter(SimpleListFilter):
    """
    This filter is being used in django admin panel in profile model.
    """
    title = 'Активные/архивные товары'
    parameter_name = 'archive'

    def choices(self, changelist):
        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string(remove=[self.parameter_name]),
            'display': _('Все'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == str(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }

    def lookups(self, request, model_admin):
        return (
            ('archive', 'Архивные'),
            ('non_archive', 'Активные')
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value() == 'archive':
            return queryset.filter(archive=True)
        elif self.value() == 'non_archive':
            return queryset.filter(archive=False)
