# Installation

## Step-by-step instructions

1. Install the `django-tailwind` package via `pip`:

   ```bash
   python -m pip install django-tailwind
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

3. Create a _Tailwind CSS_ compatible _Django_ app, I like to call it `theme`:

   ```bash
   python manage.py tailwind init
   ```
   > During the initialization step, you'll be asked to choose between **Just in
   > time (`jit`)** and **Ahead of time (`aot`)** modes. While the `jit` mode is
   > new and somewhat experimental in _Tailwind CSS_, I suggest choosing it for
   > the best development experience. You can change the mode later with a
   > simple configuration update. Check the [jit vs aot](./jit-vs-aot.md)
   > section for more information.

4. Add your newly created `'theme'` app to `INSTALLED_APPS` in `settings.py`:
   ```python
   INSTALLED_APPS = [
     # other Django apps
     'tailwind',
     'theme'
   ]
   ```

5. Register the generated `'theme'` app by adding the following line to
   `settings.py`:

   ```python
   TAILWIND_APP_NAME = 'theme'
   ```

6. Make sure that `INTERNAL_IPS` list is present in the `settings.py` file and
   contains the `127.0.0.1` ip address:

   ```python
   INTERNAL_IPS = [
       "127.0.0.1",
   ]
   ```

7. Install _Tailwind CSS_ dependencies, by running the following command:

   ```bash
   python manage.py tailwind install
   ```

8. The _Django Tailwind_ comes with a simple `base.html` template located at
   `your_tailwind_app_name/templates/base.html`. You can always extend or delete
   it if you already have a layout.

9. If you are not using the `base.html` template that comes with _Django
   Tailwind_, add `{% tailwind_css %}` to the `base.html` template:

   ```html
   {% load tailwind_tags %}
   ...
   <head>
      ...
      {% tailwind_css %}
      ...
   </head>
   ```

   The `{% tailwind_css %}` tag loads appropriate stylesheets and, when you're
   in `DEBUG` mode, connects to the `browser-sync` service that enables hot
   reloading of assets and pages.

10. Ok, now you should be able to use _Tailwind CSS_ classes in HTML. Start the
    development server by running the following command in your terminal:

        ```bash
        python manage.py tailwind start
        ```

Check out [Usage](./usage.md) section for information about the production mode.

## Optional configurations

### Purge rules configuration

Depending on your project structure, you might need to configure the `purge`
rules in `tailwind.config.js`. This file is in the `static_src` folder of the
theme app created by `python manage.py tailwind init {APP_NAME}`.

For example, your `theme/static_src/tailwind.config.js` file might look like
this:

```js
module.exports = {
  purge: [
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

Note that you may need to adjust those paths to suit your specific project
layout. It is crucial to make sure that _all_ HTML files (or files containing
HTML content, such as `.vue` or `.jsx` files) are covered by the `purge` rule.

For more information about setting `purge`, check out the _"Controlling File
Size"_ page of the Tailwind CSS docs:
[https://tailwindcss.com/docs/controlling-file-size/#removing-unused-css](https://tailwindcss.com/docs/controlling-file-size/#removing-unused-css) -
particularly the _"Removing Unused CSS"_ section, although the entire page is a
useful reference.

Under the **Ahead of time** (`aot`) mode, PurgeCSS only runs when you use the
`python manage.py tailwind build` management command (creates a production CSS
build).

If you run _Tailwind CSS_ in the **Just in time** (`jit`) mode, you will get an
optimized build even in development mode, and it happens at lightning speed.

Checkout the [JIT vs AOT](./jit-vs-aot.md) section for more information about
_Tailwind CSS_ compilation modes.

### Configuration of the path to the `npm` executable

_Tailwind CSS_ requires _Node.js_ to be installed on your machine. _Node.js_ is
a _JavaScript_ runtime that allows you to run _JavaScript_ code outside the
browser. Most (if not all) of the current frontend tools depend on _Node.js_.

If you don't have _Node.js_ installed on your machine, please follow
installation instructions from [the official Node.js page](https://nodejs.org/).

Sometimes (especially on _Windows_), the _Python_ executable cannot find the
`npm` binary installed on your system. In this case, you need to set the path to
the `npm` executable in _settings.py_ file manually (_Linux/Mac_):

```python
NPM_BIN_PATH = '/usr/local/bin/npm'
```

On _Windows_ it might look like this:

```python
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
```

Please note that the path to the `npm` executable may be different on your
system. To get the `npm` path on your system, try running the command
`which npm` in your terminal.
