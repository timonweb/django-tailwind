# Settings

_Django Tailwind_ comes with preconfigured settings. You can override them in
the `settings.py` of your Django project.

## `TAILWIND_APP_NAME`

This defines the _Tailwind_ theme Django app containing your _Tailwind CSS_
styles. I prefer to name such an app `'theme'`. You should generate the app
during the installation phase by running the following command:

```html
python manage.py tailwind init
```

Please refer to the [Installation](installation.md) section for more information
on the installation process.

## `TAILWIND_DEV_MODE`

Determines whether the `browser-sync` snippet is added to the page via the
`{% tailwind_css %}` tag. It is set to `DEBUG` by default, but you can override
this value.

## `NPM_BIN_PATH`

This defines a path to the `npm` executable in your system.

> _Tailwind CSS_ requires you to have _Node.js_ installed on your machine.
> _Node.js_ is a _JavaScript_ runtime that allows running _JavaScript_ code
> outside a browser. Most of the current frontend tools depend on _Node.js_.

> If you don't have _Node.js_ installed on your machine, please follow
> installation instructions from
> [the official Node.js page](https://nodejs.org/).

The default value is:

```html
NPM_BIN_PATH = 'npm'
```

## `TAILWIND_CSS_PATH`

This defines a path to the generated _Tailwind CSS_ stylesheet. If you have
created a theme app via the `python manage.py tailwind init` command, chances
are you don't need to change this value.

However, if you integrated _Tailwind CSS_ in another way or want to use a _CDN_
version of the bundle, you might want to change the path.

The default value is:

```html
TAILWIND_CSS_PATH = 'css/dist/styles.css'
```
