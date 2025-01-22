from typing import Type, Tuple, Any
from django.contrib import admin
from django.db import models
from django.http import HttpRequest

from .filters import create_charfield_filter


class CharFieldFilterMixin:
    """
    A mixin that adds CharField filtering capabilities to ModelAdmin classes.
    """
    charfield_filter_fields: list[str] = []  # Fields to apply the filters to
    charfield_filter_type: str = 'select'    # 'select' or 'autocomplete'
    list_filter: Tuple[Any, ...] = ()        # Default list_filter value

    def get_list_filter(self, request: HttpRequest) -> tuple:
        """
        Adds CharField filters to the list_filter tuple.
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
    A ready-to-use ModelAdmin that includes CharField filtering.
    """
    pass
