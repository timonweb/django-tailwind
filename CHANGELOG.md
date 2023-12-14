# Changelog

## 3.7.0 [In Progress...]
- Upgrades Tailwind CSS dependencies;
- Removes `@tailwindcss/line-clamp` dependency as it's now included in Tailwind by default;
- Ensures Django 5.0 support;
- Drops Python 3.8 support;
- Ensures Python 3.12 support;


## 3.6.0
- Adds support for Django 4.2.
- Stops caching CSS in DEBUG mode.
- Makes django-browser-reload dependency optional to install by using the [reload] extras.
- Adds instructions on how to contribute

## 3.5.0
- Upgrades Tailwind CSS dependencies;
- Updates Django dev dependencies;

## 3.4.0
- Upgrades Tailwind CSS dependencies;
- Updates Django dev dependencies;

## 3.3.0
- Makes `cookiecutter` dependency optional by installing it automatically when `python manage.py tailwind init` is run;
- Updates Django dev dependencies;

## 3.2.0
- Upgrades Tailwind CSS dependencies;
- Upgrades Django dependencies;

## 3.1.1

- Brings removed `browser-sync` snippet to support legacy configs;
- Follow [migrating from `browser-sync` to `django-browser-reload`](./docs/django_browser_reload.md) instructions if you've upgraded.

## 3.1.0

- Replaces `nodemon` and `browser-sync` with `django-browser-reload`;
- Deprecates `TAILWIND_DEV_MODE` setting, the development mode now is deemed when `DEBUG=True`;
- Updates *Tailwind CSS* dependencies to their latest versions;
- Removes `--no-sync` flag for `python manage.py tailwind start` command;

## 3.0.1

- Fixes minimum Django version requirement. Sets it back to `2.2`.

## 3.0.0

- Upgrades project template to be compatible with Tailwind CSS `v3.0`;
- Drops Tailwind CSS `v2.x` support;
- If you're not starting fresh, [follow the upgrade guide](https://tailwindcss.com/docs/upgrade-guide) to upgrade existing Tailwind CSS `v2.x` to `v3.x`;

## 2.3.0

- Drops support for Python 3.7 and Django 2.x;
- Updates Tailwind CSS to 2.2.19;

## 2.2.0

- Adds support for Tailwind CSS v2.2;
- Updates Tailwind CSS dependencies;
- Adds `TAILWIND_DEV_MODE` config variable;

## 2.0.1

- Updates `purge` rules in `tailwind.config.js` to include other Django app templates by default;

## 2.0.0

- Adds JIT mode support;
- Adds Hot reloading for CSS, templates and config files;
- Adds full documentation;

## 1.2.0

- Drops Tailwind v1 support;
- Adds official Tailwind plugins: typography, form, line-clamp and aspect-ratio.

## 1.1.2

- Removes the upper bound on the Django version.

## 1.1.1

- Adds `cross-env` that enables cross-platform support for `NODE_ENV` setting.

## 1.1.0

- Enables Purge CSS by default in Tailwind CSS v2 template
- Improves Windows support

## 1.0.0 🎉

- Adds support for Tailwind CSS 2.0
- Moves Tailwind CSS 1.0 support under `--legacy` flag

## 0.11.1

- Adds `manage.py tailwind check-updates` and `manage.py tailwind update` commands

## 0.11.0

- Updates tailwindcss to 1.9.6
- Updates tailwind.config.js

## 0.10.0

- Adds Django 3.1 support
- Adds Purge CSS support and instructions
- Fixes failing tests, we're green now!
- Updates tailwindcss to 1.6.2
- Updates tailwind.config.js

## 0.9.0

- Updates script commands in package.json
- Fixes SASS support

## 0.8.0

- Updates tailwindcss to 1.4.6
- Updates tailwind.config.js

## 0.7.0

- Updates tailwindcss to 1.2.0
- Updates tailwind.config.js

## 0.6.1

- Updates tailwindcss to 1.1.4
- Updates other dependencies in package.json
