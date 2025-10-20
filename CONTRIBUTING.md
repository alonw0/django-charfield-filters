# Contributing to Django CharField Filters

Thank you for your interest in contributing to Django CharField Filters! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow:

- Be respectful and inclusive
- Welcome newcomers and encourage diverse perspectives
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/django-charfield-filters.git
   cd django-charfield-filters
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/alonw0/django-charfield-filters.git
   ```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Django 4.2.0 or higher
- pip and virtualenv

### Setting Up Your Development Environment

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install the package in development mode**:
   ```bash
   pip install -e .
   ```

3. **Install Django** (if not already installed):
   ```bash
   pip install Django>=4.2.0
   ```

4. **Run tests** to ensure everything is working:
   ```bash
   python -m django test charfield_filters.tests --settings=charfield_filters.tests
   ```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues reported in the issue tracker
- **Features**: Add new filter types or functionality
- **Documentation**: Improve README, docstrings, or add examples
- **Tests**: Increase test coverage or add edge case tests
- **Performance**: Optimize queries or rendering
- **Code quality**: Refactoring, type hints, or code cleanup

### Contribution Workflow

1. **Check existing issues** to see if your contribution is already being worked on
2. **Create an issue** if you're planning a significant change (for discussion)
3. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number-description
   ```
4. **Make your changes** following our coding standards
5. **Write or update tests** for your changes
6. **Update documentation** if needed
7. **Commit your changes** with clear commit messages
8. **Push to your fork** and submit a pull request

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use meaningful variable and function names
- Keep functions small and focused on a single task
- Add docstrings to all public functions and classes

### Type Hints

Use type hints for function parameters and return values:

```python
from typing import List, Tuple, Optional

def create_charfield_filter(field_name: str, filter_type: str = 'select') -> Type[ListFilter]:
    """
    Creates a filter class for a specific field.

    Args:
        field_name: Name of the field to filter on
        filter_type: Type of filter ('select', 'autocomplete', or 'autocomplete_select')

    Returns:
        A ListFilter subclass configured for the specified field
    """
    ...
```

### Documentation

- Add docstrings to all public classes and methods
- Use Google-style or NumPy-style docstring format
- Include examples in docstrings where appropriate
- Update README.md if adding new features

### HTML/JavaScript

- Follow Django template conventions
- Use vanilla JavaScript (no jQuery or other dependencies)
- Ensure dark mode compatibility
- Test across major browsers (Chrome, Firefox, Safari)

## Testing

### Running Tests

Run the test suite:

```bash
python -m django test charfield_filters.tests --settings=charfield_filters.tests
```

### Writing Tests

- Add tests for all new features
- Include edge cases and error conditions
- Test all three filter types (select, autocomplete, autocomplete_select)
- Ensure tests pass before submitting PR

Example test structure:

```python
from django.test import TestCase
from django.contrib import admin
from .models import TestModel
from .admin import CharFieldFilterAdmin

class CharFieldFilterTestCase(TestCase):
    def setUp(self):
        # Create test data
        pass

    def test_filter_functionality(self):
        # Test your feature
        pass
```

## Submitting Changes

### Pull Request Process

1. **Update your branch** with the latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Ensure all tests pass** and code follows style guidelines

3. **Create a pull request** with:
   - Clear title describing the change
   - Description of what changed and why
   - Reference to related issues (e.g., "Fixes #123")
   - Screenshots for UI changes (if applicable)

4. **Respond to feedback** from maintainers promptly

### Pull Request Guidelines

- Keep PRs focused on a single change
- Write clear commit messages
- Update CHANGELOG with your changes
- Add tests for new functionality
- Ensure backward compatibility unless it's a breaking change

### Commit Message Format

Use clear, descriptive commit messages:

```
Add autocomplete search debouncing

- Implement 300ms debounce for autocomplete filters
- Reduces database queries during typing
- Improves performance for large datasets

Fixes #123
```

## Reporting Bugs

### Before Submitting a Bug Report

- Check the [issue tracker](https://github.com/alonw0/django-charfield-filters/issues) for existing reports
- Verify the bug exists in the latest version
- Try to reproduce the issue in a minimal test case

### Bug Report Guidelines

Include the following information:

- **Django version**: Output of `python -m django --version`
- **Python version**: Output of `python --version`
- **Package version**: Version of django-charfield-filters
- **Steps to reproduce**: Minimal code example
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Error messages**: Full traceback if applicable
- **Browser/OS**: If relevant to the issue

Example:

```markdown
## Bug Description
Autocomplete filter not working with PostgreSQL

## Environment
- Django: 5.0
- Python: 3.11
- Package: 0.1.3
- Database: PostgreSQL 14

## Steps to Reproduce
1. Configure filter with autocomplete_select
2. Type in search box
3. No results appear

## Expected
Should show filtered results

## Actual
Empty results, console error: [error message]
```

## Feature Requests

We welcome feature requests! When submitting:

1. **Check existing issues** to avoid duplicates
2. **Describe the feature** clearly and concisely
3. **Explain the use case** and why it's valuable
4. **Provide examples** of how it would work
5. **Consider backward compatibility**

### Feature Request Template

```markdown
## Feature Description
Brief description of the feature

## Motivation
Why is this feature needed?

## Proposed Solution
How should this feature work?

## Example Usage
```python
# Code example showing usage
```

## Alternatives Considered
Other approaches you've thought about
```

## Release Process

(For maintainers)

1. Update version in `setup.py` and `pyproject.toml`
2. Update `CHANGELOG` with release notes
3. Create a new git tag: `git tag v0.x.x`
4. Push tags: `git push --tags`
5. Build and upload to PyPI:
   ```bash
   python setup.py sdist bdist_wheel
   twine upload dist/*
   ```

## Questions?

If you have questions about contributing, feel free to:

- Open an issue for discussion
- Contact the maintainers
- Check the README.md for documentation

Thank you for contributing to Django CharField Filters!
