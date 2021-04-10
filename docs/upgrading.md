# Upgrading

## Updating *Tailwind CSS* and its dependencies

If there's a new release of the *Tailwind CSS* came out you can update your `theme` project
without updating *Django Tailwind*.

### Checking if there are updates for *Tailwind CSS* and its dependencies

Before doing an update, you can check if there are any updates. Run the following command:
```bash
python manage.py tailwind check-updates
```
Behind the scenes this command it runs the `npm outdated` command in the context of your `theme/static_src` directory.

If there are updates, you'll see a table dependencies with the latest compatible versions.
If there are no updates, this command will return no output.

### Updating Tailwind CSS and its dependencies

If you want to use the latest version of *Tailwind CSS*, run the following command:

```bash
python manage.py tailwind update
```
Behind the scenes this command runs the `npm update` command in the context of your `theme/static_src` directory.

If there are updates, you'll see a log of updated dependencies.
If there are no updates, this command will return no output.

## Upgrading from Django-Tailwind v1 to v2

> Please note, that the instructions below are for upgrading the Django package,
not the actual Tailwind CSS dependency.

*Django Tailwind2* `v2` introduces lots of new features that aren't available to projects,
that were generated with the previous version. Thus if you want to get all the goodies `v2` offers,
you need to update your Django `theme` app.

Depending on how many customizations you've introduced, the process might be smooth or bumpy.

### Upgrade steps

Let's assume, you've been using *Django Tailwind* for a while and you your `TAILWIND_APP_NAME` is `theme`.

1. Edit `INSTALLED_APPS` in `settings.py` and remove the `'theme'` app.
2. Rename your `theme` app directory to `theme-legacy`.
3. Generate a new *Tailwind* theme app:
   
   ```bash
   python manage.py tailwind init
   ```
   Name it like your previous app was named: `theme`.
4. Add `'theme'` back to `INSTALLED_APPS`;
5. Copy `theme-legacy/static_src/src` to `theme/static_src/src`;
6. If you have a file named `theme/static_src/src/styles.scss`, rename it to `theme/static_src/src/styles.css`. In `v2` we've dropped *SASS* support, but *POSTCSS* should work just fine. Unless you've used advanced *SASS* features, which is unlikely;
7. Open `theme-legacy/static_src/tailwind.config.js` and compare it to `theme/static_src/tailwind.config.js`, if you have customizations there, like custom colors, variables, etc, copy them over to `theme/static_src/tailwind.config.js`;
8. Pay close attention to the `plugins` listed in `theme/static_src/tailwind.config.js`. We now include there four official
   *Tailwind CSS* plugins. If you see that your forms look weird after the upgrade, that means probably you don't need the `@tailwindcss/forms` so remove the following line:
   ```html
   require('@tailwindcss/forms'),
   ```
   from the `theme/static_src/tailwind.config.js`.
9. Copy `theme-legacy/templates` to `theme/templates`;
10. Open `theme/templates/base.html` and add `{% load tailwind_tags %}` to the beginning of the file. Then, replace:
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
11. To install dependencies, run the following command:
    ```python
    python manage.py tailwind install
    ```
12. Now start the development server:
    ```python
    python manage.py tailwind start
    ```
13. If all went well, you should now be on the latest *Django Tailwind* version with your previous styles preserved.
