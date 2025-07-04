# Tailwind CSS integration for Django a.k.a. Django + Tailwind = 💚
![Django Tailwind Demo](https://raw.githubusercontent.com/timonweb/django-tailwind/master/docs/django-tailwind-demo-800.gif)

## Goal
This project aims to provide a convenient way to use the *Tailwind CSS* framework within a Django project.

## Features
* An opinionated *Tailwind CSS* setup that makes your life easier;
* Hot reloading of CSS, configuration files, and *Django* templates. No more manual page refreshes!
* Out of the box support for CSS imports, Sass-like variables, and nesting;
* Supports the latest *Tailwind CSS* `v4.x`;
* Start both *Tailwind CSS* and *Django* development servers with a single command;

## Requirements
Python 3.10 or newer and Django 4.2.20 or newer.

## Documentation
The full documentation is at https://django-tailwind.readthedocs.io/ or in the [docs directory](docs/index.md) of this repository.

## Getting Started

1. **Install django-tailwind:**
   ```bash
   pip install django-tailwind
   ```

2. **Add to INSTALLED_APPS in settings.py:**
   ```python
   INSTALLED_APPS = [
       # ...
       'tailwind',
   ]
   ```

3. **Create Tailwind app:**
   ```bash
   python manage.py tailwind init
   ```

4. **Add the generated app to INSTALLED_APPS and configure:**
   ```python
   INSTALLED_APPS = [
       # ...
       'tailwind',
       'theme',  # your generated app name
   ]

   TAILWIND_APP_NAME = 'theme'
   ```

5. **Install Tailwind CSS dependencies:**
   ```bash
   python manage.py tailwind install
   ```

6. **Start development (runs Django + Tailwind):**
   ```bash
   python manage.py tailwind dev
   ```

7. **Use Tailwind classes in your templates:**
   ```html
   {% load tailwind_tags %}
   <link href="{% tailwind_css %}" rel="stylesheet">

   <h1 class="text-4xl font-bold text-blue-600">Hello Tailwind!</h1>
   ```

That's it! 🎉 Your Django project now has Tailwind CSS with hot reloading.

For configuring automatic page reloads during development, see the [Installation](docs/installation.md) instructions.

## Bugs and suggestions

Please see [CONTRIBUTING](CONTRIBUTING.md).

2019 - 2025 (c) [Tim Kamanin - A Full Stack Django Developer](https://timonweb.com)
