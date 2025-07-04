# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django-Tailwind is a Python package that integrates Tailwind CSS with Django applications. It provides management commands, template tags, and utilities to streamline Tailwind CSS development within Django projects.

## Development Commands

### Testing
```bash
# Run all tests
poetry run tox

# Run tests with pytest directly
poetry run pytest

# Run specific test file
poetry run pytest tests/test_cli.py
```

### Code Quality
```bash
# Format code with black
poetry run black .

# Sort imports with isort
poetry run isort .

# Check code style with flake8
poetry run flake8
```

### Documentation
```bash
# Build documentation
make docs
```

### Package Management
```bash
# Install dependencies
poetry install

# Update dependencies
poetry update

# Build package
poetry build
```

### Example App Development
The `example/` directory contains a Django project with Tailwind setup:

```bash
# Navigate to example directory
cd example/

# Install Node.js dependencies for Tailwind
python manage.py tailwind install

# Start Tailwind development server (watches for changes)
python manage.py tailwind start

# Start both Django server and Tailwind watcher simultaneously
python manage.py tailwind dev

# Build production CSS
python manage.py tailwind build
```

## Architecture

### Core Components

- **Management Command** (`src/tailwind/management/commands/tailwind.py`):
  - Main entry point for all Tailwind operations
  - Handles `init`, `install`, `build`, `start`, `dev`, `check-updates`, `update` commands
  - Uses cookiecutter templates for app initialization
  - `dev` command runs Django server and Tailwind watcher simultaneously using Honcho

- **NPM Integration** (`src/tailwind/npm.py`):
  - Wrapper around npm commands
  - Handles subprocess execution for Node.js operations

- **Template Tags** (`src/tailwind/templatetags/tailwind_tags.py`):
  - `{% tailwind_css %}` - Includes Tailwind CSS in templates
  - `{% tailwind_preload_css %}` - Preloads CSS for performance
  - Automatically appends cache-busting parameters in DEBUG mode

- **Utilities** (`src/tailwind/utils.py`):
  - Helper functions for path resolution
  - Package.json manipulation
  - Dynamic pip package installation

### App Templates

Two cookiecutter templates are provided:
- `app_template_v3/` - For Tailwind CSS v3
- `app_template_v4/` - For Tailwind CSS v4

These templates generate Django apps with:
- `static_src/` directory for source files
- `package.json` with build scripts
- PostCSS configuration
- Base HTML template

### Configuration

The package uses Django settings for configuration:
- `TAILWIND_APP_NAME` - Name of the Tailwind app
- `TAILWIND_CSS_PATH` - Path to compiled CSS
- `TAILWIND_DEV_MODE` - Development mode flag
- `NPM_BIN_PATH` - Custom npm binary path

## Common Development Patterns

### Adding New Management Commands
Extend the `handle_*_command` pattern in `tailwind.py:73` following the existing command structure.

### Template Tag Development
Template tags use inclusion tags pattern with templates in `src/tailwind/templates/tailwind/tags/`.

### Testing
Tests are located in `tests/` directory and use pytest-django. The test suite includes:
- CLI command testing
- Template tag functionality
- Configuration validation

## Package Structure

```
src/tailwind/
├── management/commands/tailwind.py  # Main management command
├── templatetags/tailwind_tags.py    # Django template tags
├── apps.py                         # Django app configuration
├── npm.py                          # NPM command wrapper
├── utils.py                        # Utility functions
├── validate.py                     # Configuration validation
└── templates/                      # Template tag templates
```

## Testing Guidelines

### BDD-Style Test Documentation

All tests should use BDD-style docstrings following the GIVEN-WHEN-THEN format:

```python
def test_example_functionality(settings):
    """
    GIVEN a specific initial state or configuration
    WHEN a particular action is performed
    THEN the expected outcome should occur
    """
    # Test implementation
```

### Test Categories

**Integration Tests**: Test real functionality with minimal mocking
- Focus on actual file operations, command execution, and system integration
- Use temporary directories for file system tests
- Mock only external dependencies that would cause tests to hang or fail

**Unit Tests**: Test individual components in isolation
- Template tag rendering and output
- Configuration validation
- String formatting and parsing

### Test Patterns

- Use `tempfile.TemporaryDirectory()` for file system tests
- Mock `subprocess.run` only when necessary to prevent external command execution
- Use real Django management command testing with `call_command()`
- Clean up test artifacts with helper functions like `cleanup_theme_app_dir()`

### Example Test Structure

```python
def test_command_creates_files(settings):
    """
    GIVEN a Django project with Tailwind configured
    WHEN the tailwind init command is run
    THEN the necessary files and directories should be created
    """
    # Setup
    app_name = f'test_theme_{str(uuid.uuid1()).replace("-", "_")}'

    # Action
    call_command("tailwind", "init", "--app-name", app_name, "--no-input")

    # Assertions
    assert os.path.exists(expected_file_path)

    # Cleanup
    cleanup_theme_app_dir(app_name)
```

The package follows Django's standard app structure and uses Poetry for dependency management.
