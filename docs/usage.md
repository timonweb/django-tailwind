# Usage

## Running in Development Mode

To start Django Tailwind in development mode, run the following command in a terminal:

```bash
python manage.py tailwind start
```

This will start a long-running process that watches files for changes. Use `CTRL + C` to terminate the process.

Several things happen behind the scenes:

1. The stylesheet is updated every time you add or remove a CSS class in a Django template.
2. The `django-browser-reload` watches for changes in HTML and CSS files. When a Django template or CSS file is updated, the browser refreshes automatically, providing a smooth development experience without needing to reload the page manually.

## Building for Production

To create a production build of your theme, run:

```bash
python manage.py tailwind build
```

This will replace the development build with a bundle optimized for production. No further actions are necessary; you can deploy!
