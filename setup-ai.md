# Django-Tailwind AI Agent Setup Guide

> **For Coding Agents**: This guide provides complete installation instructions for django-tailwind with all edge cases covered. Follow steps sequentially and validate each step before proceeding.

## Prerequisites Check

**CRITICAL**: Verify these requirements before starting:

### 1. System Requirements
- [ ] Python >= 3.10 installed
- [ ] Django >= 4.2.20 installed
- [ ] Node.js installed (any recent version)
- [ ] npm available in PATH

### 2. Project Requirements
- [ ] Django project exists and is functional
- [ ] Virtual environment activated (recommended)
- [ ] You have write access to the project directory

### 3. Pre-Installation Validation
```bash
# Verify Python version
python --version

# Verify Django installation
python -c "import django; print(django.VERSION)"

# Verify Node.js/npm
node --version
npm --version

# Test Django project
python manage.py check
```

## Installation Steps

### Step 1: Install Django-Tailwind Package

**Choose installation method:**

#### Option A: Standard Installation
```bash
pip install django-tailwind
```

#### Option B: With Auto-Reload (Recommended)
```bash
pip install 'django-tailwind[reload]'
```

**Validation**: Verify installation:
```bash
python -c "import tailwind; print('django-tailwind installed successfully')"
```

### Step 2: Add to INSTALLED_APPS

**File**: `settings.py`
**Action**: Add `'tailwind'` to INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ... existing apps
    'tailwind',
    # ... other apps
]
```

**Validation**: Test Django recognizes the app:
```bash
python manage.py help tailwind
```

### Step 3: Initialize Tailwind App

**Command Options:**

#### Default (Tailwind CSS v4, recommended)
```bash
python manage.py tailwind init --no-input
```

#### For Custom App Name
```bash
python manage.py tailwind init --no-input --app-name custom_theme
```

#### For Tailwind CSS v3 (legacy)
```bash
python manage.py tailwind init --no-input --tailwind-version 3
```

**What This Creates:**
- New Django app (default name: `theme`)
- Directory structure with `static_src/` and `templates/`
- `package.json` with build scripts
- PostCSS configuration
- Base template files

**Validation**: Verify app creation:
```bash
# Check directory exists
ls -la theme/  # or your custom app name

# Check required files
ls -la theme/static_src/package.json
ls -la theme/static_src/src/styles.css
```

### Step 4: Update Django Settings

**File**: `settings.py`
**Actions**: Add generated app and configure Tailwind

```python
INSTALLED_APPS = [
    # ... existing apps
    'tailwind',
    'theme',  # Replace with your custom app name if different
    # ... other apps
]

# Configure Tailwind app name
TAILWIND_APP_NAME = 'theme'  # Replace with your custom app name if different
```

**Optional Auto-Reload Setup** (if installed with `[reload]`):
```python
INSTALLED_APPS = [
    # ... existing apps
    'tailwind',
    'theme',
    'django_browser_reload',  # Add this for auto-reload
    # ... other apps
]

MIDDLEWARE = [
    # ... existing middleware
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    # ... other middleware
]

# Add to urlpatterns in main urls.py
from django.urls import include, path

urlpatterns = [
    # ... existing patterns
    path("__reload__/", include("django_browser_reload.urls")),
]
```

**Validation**: Test configuration:
```bash
python manage.py check
```

### Step 5: Install Node.js Dependencies

**Command:**
```bash
python manage.py tailwind install
```

**For Docker/Permission Issues:**
```bash
python manage.py tailwind install --no-package-lock
```

**What This Does:**
- Installs Tailwind CSS and dependencies
- Creates `node_modules/` directory
- Generates `package-lock.json` (unless `--no-package-lock`)

**Validation**: Verify installation:
```bash
# Check node_modules exists
ls -la theme/static_src/node_modules/

