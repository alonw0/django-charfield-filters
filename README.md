# Django CharField Filters

A reusable Django app that provides advanced admin filters for CharField fields, including both dropdown select and autocomplete functionality.

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

```bash
pip install django-charfield-filters
```

Add 'charfield_filters' to your INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...
    'charfield_filters',
    ...
]
```

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

1. Select Filter (`charfield_filter_type = 'select'`):
   - Creates a dropdown with all unique values
   - Best for fields with a limited number of unique values
   - Provides exact matching

2. Autocomplete Filter (`charfield_filter_type = 'autocomplete'`):
   - Creates a search input field
   - Best for fields with many unique values
   - Provides case-insensitive partial matching

3. Autocomplete Select Filter (`charfield_filter_type = 'autocomplete_select'`):
   - Combines dropdown and search functionality
   - Shows all options in a searchable dropdown
   - Includes clear button (×) for easy filter removal
   - Best for fields with moderate number of values
   - Supports both browsing and searching

## Configuration

### Admin Class Options

- `charfield_filter_fields`: List of CharField field names to create filters for
- `charfield_filter_type`: Type of filter to use ('select', 'autocomplete', or 'autocomplete_select')

## Example

```python
from django.db import models
from django.contrib import admin
from charfield_filters.admin import CharFieldFilterAdmin

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)

@admin.register(Book)
class BookAdmin(CharFieldFilterAdmin):
    list_display = ['title', 'author', 'genre']
    charfield_filter_fields = ['author', 'genre']  # Add filters for author and genre
    charfield_filter_type = 'autocomplete_select'  # Use hybrid filter for both fields
```

## Requirements

- Python 3.8+
- Django 4.2.0+

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you have any questions or need help with the package, please open an issue on GitHub.
