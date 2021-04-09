# Upgrading

## Updating Tailwind CSS and NPM dependencies

If there's a new release of the Tailwind CSS came out you can update your `theme` project
without updating this django package.

### Checking if there are updates for Tailwind css and its dependencies

Before doing an update, you can check if there are any updates. Run the following command:
```bash
python manage.py tailwind check-updates
```
*Behind the scenes it runs `npm outdated` command within your `theme/static_src` directory.*

If there are updates, you'll see a table dependencies with the latest compatible versions.
If there are no updates, this command will return no output.

### Updating Tailwind CSS and its dependencies

If you want to use the latest version of tailwind css, run the following command:

```bash
python manage.py tailwind update
```
*Behind the scenes it runs `npm update` command within your `theme/static_src` directory.*

If there are updates, you'll see a log of updated dependencies.
If there are no updates, this command will return no output.

## Upgrading from Django-Tailwind v1 to v2

> Please note, that the instructions below are for upgrading the Django package,
not the actual Tailwind CSS dependency.

*Django-Tailwind v2* introduces lots of new features that aren't available to projects,
that were generated with the previous version. Thus if you want to get all the goodies v2 offers,
you need to update your Django `theme` app.

Depending on how many customizations you've introduced, the process might be smooth or bumpy.

### Upgrade steps

Let's assume, you have a django-tailwind app installed that is called `theme`.

1. Go to `INSTALLED_APPS` in *settings.py* and remove the `'theme'` app.
2. Rename your `theme` app directory to `theme-legacy`.
3. Generate a new Tailwind app:
   
   ```bash
   python manage.py tailwind init
   ```
   Name it like your previous app was named: `theme`.
4. Add `'theme'` back to `INSTALLED_APPS`;
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
