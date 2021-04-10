# Settings

*Django Tailwind* comes with preconfigured settings.
You can override them in the `settings.py` of your Django project.

## `NPM_BIN_PATH`
Is the path to the `npm` executable in your system.

> *Tailwind CSS* requires you to have *Node.js* installed on your machine.
> *Node.js* is a *JavaScript* runtime that allows running *JavaScript* code outside a browser. Most of the current frontend tools requires *Node.js*.
>
> If you don't have *Node.js* installed on your machine, please follow installation instructions from [the official Node.js page](https://nodejs.org/).

The default value is:
```html
NPM_BIN_PATH = 'npm'
```

## `TAILWIND_CSS_PATH`
Is the path to *Tailwind CSS* bundle. If you have created a theme app via the `python manage.py tailwind init` command,
chances are you don't need to change it. 

However, if you use integrate with *Tailwind CSS* in another way or want to use a *CDN* version of the bundle, you might want to change the path.

The default value is:
```html
TAILWIND_CSS_PATH = 'css/dist/styles.css'
```
