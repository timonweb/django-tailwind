# Tailwind CSS integration for Django a.k.a. Django + Tailwind = 💚

![Tests](https://github.com/timonweb/django-tailwind/actions/workflows/tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/django-tailwind.svg?style=flat-square)](https://pypi.org/project/django-tailwind/)
![GitHub](https://img.shields.io/github/license/timonweb/django-tailwind?style=flat-square)
![Python versions](https://img.shields.io/pypi/pyversions/django-tailwind)
[![Downloads](https://static.pepy.tech/badge/django-tailwind)](https://pepy.tech/project/django-tailwind)
[![Downloads / Month](https://pepy.tech/badge/django-tailwind/month)](<https://pepy.tech/project/django-tailwind>)

![Django Tailwind Demo](https://raw.githubusercontent.com/timonweb/django-tailwind/master/docs/django-tailwind-demo-800.gif)

## Goal

This project provides a convenient way to integrate the *Tailwind CSS* framework into a Django project.
It creates a new Django app (named theme by default) that includes all the necessary files and configurations to get started with *Tailwind CSS* quickly.

## Features

* An opinionated *Tailwind CSS* setup that makes your life easier;
* Hot reloading of CSS, configuration files, and *Django* templates. No more manual page refreshes!
* Out of the box support for CSS imports, Sass-like variables, and nesting;
* Supports the latest *Tailwind CSS* `v4.x`;
* Start both *Tailwind CSS* and *Django* development servers with a single command;
* An optional DaisyUI integration to spice up your Tailwind templates with pre-built components.
* A convenient management command for installing Tailwind CSS plugins;

## Requirements

Python 3.10 or newer and Django 4.2.20 or newer.

## Documentation

The full documentation is at https://django-tailwind.readthedocs.io/ or in the [docs directory](docs/index.md) of this
repository.

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

That's it! 🎉 Your Django project now has Tailwind CSS installed and ready to use.

For configuring automatic page reloads during development, see the [Installation](docs/installation.md) instructions.

## Bugs and suggestions

Please see [CONTRIBUTING](CONTRIBUTING.md).

2019 - 2025 (c) [Tim Kamanin - A Full Stack Django Developer](https://timonweb.com)
