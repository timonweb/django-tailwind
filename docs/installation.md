# Installation

## Step-by-step instructions

1. Install the `django-tailwind` package via `pip`:

   ```bash
   python -m pip install django-tailwind
   ```

   If you want to use automatic page reloads during development (see steps 9-12 below),
   use the `[reload]` extras, which installs the `django-browser-reload` package
   in addition:

   ```bash
   python -m pip install 'django-tailwind[reload]'
   ```

   Alternatively, you can install the latest development version via:

   ```bash
   python -m pip install git+https://github.com/timonweb/django-tailwind.git
   ```

2. Add `'tailwind'` to `INSTALLED_APPS` in `settings.py`:

   ```python
   INSTALLED_APPS = [
     # other Django apps
     'tailwind',
   ]
   ```

3. Create a *Tailwind CSS* compatible *Django* app, I like to call it `theme`:

   ```bash
   python manage.py tailwind init
   ```

   > Note: By default, we create an app compatible with Tailwind CSS version 4. If you want to create an app compatible
   > with Tailwind CSS version 3, you can use the `--tailwind-version 3` flag:

    ```bash
    python manage.py tailwind init --tailwind-version 3
    ```

4. Add your newly created `'theme'` app to `INSTALLED_APPS` in `settings.py`:

   ```python
   INSTALLED_APPS = [
     # other Django apps
     'tailwind',
     'theme'
   ]
   ```

5. Register the generated `'theme'` app by adding the following line to `settings.py`:

   ```python
   TAILWIND_APP_NAME = 'theme'
   ```

6. Install *Tailwind CSS* dependencies by running the following command:

   ```bash
   python manage.py tailwind install
   ```

   > Note: If for some reason you don't want `package-lock.json` to be created, you can use the `--no-package-lock` flag:

    ```bash
    python manage.py tailwind install --no-package-lock
    ```

7. The *Django Tailwind* comes with a simple `base.html` template located at
   `your_tailwind_app_name/templates/base.html`. You can always extend or delete it if you already have a layout.

8. If you are not using the `base.html` template that comes with *Django Tailwind*, add `{% tailwind_css %}` to
   your `base.html` template:

   ```html
   {% load static tailwind_tags %}
   ...
   <head>
      ...
      {% tailwind_css %}
      ...
   </head>
   ```

   The `{% tailwind_css %}` tag includes Tailwind's stylesheet.

9. Let's also add and configure `django_browser_reload`, which takes care of automatic page and CSS refreshes in
   development mode. Add it to `INSTALLED_APPS` in `settings.py`:

    ```python
    INSTALLED_APPS = [
      # other Django apps
      'tailwind',
      'theme',
      'django_browser_reload'
    ]
    ```

10. Staying in `settings.py`, add the middleware:

    ```python
    MIDDLEWARE = [
      # ...
      "django_browser_reload.middleware.BrowserReloadMiddleware",
      # ...
    ]
    ```

    The middleware should be listed after any that encode the response, such as Django’s `GZipMiddleware`. The
    middleware automatically inserts the required script tag on HTML responses before `</body>` when `DEBUG` is `True`.

11. Include `django_browser_reload` URL in your root `urls.py`:

    ```python
    from django.urls import include, path
    urlpatterns = [
        ...,
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    ```

12. Finally, you should be able to use *Tailwind CSS* classes in HTML. You have two options to start development:

    **Option 1 (Recommended):** Start both Django and Tailwind development servers simultaneously:

    ```bash
    python manage.py tailwind dev
    ```

    **Option 2:** Start only the Tailwind watcher (you'll need to run `python manage.py runserver` separately):

    ```bash
    python manage.py tailwind start
    ```

    Check out the [Usage](./usage.md) section for more details and information about the production mode.

## Optional configurations

### Content (formerly Purge) rules configuration (for Tailwind CSS v3)

The `content` section of your `tailwind.config.js` file is where you configure the paths to all of your HTML templates,
JavaScript components, and any other source files that contain *Tailwind* class names.

Depending on your project structure, you might need to configure the `content` rules in `tailwind.config.js`. This file
is in the `static_src` folder of the theme app created by `python manage.py tailwind init {APP_NAME}`.

For example, your `theme/static_src/tailwind.config.js` file might look like this:

```js
module.exports = {
    content: [
        // Templates within theme app (e.g. base.html)
        '../templates/**/*.html',
        // Templates in other apps
        '../../templates/**/*.html',
        // Ignore files in node_modules
        '!../../**/node_modules',
        // Include JavaScript files that might contain Tailwind CSS classes
        '../../**/*.js',
        // Include Python files that might contain Tailwind CSS classes
        '../../**/*.py'
    ],
    ...
}
```

Note that you may need to adjust those paths to suit your specific project layout. It is crucial to make sure that *all*
HTML files (or files containing HTML content, such as `.vue` or `.jsx` files) are covered by the `content` rule.

For more information about setting `content`, check out the *"Content Configuration"* page of the Tailwind CSS
docs: [https://tailwindcss.com/docs/content-configuration](https://tailwindcss.com/docs/content-configuration).

### @source directive configuration (for Tailwind CSS v4)

The `content` section from Tailwind CSS v3 has been replaced with the `@source` directive in Tailwind CSS v4.
The `@source` directive is a new way to specify the source files that Tailwind CSS should scan for class names. It's
placed in the `style.css` file.

By default, it looks like this:

```css
@source "../../**/*.{html,py,js}";
```

This means that Tailwind CSS will scan all HTML, Python, and JavaScript files in all directories starting from the
three directories above the `style.css` file. Depending on your project structure, you might need to adjust the
`@source` directive to suit your specific project layout.

For more information about setting `@source`, check out the *"Source Configuration"* page of the Tailwind CSS docs:
[https://tailwindcss.com/docs/detecting-classes-in-source-files#explicitly-registering-sources](https://tailwindcss.com/docs/detecting-classes-in-source-files#explicitly-registering-sources).

### Configuration of the path to the `npm` executable

*Tailwind CSS* requires *Node.js* to be installed on your machine.
*Node.js* is a *JavaScript* runtime that allows you to run *JavaScript* code outside the browser. Most (if not all) of
the current frontend tools depend on *Node.js*.

If you don't have *Node.js* installed on your machine, please follow the installation instructions
from [the official Node.js page](https://nodejs.org/).

Sometimes (especially on *Windows*), the *Python* executable cannot find the `npm` binary installed on your system. In
this case, you need to set the path to the `npm` executable in the *settings.py* file manually (*Linux/Mac*):

```python
NPM_BIN_PATH = '/usr/local/bin/npm'
```

On *Windows*, you may have npm on `$PATH` but it's `npm.cmd` rather than `npm`. (You can call it from the terminal
because `$PATHEXT` contains `.cmd`.) If so, please override the default `NPM_BIN_PATH = 'npm'`:

```python
NPM_BIN_PATH = 'npm.cmd'
```

Alternatively (and for maximum reliability), you can use a fully qualified path. It might look like this:

```python
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
```

Please note that the path to the `npm` executable may be different for your system. To get the `npm` path, try running
the command `which npm` in your terminal. (On *Windows*, please try `where npm` or `Get-Command npm`)
