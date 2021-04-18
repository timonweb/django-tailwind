## Migrating from Django-Tailwind v1 to v2

> Please note that the instructions below are for upgrading the Django package, not for the actual dependency on Tailwind CSS.

*Django Tailwind2* `v2` introduces many new features that aren't available to projects generated with the
previous version of the package. Thus if you want to get all the goodies `v2` offers, you need to update your Django `theme` app.

Depending on how many customizations you have, the process can be smooth or bumpy.

### Steps to upgrade

Let's assume you've been using *Django Tailwind* for a while, and your `TAILWIND_APP_NAME` is `theme`.

1. Edit `INSTALLED_APPS` in `settings.py` file and remove the `'theme'` app.
2. Rename the `theme` app directory to `theme-legacy`.
3. Generate a new *Tailwind* theme app:

   ```bash
   python manage.py tailwind init
   ```
   Name it the same as your previous app: `theme`.
4. Add the `'theme'` back to `INSTALLED_APPS`;
5. Copy `theme-legacy/static_src/src` to `theme/static_src/src`;
6. If you have a file named `theme/static_src/src/styles.scss`, rename it to `theme/static_src/src/styles.css`. In `v2`
   we dropped support for *SASS*, but *POSTCSS* should work just fine. Unless you've used advanced *SASS* features, which
   is unlikely;
7. Open `theme-legacy/static_src/tailwind.config.js` and compare it with `theme/static_src/tailwind.config.js`, if you
   have customizations there, like custom colors, variables, etc., copy them to `theme/static_src/tailwind.config.js`;
8. Notice the `plugins` listed in `theme/static_src/tailwind.config.js`. We've now included the four
   official
   *Tailwind CSS* plugins there. If you see that your forms look weird after the update, you probably don't need
   the official `@tailwindcss/forms` package, so disable it by removing the following line:
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

13. If all went well, you should now be on the latest version of *Django Tailwind* with your previous styles intact.
