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

3. Create a *Tailwind CSS* compatible *Django* app, I like to call it `theme`:

   ```bash
   python manage.py tailwind init
   ```
   > During the initialization step, you'll be asked to choose between **Just in time (`jit`)** and **Ahead of time (`aot`)** modes. While the `jit` mode is new and somewhat experimental in *Tailwind CSS*, I suggest choosing it for the best development experience.
   > You can change the mode later with a simple configuration update. Check the [jit vs aot](./jit-vs-aot.md) section for more information.

4. Add your newly created `'theme'` app to `INSTALLED_APPS` in `settings.py`:
   ```python
   INSTALLED_APPS = [
     # other Django apps
     'tailwind',
     'theme'
   ]
   ```

5. Register the generated `'theme'` app by adding the following line to `settings.py` file:

   ```python
   TAILWIND_APP_NAME = 'theme'
   ```
   
6. Make sure that the `INTERNAL_IPS` list is present in the `settings.py` file and contains the `127.0.0.1` ip address:

   ```python
   INTERNAL_IPS = [
       "127.0.0.1",
   ]
   ```

7. Install *Tailwind CSS* dependencies, by running the following command:

   ```bash
   python manage.py tailwind install
   ```

8. The *Django Tailwind* comes with a simple `base.html` template located at
   `your_tailwind_app_name/templates/base.html`. You can always extend or delete it if you already have a layout.

9. If you are not using the `base.html` template that comes with *Django Tailwind*, add `{% tailwind_css %}` to the `base.html` template:

   ```html
   {% load tailwind_tags %}
   ...
   <head>
      ...
      {% tailwind_css %}
      ...
   </head>
   ```
   
   The `{% tailwind_css %}` tag loads appropriate stylesheets and, when you're in `DEBUG` mode, connects to the `browser-sync` service that enables hot reloading of assets and pages.

10. Ok, now you should be able to use *Tailwind CSS* classes in HTML. Start the development server by running the following command in your terminal:
   
      ```bash
      python manage.py tailwind start
      ```
 
   Check out the [Usage](./usage.md) section for information about the production mode.

## Optional configurations

### Purge rules configuration

Depending on your project structure, you might need to configure the `purge` rules in `tailwind.config.js`.
This file is in the `static_src` folder of the theme app created by `python manage.py tailwind init {APP_NAME}`.

For example, your `theme/static_src/tailwind.config.js` file might look like this:

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

Note that you may need to adjust those paths to suit your specific project layout. It is crucial to make sure that *all* HTML files (or files containing HTML content, such as `.vue` or `.jsx` files) are covered by the `purge` rule.

For more information about setting `purge`, check out the *"Controlling File Size"* page of the Tailwind CSS docs: [https://tailwindcss.com/docs/controlling-file-size/#removing-unused-css](https://tailwindcss.com/docs/controlling-file-size/#removing-unused-css) - particularly the *"Removing Unused CSS"* section, although the entire page is a useful reference.

Under the **Ahead of time** (`aot`) mode, PurgeCSS only runs when you use the `python manage.py tailwind build` management command (creates a production CSS build).

If you run *Tailwind CSS* in the **Just in time** (`jit`) mode, you will get an optimized build even in development mode, and it happens at lightning speed.

See the [JIT vs AOT](./jit-vs-aot.md) section for more information about *Tailwind CSS* compilation modes.

### Configuration of the path to the `npm` executable

*Tailwind CSS* requires *Node.js* to be installed on your machine.
*Node.js* is a *JavaScript* runtime that allows you to run *JavaScript* code outside the browser. Most (if not all) of the current frontend tools depend on *Node.js*.

If you don't have *Node.js* installed on your machine, please follow installation instructions from [the official Node.js page](https://nodejs.org/).

Sometimes (especially on *Windows*), the *Python* executable cannot find the `npm` binary installed on your system.
In this case, you need to set the path to the `npm` executable in *settings.py* file manually (*Linux/Mac*):

```python
NPM_BIN_PATH = '/usr/local/bin/npm'
```

On *Windows* it might look like this:

```python
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
```

Please note that the path to the `npm` executable may be different on your system. To get the `npm` path on your system, try running the command `which npm` in your terminal.
