# Usage

## Running in development mode

To start Django Tailwind in development mode, run the following command in a terminal:
```bash
python manage.py tailwind start
```

This will start a long-running process that watches files for changes. Use a combination of `CTRL` + `C` to terminate the process.

Several things are happening behind the scenes at that moment:

1. When *Tailwind CSS* `jit` mode is enabled, a stylesheet is updated every time you add or remove a CSS class in a Django template.
2. The `browser-sync` service watches for changes in HTML and CSS files. When a Django template page is updated, a browser reloads it. When a CSS file is updated, `browser-sync` applies updates without reloading the page. That gives you a smooth development experience without the need to reload the page to see updates.
3. The `nodemon` watches for config file changes (`tailwind.config.js`, `postcss.config.js`, `bs.config.js`) and restarts the long-polling process every time there's a change in those files.

If by somewhat reason you don't want to use hot-reloading, you can run the long-polling process with the `--no-sync` option to disable hot reloading:

```bash
python manage.py tailwind start --no-sync
```

## Building for production

To create a production build of your theme, run:

```bash
python manage.py tailwind build
```

This will replace the development build with a bundle optimized for production. No further actions are necessary; you can deploy!
