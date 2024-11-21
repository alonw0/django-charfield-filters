from django.test import TestCase, RequestFactory
from django.contrib import admin
from django.db import models
from django.http import HttpRequest
from .filters import (
    create_charfield_select_filter,
    create_charfield_autocomplete_filter,
    create_charfield_autocomplete_select_filter
)
from .admin import CharFieldFilterMixin, CharFieldFilterAdmin


class TestModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    class Meta:
        app_label = 'charfield_filters'


class TestSelectAdmin(CharFieldFilterAdmin):
    charfield_filter_fields = ['name', 'description']
    charfield_filter_type = 'select'


class TestAutocompleteAdmin(CharFieldFilterAdmin):
    charfield_filter_fields = ['name', 'description']
    charfield_filter_type = 'autocomplete'


class TestAutocompleteSelectAdmin(CharFieldFilterAdmin):
    charfield_filter_fields = ['name', 'description']
    charfield_filter_type = 'autocomplete_select'


class CharFieldFiltersTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.select_admin = TestSelectAdmin(TestModel, admin.site)
        self.autocomplete_admin = TestAutocompleteAdmin(TestModel, admin.site)
        self.autocomplete_select_admin = TestAutocompleteSelectAdmin(TestModel, admin.site)
        
        # Create test data
        TestModel.objects.create(name='Test1', description='Description 1')
        TestModel.objects.create(name='Test2', description='Description 2')
        TestModel.objects.create(name='Test3', description='Description 3')

    def test_select_filter(self):
        request = self.factory.get('/')
        
        # Create a filter instance using the factory function
        SelectFilter = create_charfield_select_filter('name')
        filter_instance = SelectFilter(
            request, {'name__exact': 'Test1'}, TestModel, self.select_admin
        )
        
        # Test filter choices
        choices = filter_instance.lookups(request, self.select_admin)
        self.assertEqual(len(choices), 3)
        self.assertIn(('Test1', 'Test1'), choices)
        
        # Test queryset filtering
        queryset = TestModel.objects.all()
        filtered_qs = filter_instance.queryset(request, queryset)
        self.assertEqual(filtered_qs.count(), 1)
        self.assertEqual(filtered_qs.first().name, 'Test1')

    def test_autocomplete_filter(self):
        request = self.factory.get('/')
        
        # Create a filter instance using the factory function
        AutocompleteFilter = create_charfield_autocomplete_filter('name')
        filter_instance = AutocompleteFilter(
            request, {'name__icontains': 'Test'}, TestModel, self.autocomplete_admin
        )
        
        # Test queryset filtering
        queryset = TestModel.objects.all()
        filtered_qs = filter_instance.queryset(request, queryset)
        self.assertEqual(filtered_qs.count(), 3)  # All test items contain 'Test'
        
        # Test partial match
        filter_instance = AutocompleteFilter(
            request, {'name__icontains': 'Test1'}, TestModel, self.autocomplete_admin
        )
        filtered_qs = filter_instance.queryset(request, queryset)
        self.assertEqual(filtered_qs.count(), 1)
        self.assertEqual(filtered_qs.first().name, 'Test1')

    def test_autocomplete_select_filter(self):
        request = self.factory.get('/')
        
        # Create a filter instance using the factory function
        AutocompleteSelectFilter = create_charfield_autocomplete_select_filter('name')
        
        # Test exact match (dropdown selection)
        filter_instance = AutocompleteSelectFilter(
            request, {'name__exact': 'Test1'}, TestModel, self.autocomplete_select_admin
        )
        queryset = TestModel.objects.all()
        filtered_qs = filter_instance.queryset(request, queryset)
        self.assertEqual(filtered_qs.count(), 1)
        self.assertEqual(filtered_qs.first().name, 'Test1')
        
        # Test filter choices
        choices = filter_instance.lookups(request, self.autocomplete_select_admin)
        self.assertEqual(len(choices), 3)
        self.assertIn(('Test1', 'Test1'), choices)
        
        # Test template
        self.assertEqual(
            filter_instance.template,
            'admin/charfield_filters/autocomplete_select_filter.html'
        )

    def test_admin_mixin_select(self):
        request = self.factory.get('/')
        list_filter = self.select_admin.get_list_filter(request)
        
        # Test that both fields are included in list_filter
        self.assertEqual(len(list_filter), 2)
        
        # Test filter class names
        self.assertEqual(list_filter[0].__name__, 'NameSelectFilter')
        self.assertEqual(list_filter[1].__name__, 'DescriptionSelectFilter')

    def test_admin_mixin_autocomplete(self):
        request = self.factory.get('/')
        list_filter = self.autocomplete_admin.get_list_filter(request)
        
        # Test that both fields are included in list_filter
        self.assertEqual(len(list_filter), 2)
        
        # Test filter class names
        self.assertEqual(list_filter[0].__name__, 'NameAutocompleteFilter')
        self.assertEqual(list_filter[1].__name__, 'DescriptionAutocompleteFilter')

    def test_admin_mixin_autocomplete_select(self):
        request = self.factory.get('/')
        list_filter = self.autocomplete_select_admin.get_list_filter(request)
        
        # Test that both fields are included in list_filter
        self.assertEqual(len(list_filter), 2)
        
        # Test filter class names
        self.assertEqual(list_filter[0].__name__, 'NameAutocompleteSelectFilter')
        self.assertEqual(list_filter[1].__name__, 'DescriptionAutocompleteSelectFilter')
