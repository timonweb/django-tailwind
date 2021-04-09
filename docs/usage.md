# Usage

## Running in the development mode

To start Django Tailwind in the development mode run the following command in a terminal:
```bash
python manage.py tailwind start
```

It will start a long-running process that watches files for changes. Use a combination of `CTRL` + `C` to terminate the process.

Several things are happening behind the scenes at that moment:

1. If Tailwind `jit` mode is enabled, a stylesheet is being updated every time you add or remove a css class to a Django template.
2. *Browser-sync* service watches for HTML and CSS changes. When HTML page is updated, browser page reloads. When a CSS file updates, it fetches the update without reloading a page. This gives you a smooth development experience without a need to reload a page to see updates.
3. *Nodemon* watches for changes in config files (`tailwind.config.js`, `postcss.config.js`, `bs.config.js`) and restarts the long-polling process every time there's a change in those files.

If by somewhat reason you don't want to use hot-reloading, you can run the long-polling process with `--no-sync` option to disable hot reloading:

```bash
python manage.py tailwind start --no-sync
```

## Building for production

To create a production build of your theme, run:

```bash
python manage.py tailwind build
```

It will replace the development build with a bundle optimized for production. No further actions are necessary, you can deploy!
