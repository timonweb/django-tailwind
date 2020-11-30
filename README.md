# The integration of Tailwind CSS framework with Django a.k.a. Django + Tailwind = ❤

## Quick start

1. Install the `django-tailwind` package via Pip:

   `python -m pip install django-tailwind`

   Alternatively, you can install the latest development version via:

   `python -m pip install git+https://github.com/timonweb/django-tailwind.git`

2. Add `tailwind` to INSTALLED_APPS in **settings.py**

3. Create a tailwind-compatible Django-app, I like to call it `theme`:

   `python manage.py tailwind init theme`
   
   *NOTE:* By default, we install v2 of Tailwind CSS. If you want v1 Tailwind CSS you need to pass an additional `--legacy` parameter to the command:
   `python manage.py tailwind init --legacy theme`.

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

9. If you're not using `base.html` template provided with Django Tailwind, add `styles.css` to your own `base.html` template file:

   ```html
   <link
     rel="stylesheet"
     href="{% static 'css/styles.css' %}"
     type="text/css"
   />
   ```

10) You should now be able to use Tailwind CSS classes in your html.

11) To build a production version of CSS run:

    `python manage.py tailwind build`.

## PurgeCSS setup

To avoid importing all of Tailwind (resulting in a massive CSS filesize), set up the purge configuration in `tailwind.config.js`.
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

To help speed up development builds, PurgeCSS is only run when you use the `tailwind build` management command (to create a production build of your CSS).

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

## Bugs and suggestions

If you have found a bug, please use the issue tracker on GitHub.

[https://github.com/timonweb/django-tailwind/issues](https://github.com/timonweb/django-tailwind/issues)

2020 (c) [Tim Kamanin - A Full Stack Django Developer](https://timonweb.com)
