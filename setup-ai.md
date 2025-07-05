# Django-Tailwind AI Agent Setup Guide

> **For Coding Agents**: This guide provides complete installation instructions for django-tailwind with all edge cases covered. Follow steps sequentially and validate each step before proceeding.

## Prerequisites Check

**CRITICAL**: Verify these requirements before starting:

### 1. System Requirements
- [ ] Python >= 3.10 installed
- [ ] Django >= 4.2.20 installed
- [ ] **Node.js MUST be installed** (any recent version) - **AGENT CANNOT INSTALL THIS**
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

**IMPORTANT**: Detect project's package manager first, then use appropriate installation method.

#### Auto-Detect Package Manager
```bash
# Check for package managers in order of preference
if [ -f "uv.lock" ] || [ -f "pyproject.toml" ] && command -v uv &> /dev/null; then
    echo "Using uv"
    PKG_MANAGER="uv"
elif [ -f "poetry.lock" ] || [ -f "pyproject.toml" ] && command -v poetry &> /dev/null; then
    echo "Using poetry"
    PKG_MANAGER="poetry"
elif [ -f "Pipfile" ] && command -v pipenv &> /dev/null; then
    echo "Using pipenv"
    PKG_MANAGER="pipenv"
elif [ -f "requirements.txt" ] || [ -f "setup.py" ] || [ -f "setup.cfg" ]; then
    echo "Using pip"
    PKG_MANAGER="pip"
else
    echo "Using pip (default)"
    PKG_MANAGER="pip"
fi
```

#### Installation Commands by Package Manager

**⚠️ AGENT INSTRUCTION**: Always install with `[reload]` option by default for best development experience.

##### If using uv
```bash
# Default installation (with auto-reload)
uv add 'django-tailwind[reload]'
```

##### If using Poetry
```bash
# Default installation (with auto-reload)
poetry add 'django-tailwind[reload]'
```

##### If using Pipenv
```bash
# Default installation (with auto-reload)
pipenv install 'django-tailwind[reload]'
```

##### If using pip
```bash
# Default installation (with auto-reload)
pip install 'django-tailwind[reload]'
```

**Validation**: Verify installation:
```bash
python -c "import tailwind; print('django-tailwind installed successfully')"
```

### Step 2: Add ONLY 'tailwind' to INSTALLED_APPS

**⚠️ CRITICAL**: Only add `'tailwind'` now. DO NOT add the theme app yet - it doesn't exist!

**File**: `settings.py`
**Action**: Add ONLY `'tailwind'` to INSTALLED_APPS

```python
INSTALLED_APPS = [
    # ... existing apps
    'tailwind',  # Add ONLY this - do NOT add 'theme' yet!
    # ... other apps
]
```

**Validation**: Test Django recognizes the app:
```bash
python manage.py help tailwind
```

### Step 3: Initialize Tailwind App

**⚠️ MANDATORY USER INTERACTION**: You MUST ASK the user for their preferred app name before proceeding.

**REQUIRED USER QUESTION:**
```
"What would you like to name your Tailwind app? (Default: 'theme')"
```

**⚠️ AGENT REQUIREMENT**: You MUST ask this question and wait for user response. Do not proceed without asking!

**Command Options:**

#### Default (Tailwind CSS v4, recommended)
```bash
# If user chose default 'theme' name
python manage.py tailwind init --no-input

# If user chose custom name (replace 'custom_theme' with user's choice)
python manage.py tailwind init --no-input --app-name custom_theme
```

#### For Tailwind CSS v3 (legacy)
```bash
# If user chose default 'theme' name
python manage.py tailwind init --no-input --tailwind-version 3

# If user chose custom name (replace 'custom_theme' with user's choice)
python manage.py tailwind init --no-input --app-name custom_theme --tailwind-version 3
```

**What This Creates:**
- New Django app (default name: `theme` or user's custom name)
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

**⚠️ AGENT INSTRUCTION**: Now that the Tailwind app has been created, add it to INSTALLED_APPS and configure auto-reload.

**File**: `settings.py`
**Actions**: Add generated app and configure Tailwind with auto-reload

```python
INSTALLED_APPS = [
    # ... existing apps
    'tailwind',
    'theme',  # Replace with your custom app name if different
    # ... other apps
]

# Configure Tailwind app name
TAILWIND_APP_NAME = 'theme'  # Replace with your custom app name if different

# Add django_browser_reload only in DEBUG mode (development)
if DEBUG:
    INSTALLED_APPS += ['django_browser_reload']

    # Add Browser Reload Middleware only in DEBUG mode
    MIDDLEWARE += [
        'django_browser_reload.middleware.BrowserReloadMiddleware',
    ]
```

**File**: Main `urls.py` (usually `myproject/urls.py`)
**Action**: Add auto-reload URL pattern ONLY in DEBUG mode

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # ... your existing URL patterns
]

