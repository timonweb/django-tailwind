## Upgrading from Tailwind CSS 2.1 to 2.2

*Tailwind CSS* `2.2` has introduced a few breaking changes which means you have to update your `TAILWIND_APP`
configuration.

In the following steps, we assume that your `TAILWIND_APP_NAME` is `theme`; replace it with your theme name if it is
different.

1. Install the latest *Django-Tailwind* version via `pip`:

    ```bash
    pip install django-tailwind
    ```

2. Open the `theme/static_src/postcss.config.js` and remove the following two lines from it:

   ```javascript
       tailwindcss: {},
       autoprefixer: {},
   ```

   We do this because `autoprefixer` is now built into *Tailwind CSS* `v2.2`, and `tailwindcss` is now a command-line
   tool, not a *postcss* plugin.

3. Now open the `theme/static_src/package.json` and update its `scripts` section to look like:

   ```json
    "scripts": {
        "start": "npm run dev",
        "build": "npm run build:clean && npm run build:tailwind",
        "build:clean": "rimraf ../static/css/dist",
        "build:tailwind": "cross-env NODE_ENV=production tailwindcss --postcss -i ./src/styles.css -o ../static/css/dist/styles.css --minify",
        "sync": "browser-sync start --config bs.config.js",
        "dev:tailwind": "cross-env NODE_ENV=development tailwindcss --postcss -i ./src/styles.css -o ../static/css/dist/styles.css -w",
        "dev:sync": "run-p dev:tailwind sync",
        "dev": "nodemon -x \"npm run dev:sync\" -w tailwind.config.js -w postcss.config.js -w bs.config.js -e js",
        "tailwindcss": "node ./node_modules/tailwindcss/lib/cli.js"
    },
   ```

   Here we replaced the `postcss` command with the `tailwindcss` command.

4. Staying in `theme/static_src/package.json`, find the *tailwindcss* dependency in `devDependencies` and make sure its
   value is set to `"~2.2.4"`. This way, you bind the *Tailwind CSS* version to the `2.2.x` branch, which gives you
   better control over future updates to the *Tailwind CSS* version.

5. Go to the `theme/static_src` directory and run the following command to install the updates:

   ```bash
   npm install
   ```

Congrats, you're done with the upgrade!

## Migrating from Django-Tailwind v1 to v2

> Please note that the instructions below are for upgrading the Django package, not for the actual dependency on Tailwind CSS.

*Django Tailwind2* `v2` introduces many new features that aren't available to projects generated with the previous
version of the package. Thus if you want to get all the goodies `v2` offers, you need to update your Django `theme` app.

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
5. Make sure that `INTERNAL_IPS` list is present in the `settings.py` file and contains the `127.0.0.1` ip address:

       ```python
       INTERNAL_IPS = [
           "127.0.0.1",
       ]
       ```

6. Copy `theme-legacy/static_src/src` to `theme/static_src/src`;
7. If you have a file named `theme/static_src/src/styles.scss`, rename it to `theme/static_src/src/styles.css`. In `v2`
   we dropped support for *SASS*, but *POSTCSS* should work just fine. Unless you've used advanced _SASS_ features,
   which is unlikely;
8. Open `theme-legacy/static_src/tailwind.config.js` and compare it with `theme/static_src/tailwind.config.js`, if you
   have customizations there, like custom colors, variables, etc., copy them to `theme/static_src/tailwind.config.js`;
9. Notice the `plugins` listed in `theme/static_src/tailwind.config.js`. We've now included the four official *Tailwind
   CSS* plugins there. If you see that your forms look weird after the update, you probably don't need the
   official `@tailwindcss/forms` package, so disable it by removing the following line:
   ```html
   require('@tailwindcss/forms'),
   ```
   from the `theme/static_src/tailwind.config.js`.
10. Copy `theme-legacy/templates` to `theme/templates`;
11. Open `theme/templates/base.html` and add `{% load tailwind_tags %}` to the beginning of the file. Then, replace:

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

12. To install dependencies, run the following command:

    ```python
    python manage.py tailwind install
    ```

13. Now start the development server:

    ```python
    python manage.py tailwind start
    ```

14. If all went well, you should now be on the latest version of _Django Tailwind_ with your previous styles intact.
