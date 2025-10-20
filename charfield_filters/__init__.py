"""
Django CharField Filters

A reusable Django app that provides advanced admin filters for CharField fields,
including both dropdown select and autocomplete functionality.

This package makes it easy to add powerful, user-friendly filtering capabilities
to your Django admin interface for CharField fields. It supports three filter types:

- **Select**: Classic dropdown with all unique values
- **Autocomplete**: Search box with type-to-filter functionality
- **Autocomplete Select**: Searchable dropdown combining both approaches (recommended)

Quick Start:
    >>> from django.contrib import admin
    >>> from charfield_filters.admin import CharFieldFilterAdmin
    >>>
    >>> @admin.register(MyModel)
    ... class MyModelAdmin(CharFieldFilterAdmin):
    ...     charfield_filter_fields = ['category', 'status']
    ...     charfield_filter_type = 'autocomplete_select'

For more information, see: https://github.com/alonw0/django-charfield-filters
"""

__version__ = "0.1.3"
__author__ = "Alon Wolenitz"
__license__ = "MIT"

# Expose main classes for convenient imports
from .admin import CharFieldFilterAdmin, CharFieldFilterMixin
from .filters import create_charfield_filter

__all__ = [
    'CharFieldFilterAdmin',
    'CharFieldFilterMixin',
    'create_charfield_filter',
]