# Add django_browser_reload URL pattern only in DEBUG mode
if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
```

**Validation**: Test configuration and verify DEBUG conditions:
```bash
python manage.py check
```

**⚠️ CRITICAL VALIDATION**: Check that django_browser_reload is properly configured with DEBUG conditions:

1. **Check settings.py** - django_browser_reload should ONLY be in INSTALLED_APPS and MIDDLEWARE with `if DEBUG:`:
   - ✅ **CORRECT**: `if DEBUG: INSTALLED_APPS += ['django_browser_reload']`
   - ❌ **WRONG**: `'django_browser_reload'` directly in INSTALLED_APPS list
   - ✅ **CORRECT**: `if DEBUG: MIDDLEWARE += ['django_browser_reload.middleware.BrowserReloadMiddleware']`
   - ❌ **WRONG**: `'django_browser_reload.middleware.BrowserReloadMiddleware'` directly in MIDDLEWARE list

2. **Check urls.py** - django_browser_reload URLs should ONLY be added with `if settings.DEBUG:`:
   - ✅ **CORRECT**: `if settings.DEBUG: urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]`
   - ❌ **WRONG**: `path("__reload__/", include("django_browser_reload.urls"))` directly in urlpatterns list

**If you find django_browser_reload configured WITHOUT DEBUG conditions, you MUST fix it immediately:**

**Fix for INSTALLED_APPS (if wrongly added directly):**
```python
# WRONG - Remove this:
INSTALLED_APPS = [
    # ... apps
    'django_browser_reload',  # ❌ Remove this line
]

# CORRECT - Replace with this:
INSTALLED_APPS = [
    # ... apps
]

if DEBUG:
    INSTALLED_APPS += ['django_browser_reload']
```

**Fix for MIDDLEWARE (if wrongly added directly):**
```python
# WRONG - Remove this:
MIDDLEWARE = [
    # ... middleware
    'django_browser_reload.middleware.BrowserReloadMiddleware',  # ❌ Remove this line
]

# CORRECT - Replace with this:
MIDDLEWARE = [
    # ... middleware
]

if DEBUG:
    MIDDLEWARE += ['django_browser_reload.middleware.BrowserReloadMiddleware']
```

**Fix for urlpatterns (if wrongly added directly):**
```python
# WRONG - Remove this:
urlpatterns = [
    # ... patterns
    path("__reload__/", include("django_browser_reload.urls")),  # ❌ Remove this line
]

# CORRECT - Replace with this:
urlpatterns = [
    # ... patterns
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
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

**⚠️ AGENT MUST NOT INSTALL NODE.JS AUTOMATICALLY**

**Solution for Agent:**
1. **STOP** - Ask user to install Node.js first
2. Inform user: "Node.js is required but not installed. Please install Node.js from https://nodejs.org/ and then re-run this setup."
3. Offer to help after user installs Node.js
4. Alternative: If user has Node.js but different path, ask for custom npm path:
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

### Critical Requirements for Agents
1. **MANDATORY**: Ask user for app name before Step 3 (tailwind init)
2. **MANDATORY**: Only add 'tailwind' to INSTALLED_APPS in Step 2
3. **MANDATORY**: Add theme app to INSTALLED_APPS only AFTER Step 3 creates it
4. **MANDATORY**: All django_browser_reload setup MUST use `if DEBUG:` conditions
5. **FORBIDDEN**: Do NOT create any test views or test routes
6. Always use `--no-input` flag for tailwind commands
7. Verify each step before proceeding
8. Check for error messages in command output
9. After successful setup, inform user to run: `python manage.py tailwind dev`

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

---

## Support Information

- **Documentation**: https://github.com/timonweb/django-tailwind/tree/master/docs
- **GitHub**: https://github.com/timonweb/django-tailwind
- **Issues**: https://github.com/timonweb/django-tailwind/issues

---

*This guide covers all known edge cases and installation scenarios. Follow steps sequentially and validate each step for successful installation.*
