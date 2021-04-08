# The integration of Tailwind CSS framework with Django a.k.a. Django + Tailwind = ❤

## Features
* An opinionated Tailwind setup that makes your life easier;
* Hot reloading of CSS, configuration files and Django templates. No more manual page refreshes!
* Out of the box support for CSS imports, SASS-like variables and nesting;
* Includes official Tailwind plugins like typography, form, line-clamp and aspect-ratio;

## Quick start

1. Install the `django-tailwind` package via Pip:

   `python -m pip install django-tailwind`

   Alternatively, you can install the latest development version via:

   `python -m pip install git+https://github.com/timonweb/django-tailwind.git`

2. Add `tailwind` to INSTALLED_APPS in **settings.py**

3. Create a tailwind-compatible Django-app, I like to call it `theme`:

   `python manage.py tailwind init`

   > During the initialization step, you'll be prompted to choose between `jit` and `default` modes. Whereas `jit` mode is new and somewhat experimental in Tailwind, I suggest choosing it for the best development experience.

4. Add your newly created `theme` app to INSTALLED_APPS in **settings.py**

5. In settings.py, register tailwind app by adding the following string:

   `TAILWIND_APP_NAME = 'theme'`

6. Run a command to install all necessary dependencies for tailwind css:

   `python manage.py tailwind install`

7. Now, go and start tailwind in dev mode:

   `python manage.py tailwind start`

8. Django Tailwind comes with a simple `base.html` template that can be found under
   `your_tailwind_app_name/templates/base.html`. You can always extend it or delete it if you
   have own layout.

9. If don't use `base.html` template provided with Django Tailwind, add `{% tailwind_css %}` to your `base.html` template file:

   ```html
   {% load tailwind_tags %}
   ...
   <head>
      ...
      {% tailwind_css %}
      ...
   </head>
   ```

10) You should now be able to use Tailwind CSS classes in your html.

11) To build a production version of CSS run:

    `python manage.py tailwind build`.

## PurgeCSS setup

To avoid importing all Tailwind (resulting in a massive CSS filesize), set up the purge configuration in `tailwind.config.js`.
This file is located in the `static_src` folder of the app created by `tailwind init {APP_NAME}`.

For example, your `tailwind.config.js` file could look like:

```js
module.exports = {
  purge: [
    // Templates within theme app (e.g. base.html)
    '../templates/**/*.html',
    // Templates in other apps
    '../../templates/**/*.html',
  ],
  ...
}
```

Note that you may need to adjust those paths to suit your specific project layout. It is important to ensure that _all_ of your HTML files are covered (or files with contain HTML content, such as .vue or .jsx files), to enusre PurgeCSS can whitelist all of your classes.

For more information on this, check out the "Controlling File Size" page of the Tailwind docs: [https://tailwindcss.com/docs/controlling-file-size/#removing-unused-css](https://tailwindcss.com/docs/controlling-file-size/#removing-unused-css) - particularly the "Removing Unused CSS" section, although the entire page is a useful reference.

*The following applies to the `default` mode only.* 
To help speed up development builds, PurgeCSS is only run when you use the `tailwind build` management command (to create a production build of your CSS).

If you run in `jit` mode, you get an optimized build even in dev mode, and it happens at the lightning speed.

## NPM executable path configuration

Sometimes (especially on Windows), Python executable can't find `NPM` installed in the system.
In this case, you need to set `NPM` executable path in settings.py file manually (Linux/Mac):

```python
NPM_BIN_PATH = '/usr/local/bin/npm'
```

On windows it might look like:

```python
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
```

Please note that `NPM` path of your system may be different. Try to run `which npm` in your
command line to get the path.

## Updating Tailwind CSS and dependencies

If there's a new release of the tailwind css came out you can always update your `theme` project
without updating this django package by using two commands: `python manage.py tailwind check-updates` and
`python manage.py tailwind update`.

### Checking if there are updates for tailwind css and its dependencies

Before doing an update, you can check if there are any updates. Run the following command:
```
python manage.py tailwind check-updates
```
*Behind the scenes it runs `npm outdated` command within your `theme/static_src` directory.*

If there are updates, you'll see a table dependencies with the latest compatible versions.
If there are no updates, this command will return no output.

### Updating tailwind css and its dependencies

If you want to use the latest version of tailwind css, run the following command:

```
python manage.py tailwind update
```
*Behind the scenes it runs `npm update` command within your `theme/static_src` directory.*

If there are updates, you'll see a log of updated dependencies.
If there are no updates, this command will return no output.

## Upgrading from Django-Tailwind v1 to v2

Please note, that the instructions below are for upgrading the Django package,
not the actual Tailwind CSS dependency.

Django-Tailwind v2 introduces lots of new features that aren't available to projects,
that were generated with the previous version. Thus if you want to get all the goodies, v2 offers,
you'll have to update your Django `theme` app.

Depending on how many customizations you've introduced, the process might be smooth or bumpy.

### Upgrade steps

Let's assume, you have a django-tailwind app installed that is called `theme`.

1. Go to `INSTALLED_APPS` in *settings.py* and remove 'theme' app.
2. Rename your `theme` app directory to `theme-legacy`.
3. Generate a new Tailwind app:
   
   ```bash
   python manage.py tailwind init
   ```
   Name it like your previous app was named: `theme`.
4. Add `theme` back to `INSTALLED_APPS`;
5. Copy `theme-legacy/static_src/src` to `theme/static_src/src`;
6. If you have a file named `theme/static_src/src/styles.scss`, rename it to `theme/static_src/src/styles.css`. In v2 we've dropped SASS support, but POSTCSS should work just fine. Unless you've used advanced SASS features, which is unlikely;
7. Open `theme-legacy/static_src/tailwind.config.js` and compare it to `theme/static_src/tailwind.config.js`, if you have customizations there, like custom colors, variables, etc, copy them over to `theme/static_src/tailwind.config.js`;
8. Copy `theme-legacy/templates` to `theme/templates`;
9. Open `theme/templates/base.html` and add `{% load tailwind_tags %}` at the beginning of the file. Then, replace:
   ```html
   <link
     rel="stylesheet"
     href="{% static 'css/styles.css' %}"
     type="text/css"
   />
   ```
   with
   ```html
   {% tailwind_css %}
   ```
10. Run `python manage.py tailwind install` to install dependencies.
11. Run `python manage.py tailwind start` to start the development server.
12. If all went well, you should now be on the latest Django-Tailwind version with your previous styles preserved.

## Bugs and suggestions

If you have found a bug, please use the issue tracker on GitHub.

[https://github.com/timonweb/django-tailwind/issues](https://github.com/timonweb/django-tailwind/issues)

2019 - 2021 (c) [Tim Kamanin - A Full Stack Django Developer](https://timonweb.com)
