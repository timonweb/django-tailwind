# A Tailwind integration for Django Projects

Early alpha, work in progress...

## Quick start

1. Install the python package django-tailwind from pip

   `pip install django-tailwind`

   Alternatively, you can download or clone this repo and run `pip install -e .`.

2. Add `tailwind` to INSTALLED_APPS in **settings.py**

3. Create a tailwind-compatible Django-app, I like to call it `theme`:

   `python manage.py tailwind init theme`

4. Add your newly created `theme` app to INSTALLED_APPS in **settings.py**

5. In settings.py, register tailwind app by adding the following string:

   `TAILWIND_APP_NAME = 'theme'`

6. Run a command to install all necessary dependencies for tailwind css:

   `python manage.py tailwind install`

7. Now, go and start tailwind in dev mode:

   `python manage.py tailwind start`

8. Add `styles.min.css` to your `base.html` template file:

   ```html
   <link
     rel="stylesheet"
     href="{% static 'css/styles.min.css' %}"
     type="text/css"
   />
   ```

9. You should now be able to use Tailwind css classes in your html.

10. To build a production version of CSS run:

    `python manage.py tailwind build`.

## Bugs and suggestions

If you have found a bug, please use the issue tracker on GitHub.

[https://github.com/timonweb/django-tailwind/issues](https://github.com/timonweb/django-tailwind/issues)
