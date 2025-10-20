"""
Django CharField Filters - Admin Classes

This module provides admin classes and mixins for easily adding CharField filters
to Django admin interfaces. It includes both a mixin for flexibility and a ready-to-use
ModelAdmin class for convenience.

Classes:
    CharFieldFilterMixin: Mixin that adds CharField filtering to any ModelAdmin
    CharFieldFilterAdmin: Ready-to-use ModelAdmin with CharField filtering built-in

Usage:
    >>> from charfield_filters.admin import CharFieldFilterAdmin
    >>>
    >>> @admin.register(MyModel)
    ... class MyModelAdmin(CharFieldFilterAdmin):
    ...     charfield_filter_fields = ['category', 'status']
    ...     charfield_filter_type = 'autocomplete_select'
"""
from typing import Type, Tuple, Any
from django.contrib import admin
from django.db import models
from django.http import HttpRequest

from .filters import create_charfield_filter


class CharFieldFilterMixin:
    """
    A mixin that adds CharField filtering capabilities to Django ModelAdmin classes.

    This mixin dynamically creates filters for specified CharField fields and adds them
    to the admin's list_filter. It supports three filter types: select, autocomplete,
    and autocomplete_select.

    Attributes:
        charfield_filter_fields: List of CharField field names to create filters for.
            Only fields that exist in the model and are CharField instances will be processed.
        charfield_filter_type: Type of filter to use for all specified fields.
            Options: 'select', 'autocomplete', or 'autocomplete_select'.
            Default: 'select'
        list_filter: Base list_filter tuple that will be extended with CharField filters.
            Default: ()

    Example:
        >>> class BookAdmin(CharFieldFilterMixin, admin.ModelAdmin):
        ...     charfield_filter_fields = ['author', 'genre']
        ...     charfield_filter_type = 'autocomplete_select'
        ...     list_display = ['title', 'author', 'genre']

    Note:
        The mixin should be listed before admin.ModelAdmin in the inheritance chain
        to ensure proper method resolution order.
    """
    charfield_filter_fields: list[str] = []  # Fields to apply the filters to
    charfield_filter_type: str = 'select'    # 'select', 'autocomplete', or 'autocomplete_select'
    list_filter: Tuple[Any, ...] = ()        # Default list_filter value

    def get_list_filter(self, request: HttpRequest) -> tuple:
        """
        Dynamically adds CharField filters to the list_filter tuple.

        This method intercepts the standard get_list_filter call to inject
        dynamically-created filter classes for each field specified in
        charfield_filter_fields. Only CharField fields that exist in the model
        are processed; invalid fields are silently skipped.

        Args:
            request: The current HTTP request object.

        Returns:
            A tuple of filter classes including both the base filters and
            dynamically-created CharField filters.

        Note:
            This method validates each field against the model's meta to ensure
            it exists and is a CharField before creating a filter for it.
        """
        # Get base list_filter value
        base_filters = list(super().get_list_filter(request) or [])

        # Add CharField filters
        for field_name in self.charfield_filter_fields:
            try:
                # Get the actual field from the model
                field = self.model._meta.get_field(field_name)
                if isinstance(field, models.CharField):
                    # Create and add the filter
                    filter_class = create_charfield_filter(field_name, self.charfield_filter_type)
                    base_filters.append(filter_class)
            except models.FieldDoesNotExist:
                continue

        return tuple(base_filters)


class CharFieldFilterAdmin(CharFieldFilterMixin, admin.ModelAdmin):
    """
    A ready-to-use ModelAdmin class that includes CharField filtering capabilities.

    This is a convenience class that combines CharFieldFilterMixin with Django's
    ModelAdmin. Use this when you don't need to inherit from other admin classes.

    Attributes:
        charfield_filter_fields: List of CharField field names to create filters for.
        charfield_filter_type: Type of filter ('select', 'autocomplete', or 'autocomplete_select').

    Example:
        >>> from django.contrib import admin
        >>> from charfield_filters.admin import CharFieldFilterAdmin
        >>> from .models import Book
        >>>
        >>> @admin.register(Book)
        ... class BookAdmin(CharFieldFilterAdmin):
        ...     list_display = ['title', 'author', 'genre']
        ...     charfield_filter_fields = ['author', 'genre']
        ...     charfield_filter_type = 'autocomplete_select'

    Note:
        If you need to combine with other admin mixins, use CharFieldFilterMixin
        directly instead of this class.
    """
    pass
