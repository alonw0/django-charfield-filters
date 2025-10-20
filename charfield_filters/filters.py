"""
Django CharField Filters - Filter Classes

This module provides the core filtering functionality for CharField fields in Django admin.
It includes the factory function for creating dynamic filter classes that support three
different filter types: select, autocomplete, and autocomplete_select.

Classes:
    DynamicCharFieldFilter: A dynamically-created SimpleListFilter subclass (internal)

Functions:
    create_charfield_filter: Factory function to create filter classes for CharField fields

Usage:
    >>> from charfield_filters.filters import create_charfield_filter
    >>>
    >>> class MyModelAdmin(admin.ModelAdmin):
    ...     list_filter = [
    ...         create_charfield_filter('category', 'autocomplete_select'),
    ...     ]
"""
from typing import Any, Optional, Tuple, Type, List
from django.contrib import admin
from django.contrib.admin import ListFilter, SimpleListFilter
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _


def create_charfield_filter(field_name: str, filter_type: str = 'select') -> Type[ListFilter]:
    """
    Factory function that creates a custom filter class for a specific CharField.

    This function dynamically generates a ListFilter subclass configured for the
    specified field and filter type. The returned class can be added to a ModelAdmin's
    list_filter to enable filtering on that field.

    Args:
        field_name: The name of the CharField to create a filter for. Must match
            a field name in the model exactly.
        filter_type: The type of filter interface to create. Options:
            - 'select': Classic dropdown with all unique values
            - 'autocomplete': Search box with type-to-filter
            - 'autocomplete_select': Searchable dropdown (recommended)
            Default: 'select'

    Returns:
        A dynamically created ListFilter subclass (DynamicCharFieldFilter) configured
        for the specified field and filter type.

    Example:
        >>> # Direct usage in list_filter
        >>> class BookAdmin(admin.ModelAdmin):
        ...     list_filter = [
        ...         create_charfield_filter('author', 'select'),
        ...         create_charfield_filter('genre', 'autocomplete_select'),
        ...     ]

    Note:
        - The filter title is automatically generated from the field name
        - Field names with underscores are converted to title case (e.g., 'first_name' -> 'First Name')
        - Non-existent fields will cause Django to raise FieldDoesNotExist at runtime
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
            """
            Determines whether the filter should be displayed in the admin sidebar.

            Returns:
                Always returns True to ensure the filter is always visible,
                even when there are no values to filter.
            """
            return True

        def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin) -> List[Tuple[str, str]]:
            """
            Returns the list of tuples for filter choices.

            For 'select' and 'autocomplete_select' filter types, this queries the
            database for all distinct values of the field. For 'autocomplete' type,
            it returns a dummy value to ensure the filter is shown.

            Args:
                request: The current HTTP request object.
                model_admin: The ModelAdmin instance for the filtered model.

            Returns:
                A list of (value, display) tuples representing available filter options.
                For 'select' and 'autocomplete_select': all unique field values sorted.
                For 'autocomplete': a single dummy tuple [('', 'All')].

            Note:
                Values are retrieved using distinct().order_by() for optimal database performance.
                NULL values are automatically excluded from the results.
            """
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
            """
            Filters the queryset based on the selected filter value.

            Args:
                request: The current HTTP request object.
                queryset: The base queryset to filter.

            Returns:
                The filtered queryset if a value is selected, or the original
                queryset if no filter value is present.

            Note:
                - For 'autocomplete' filter: uses case-insensitive partial matching (__icontains)
                - For 'select' and 'autocomplete_select': uses exact matching
            """
            value = self.value()
            if not value:
                return queryset

            if filter_type == 'autocomplete':
                return queryset.filter(**{f"{field_name}__icontains": value})
            return queryset.filter(**{field_name: value})

        def choices(self, changelist):
            """
            Generates the list of choices for rendering the filter in the admin sidebar.

            This method is called by Django's admin to render the filter UI. It yields
            dictionaries containing information about each filter choice, including
            whether it's selected and the query string for that choice.

            Args:
                changelist: The ChangeList instance managing the admin list view.

            Yields:
                Dictionaries with keys:
                - 'selected': Boolean indicating if this choice is currently active
                - 'query_string': URL query string to apply this filter
                - 'display': The display text for this choice

            Note:
                The first yielded choice is always 'All' to allow clearing the filter.
            """
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
            """
            Returns the list of expected URL parameters for this filter.

            This method tells Django's admin which URL parameters this filter
            will use, allowing proper handling of multiple filters.

            Returns:
                A list containing the single parameter name used by this filter.
            """
            return [self.parameter_name]

        def value(self):
            """
            Retrieves the current filter value from the request's GET parameters.

            Returns:
                The filter value as a string if present in the URL, or None
                if no filter is applied.

            Example:
                For URL: /admin/myapp/mymodel/?author=Smith
                Returns: 'Smith' (if parameter_name is 'author')
            """
            return self._request.GET.get(self.parameter_name)

    return DynamicCharFieldFilter
