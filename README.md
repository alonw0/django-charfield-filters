# Django CharField Filters

[![PyPI](https://img.shields.io/pypi/v/django-charfield-filters)](https://pypi.org/project/django-charfield-filters)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-charfield-filters)
![Django Version](https://img.shields.io/badge/django-4.2%20%7C%205.0%20%7C%205.1-%2344B78B?labelColor=%23092E20)
<!-- https://shields.io/badges -->
<!-- django-4.2 | 5.0 | 5.1-#44B78B -->
<!-- labelColor=%23092E20 -->

A reusable Django app that provides advanced admin filters for CharField fields, including both dropdown select and autocomplete functionality.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Using the Mixin](#using-the-mixin)
  - [Filter Types](#filter-types)
- [Configuration](#configuration)
- [Examples](#examples)
  - [Complete Example with Multiple Models](#complete-example-with-multiple-models)
  - [Using Different Filter Types](#using-different-filter-types)
  - [Combining with Other Filters](#combining-with-other-filters)
- [How It Works](#how-it-works)
- [Performance Considerations](#performance-considerations)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Features

- Easy-to-use filters for CharField fields in Django admin
- Three filter types:
  - Select: Dropdown with all unique values
  - Autocomplete: Type-to-search functionality
  - Autocomplete Select: Hybrid filter combining dropdown and search
- User-friendly interface with clear button for quick filter removal
- Dynamic filtering as you type
- Automatic title generation from field names
- Cached lookups for better performance
- Compatible with Django 4.2.0+

## Installation

Install from PyPI using pip:

```bash
pip install django-charfield-filters
```

Add `charfield_filters` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'charfield_filters',
    ...
]
```

That's it! No database migrations or additional configuration needed.

## Quick Start

Here's a minimal example to get you started in 30 seconds:

```python
# models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)

# admin.py
from django.contrib import admin
from charfield_filters.admin import CharFieldFilterAdmin
from .models import Product

@admin.register(Product)
class ProductAdmin(CharFieldFilterAdmin):
    list_display = ['name', 'category', 'brand']
    charfield_filter_fields = ['category', 'brand']
    charfield_filter_type = 'autocomplete_select'
```

Now you have searchable dropdown filters for `category` and `brand` in your Django admin!

## Usage

### Basic Usage

```python
from django.contrib import admin
from charfield_filters.admin import CharFieldFilterAdmin

@admin.register(YourModel)
class YourModelAdmin(CharFieldFilterAdmin):
    list_display = ['name', 'category']  # Fields to display
    charfield_filter_fields = ['name', 'category']  # Fields to filter
    charfield_filter_type = 'autocomplete_select'  # 'select', 'autocomplete', or 'autocomplete_select'
```

### Using the Mixin

If you need to combine with other admin classes:

```python
from django.contrib import admin
from charfield_filters.admin import CharFieldFilterMixin

@admin.register(YourModel)
class YourModelAdmin(CharFieldFilterMixin, admin.ModelAdmin):
    list_display = ['name', 'category']
    charfield_filter_fields = ['name', 'category']
    charfield_filter_type = 'autocomplete_select'
```

### Filter Types

Choose the filter type that best matches your data and use case:

#### 1. Select Filter (`charfield_filter_type = 'select'`)

Classic dropdown filter with all available options.

```python
charfield_filter_type = 'select'
```

**When to use:**
- Fields with 2-20 unique values (e.g., status, priority, type)
- When users need to see all available options at a glance
- When exact matching is required

**Features:**
- Shows all unique values in a dropdown
- Provides exact matching
- Minimal UI, no search functionality

#### 2. Autocomplete Filter (`charfield_filter_type = 'autocomplete'`)

Search box with type-to-filter functionality.

```python
charfield_filter_type = 'autocomplete'
```

**When to use:**
- Fields with many unique values (e.g., product names, user emails)
- When users know what they're searching for
- When you want case-insensitive partial matching

**Features:**
- Text input with search functionality
- Case-insensitive partial matching (uses `__icontains`)
- No dropdown, pure search interface
- Dynamic filtering as you type

#### 3. Autocomplete Select Filter (`charfield_filter_type = 'autocomplete_select'`) - Recommended

Hybrid filter combining dropdown and search functionality.

```python
charfield_filter_type = 'autocomplete_select'
```

**When to use:**
- Most use cases (this is the recommended default)
- Fields with 5-100 unique values
- When users might want to browse OR search
- When you want the best user experience

**Features:**
- Searchable dropdown with all options visible
- Clear button (×) for quick filter removal
- Supports both browsing and searching
- Best of both worlds: discovery + search

## Configuration

### Admin Class Options

- `charfield_filter_fields`: List of CharField field names to create filters for
- `charfield_filter_type`: Type of filter to use ('select', 'autocomplete', or 'autocomplete_select')

## Examples

### Complete Example with Multiple Models

```python
# models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    publisher = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)

    def __str__(self):
        return self.title

class Magazine(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    frequency = models.CharField(max_length=50)  # monthly, weekly, etc.

    def __str__(self):
        return self.name

# admin.py
from django.contrib import admin
from charfield_filters.admin import CharFieldFilterAdmin
from .models import Book, Magazine

@admin.register(Book)
class BookAdmin(CharFieldFilterAdmin):
    list_display = ['title', 'author', 'genre', 'publisher']
    charfield_filter_fields = ['author', 'genre', 'publisher']
    charfield_filter_type = 'autocomplete_select'
    search_fields = ['title', 'isbn']

@admin.register(Magazine)
class MagazineAdmin(CharFieldFilterAdmin):
    list_display = ['name', 'category', 'frequency']
    charfield_filter_fields = ['category', 'frequency']
    charfield_filter_type = 'select'  # Use simple dropdown for limited values
```

### Using Different Filter Types

You can mix this package with other admin features:

```python
from django.contrib import admin
from charfield_filters.admin import CharFieldFilterAdmin

@admin.register(Employee)
class EmployeeAdmin(CharFieldFilterAdmin):
    list_display = ['name', 'department', 'position', 'status', 'hire_date']

    # CharField filters from this package
    charfield_filter_fields = ['department', 'position']
    charfield_filter_type = 'autocomplete_select'

    # Other standard admin features work normally
    search_fields = ['name', 'email']
    date_hierarchy = 'hire_date'
    ordering = ['-hire_date']
```

### Combining with Other Filters

The mixin works seamlessly with Django's built-in filters:

```python
from django.contrib import admin
from charfield_filters.admin import CharFieldFilterMixin

class OrderAdmin(CharFieldFilterMixin, admin.ModelAdmin):
    list_display = ['order_id', 'customer', 'status', 'total', 'created_at']

    # CharField filters for text fields
    charfield_filter_fields = ['status', 'customer']
    charfield_filter_type = 'autocomplete_select'

    # Standard Django filters for other field types
    list_filter = [
        'created_at',  # Date filter
        'is_paid',     # Boolean filter
    ]
```

## How It Works

This package extends Django's admin filtering system by:

1. **Dynamic Filter Creation**: The `CharFieldFilterMixin` intercepts the `get_list_filter()` method and dynamically creates filter classes for specified CharField fields.

2. **Custom Templates**: Each filter type uses a custom HTML template with JavaScript for enhanced functionality (autocomplete, search, clear buttons).

3. **Efficient Querying**: Filters query the database for distinct values only when needed, with results cached per request.

4. **Field Validation**: Only actual CharField fields from your model are processed; non-existent fields are silently skipped.

**Under the hood:**
- `select` filter: Uses exact matching (`field_name=value`)
- `autocomplete` filter: Uses case-insensitive partial matching (`field_name__icontains=value`)
- `autocomplete_select` filter: Combines both approaches with JavaScript-enhanced UI

## Performance Considerations

### Query Optimization

The package executes a distinct query for each filtered field to populate dropdown options:

```python
model._default_manager.distinct().order_by(field_name).values_list(field_name, flat=True)
```

**Tips for optimal performance:**

1. **Add Database Indexes**: Index CharField fields that you filter frequently
   ```python
   class Product(models.Model):
       category = models.CharField(max_length=100, db_index=True)
       brand = models.CharField(max_length=100, db_index=True)
   ```

2. **Choose the Right Filter Type**:
   - Use `select` for fields with <20 unique values (single query)
   - Use `autocomplete` for fields with >100 unique values (no initial query)
   - Use `autocomplete_select` for everything in between

3. **Limit Filtered Fields**: Only add filters for fields users actually need

4. **Monitor Query Count**: Use Django Debug Toolbar to monitor the impact of filters on your query count

### Database Impact

- **`select` and `autocomplete_select`**: One additional query per field per page load
- **`autocomplete`**: No additional queries until user starts typing
- **Caching**: Distinct values are fetched once per request and reused

## Troubleshooting

### Filters not appearing in admin

**Problem**: Added `charfield_filter_fields` but filters don't show up.

**Solutions**:
1. Verify `charfield_filters` is in `INSTALLED_APPS`
2. Check that field names in `charfield_filter_fields` match your model exactly
3. Ensure the fields are actually `CharField` instances (not `TextField`, `ForeignKey`, etc.)
4. Clear your browser cache and restart the development server

### FieldDoesNotExist error

**Problem**: `FieldDoesNotExist: MyModel has no field named 'xyz'`

**Solution**: Double-check spelling of field names in `charfield_filter_fields`. The package silently skips non-existent fields, but errors may appear if there's a typo in related configuration.

### Filters showing but not filtering

**Problem**: Filters appear but selecting values doesn't filter the results.

**Solutions**:
1. Check browser console for JavaScript errors
2. Ensure you're not overriding `get_queryset()` in a way that ignores URL parameters
3. Verify the field values in your database actually match the filter options

### Autocomplete search not working

**Problem**: Typing in autocomplete filter doesn't show results or filter.

**Solutions**:
1. Verify JavaScript is enabled in the browser
2. Check that the template files are being loaded (look for 404s in browser dev tools)
3. Ensure there are no JavaScript conflicts with other admin customizations

### Performance issues with large datasets

**Problem**: Admin loads slowly with many filters.

**Solutions**:
1. Add database indexes to filtered fields
2. Switch from `autocomplete_select` to `autocomplete` for fields with many values
3. Reduce the number of `charfield_filter_fields`
4. Consider pagination settings in Django admin

## FAQ

### Can I use different filter types for different fields?

Not directly with the current version. The `charfield_filter_type` applies to all fields in `charfield_filter_fields`. If you need different types, you can:

```python
from charfield_filters.filters import create_charfield_filter

class MyAdmin(admin.ModelAdmin):
    list_filter = [
        create_charfield_filter('category', 'select'),
        create_charfield_filter('brand', 'autocomplete_select'),
    ]
```

### Does this work with TextField?

No, this package is specifically designed for CharField fields. TextFields are typically too long and varied to filter effectively. For TextField filtering, consider using Django's built-in search functionality instead.

### Can I customize the filter template?

Yes! Override the templates in your project:

1. Create a directory: `templates/admin/charfield_filters/`
2. Copy the template you want to customize from the package
3. Modify it to your needs

Template files:
- `dropdown_filter.html` - Select filter
- `autocomplete_filter.html` - Autocomplete filter
- `autocomplete_select_filter.html` - Autocomplete select filter

### Does this support Django's dark mode?

Yes! Version 0.1.3+ includes full dark mode support that automatically adapts to Django's admin dark mode.

### Can I use this with ForeignKey fields?

No, this package is specifically for CharField. For ForeignKey filtering, use Django's built-in `list_filter` with the field name directly, or use `autocomplete_fields` for better UX.

### Is this compatible with other admin packages?

Yes! The `CharFieldFilterMixin` is designed to work alongside other admin mixins and packages. Just ensure you inherit from the mixin before `admin.ModelAdmin`:

```python
class MyAdmin(CharFieldFilterMixin, OtherMixin, admin.ModelAdmin):
    pass
```

### How do I filter on multiple fields at once?

Filters work independently and are automatically combined with AND logic. Users can select values in multiple filters simultaneously, and Django will show only records matching all selected filters.

### Can I programmatically set default filter values?

Yes, you can override `changelist_view` to set default filters:

```python
class MyAdmin(CharFieldFilterAdmin):
    def changelist_view(self, request, extra_context=None):
        if not request.GET:
            from django.http import QueryDict
            q = QueryDict(mutable=True)
            q['status'] = 'active'
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()
        return super().changelist_view(request, extra_context=extra_context)
```

## Requirements

- Python 3.8+
- Django 4.2.0+

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

For more details, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Support

If you have any questions or need help with the package, please open an issue on GitHub.
