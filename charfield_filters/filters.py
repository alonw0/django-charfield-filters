from typing import Any, Optional, Tuple, Type, List
from django.contrib import admin
from django.contrib.admin import ListFilter, SimpleListFilter
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _


def create_charfield_filter(field_name: str, filter_type: str = 'select') -> Type[ListFilter]:
    """
    Creates a filter class for a specific field.
    
    Args:
        field_name: Name of the field to filter on
        filter_type: Type of filter ('select', 'autocomplete', or 'autocomplete_select')
    """
    class DynamicCharFieldFilter(SimpleListFilter):
        title = _(field_name.replace('_', ' ').title())
        parameter_name = field_name

        @property
        def template(self):
            templates = {
                'select': 'admin/charfield_filters/dropdown_filter.html',
                'autocomplete': 'admin/charfield_filters/autocomplete_filter.html',
                'autocomplete_select': 'admin/charfield_filters/autocomplete_select_filter.html'
            }
            return templates.get(filter_type, templates['select'])

        def __init__(self, request: HttpRequest, params: dict, model: Any, model_admin: admin.ModelAdmin):
            super().__init__(request, params, model, model_admin)
            self._model_admin = model_admin
            self._request = request

        def has_output(self) -> bool:
            """Always show the filter."""
            return True

        def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin) -> List[Tuple[str, str]]:
            """Get unique values for dropdown."""
            if filter_type in ['select', 'autocomplete_select']:
                values = (
                    model_admin.model._default_manager.distinct()
                    .order_by(field_name)
                    .values_list(field_name, flat=True)
                )
                return [(str(val), str(val)) for val in values if val is not None]
            # For autocomplete, return a dummy value to ensure filter is shown
            return [('', _('All'))]

        def queryset(self, request: HttpRequest, queryset: QuerySet) -> Optional[QuerySet]:
            """Filter the queryset based on selected value."""
            value = self.value()
            if not value:
                return queryset

            if filter_type == 'autocomplete':
                return queryset.filter(**{f"{field_name}__icontains": value})
            return queryset.filter(**{field_name: value})

        def choices(self, changelist):
            """Return choices for the filter."""
            yield {
                'selected': self.value() is None,
                'query_string': changelist.get_query_string(remove=[self.parameter_name]),
                'display': _('All')
            }
            
            if filter_type in ['select', 'autocomplete_select']:
                for lookup, title in self.lookups(self._request, self._model_admin):
                    if lookup:  # Don't yield empty values
                        yield {
                            'selected': str(self.value()) == str(lookup),
                            'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                            'display': title
                        }
            elif self.value():  # For autocomplete, show current value if set
                yield {
                    'selected': True,
                    'query_string': changelist.get_query_string({self.parameter_name: self.value()}),
                    'display': self.value()
                }

        def expected_parameters(self):
            """Return the expected parameters for this filter."""
            return [self.parameter_name]

        def value(self):
            """Get the current value from the request."""
            return self._request.GET.get(self.parameter_name)

    return DynamicCharFieldFilter