# Test build command
python manage.py tailwind build
```

### Step 6: Template Integration

**File**: Your base template (e.g., `templates/base.html`)
**Action**: Add Tailwind CSS inclusion

```html
{% load static tailwind_tags %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django Tailwind</title>
    {% tailwind_preload_css %}
    {% tailwind_css %}
</head>
<body>
    <h1 class="text-4xl font-bold text-blue-600">Hello Tailwind!</h1>
    <!-- Your content -->
</body>
</html>
```

**Validation**: Test template rendering:
```bash
python manage.py runserver
# Visit http://127.0.0.1:8000 and check if Tailwind styles apply
```

## Development Setup

### Option 1: Combined Development (Recommended)
```bash
python manage.py tailwind dev
```
- Starts Django server and Tailwind watcher simultaneously
- Auto-installs Honcho if needed
- Creates `Procfile.tailwind` automatically

### Option 2: Separate Processes
```bash
# Terminal 1: Start Tailwind watcher
python manage.py tailwind start

# Terminal 2: Start Django server
python manage.py runserver
```

## Configuration Options

### Essential Settings

```python
# Required
TAILWIND_APP_NAME = 'theme'  # Your Tailwind app name

# Optional (with defaults)
TAILWIND_CSS_PATH = 'css/dist/styles.css'  # Path to generated CSS
NPM_BIN_PATH = 'npm'  # Path to npm executable
```

### Custom npm Path (if needed)
```python
# Linux/Mac
NPM_BIN_PATH = '/usr/local/bin/npm'

# Windows
NPM_BIN_PATH = 'npm.cmd'
# or full path
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
```

## Common Issues & Solutions

### Issue 1: Node.js/npm Not Found
**Error**: `OSError: It looks like node.js and/or npm is not installed`

**Solution**:
1. Install Node.js from https://nodejs.org/
2. Or set custom npm path in settings:
   ```python
   NPM_BIN_PATH = '/path/to/npm'
   ```

### Issue 2: App Not in INSTALLED_APPS
**Error**: `{app_name} is not in INSTALLED_APPS`

**Solution**: Add app to INSTALLED_APPS:
```python
INSTALLED_APPS = [
    # ... other apps
    'tailwind',
    'theme',  # your generated app
]
```

### Issue 3: Missing TAILWIND_APP_NAME
**Error**: `TAILWIND_APP_NAME isn't set in settings.py`

**Solution**: Add setting:
```python
TAILWIND_APP_NAME = 'theme'
```

### Issue 4: Not a Tailwind App
**Error**: `'{app_name}' isn't a Tailwind app`

**Solution**: App must have `package.json` in `static_src/` directory. Re-run:
```bash
python manage.py tailwind init --no-input
```

### Issue 5: Permission Errors
**Common in Docker/Production**

**Solution**:
- Use `--no-package-lock` flag
- Check file permissions
- Ensure proper ownership

### Issue 6: CSS Not Updating
**Possible Causes**:
- Content paths not configured
- Tailwind watcher not running

**Solutions**:
- Check `@source` directive in v4 or `content` array in v3
- Restart `python manage.py tailwind start`
- Verify file permissions

### Issue 7: Import Errors
**Error**: Template tags not found

**Solution**: Ensure proper loading in templates:
```html
{% load static tailwind_tags %}
{% tailwind_css %}
```

## Version-Specific Notes

### Tailwind CSS v4 (Default)
- No `tailwind.config.js` needed
- Uses `@source` directive for content scanning
- Simpler configuration

### Tailwind CSS v3 (Legacy)
- Uses `tailwind.config.js` for configuration
- Content scanning via `content` array
- More complex setup

## Agent-Specific Considerations

### For Automated Installation
1. Always use `--no-input` flag
2. Verify each step before proceeding
3. Check for error messages in command output
4. Test final setup with simple HTML

### Error Detection
Watch for these error patterns:
- `CommandError:`
- `OSError:`
- `ImportError:`
- `ModuleNotFoundError:`
- `FileNotFoundError:`

### Success Validation
Confirm these indicators:
- ✅ No errors in `python manage.py check`
- ✅ Tailwind commands work: `python manage.py tailwind --help`
- ✅ CSS file generated: `theme/static/css/dist/styles.css`
- ✅ Template tags load without errors

## Production Deployment

### Build Process
```bash
# Build optimized CSS
python manage.py tailwind build

# Collect static files
python manage.py collectstatic
```

### Docker Considerations
```dockerfile
# Install Node.js in container
RUN apt-get update && apt-get install nodejs npm -y

# Install without package-lock
RUN python manage.py tailwind install --no-package-lock

# Build CSS
RUN python manage.py tailwind build

# Collect static files
RUN python manage.py collectstatic --no-input
```

## Final Verification Checklist

**Before considering setup complete:**

- [ ] `python manage.py check` runs without errors
- [ ] `python manage.py tailwind --help` shows available commands
- [ ] CSS file exists: `theme/static/css/dist/styles.css`
- [ ] Template tags load: `{% load tailwind_tags %}`
- [ ] Tailwind classes apply in browser
- [ ] Development server runs: `python manage.py runserver`
- [ ] Tailwind watcher works: `python manage.py tailwind start`

## Quick Setup Script

**For rapid deployment, use this command sequence:**

```bash
# Install package
pip install 'django-tailwind[reload]'

# Initialize (adjust app name as needed)
python manage.py tailwind init --no-input

# Install dependencies
python manage.py tailwind install

# Build CSS
python manage.py tailwind build

# Verify setup
python manage.py check
```

**Then manually update settings.py:**
```python
INSTALLED_APPS = [
    # ... existing apps
    'tailwind',
    'theme',
    'django_browser_reload',  # if using reload
]

TAILWIND_APP_NAME = 'theme'
```

---

## Support Information

- **Documentation**: https://github.com/timonweb/django-tailwind/tree/master/docs
- **GitHub**: https://github.com/timonweb/django-tailwind
- **Issues**: https://github.com/timonweb/django-tailwind/issues

---

*This guide covers all known edge cases and installation scenarios. Follow steps sequentially and validate each step for successful installation.*
