# Tailwind CSS integration for Django a.k.a. Django + Tailwind = 💚

>**Note:** This is a maintained fork of Tim Kamanin's original django-tailwind project. The original project is no longer maintained. This fork updates the project to work with the latest version of Tailwind CSS while preserving the original functionality.

![Django Tailwind Demo](https://raw.githubusercontent.com/timonweb/django-tailwind/master/docs/django-tailwind-demo-800.gif)

## Goal
This project aims to provide a comfortable way of using the *Tailwind CSS* framework within a Django project.

## Features
* An opinionated *Tailwind CSS* setup that makes your life easier;
* Hot reloading of CSS, configuration files, and *Django* templates. No more manual page refreshes!
* Out of the box support for CSS imports, SASS-like variables, and nesting;
* Includes official *Tailwind CSS* plugins like *typography*, *form*, *line-clamp*, and *aspect-ratio*;
* Supports the latest *Tailwind CSS* `v4.x`;

> [For instructions on upgrading from `v2` to `v3`, see this post on Tim Kamanin's blog](https://timonweb.com/django/django-tailwind-with-support-for-the-latest-tailwind-css-v3-is-out/).

## Requirements
Python 3.10 or newer with Django >= 3.2 or newer.

## Documentation
The full documentation is at https://django-tailwind-4.readthedocs.io

## Installation
Via PIP:
```bash
pip install django-tailwind
```

[RECOMMENDED IN DEV] If you want to use automatic page reloads during development use the `[reload]` extras, which installs the `django-browser-reload` package in addition:

 ```bash
 pip install 'django-tailwind[reload]'
 ```

Check docs for the [Installation](https://django-tailwind-4.readthedocs.io/en/latest/installation.html) instructions.

## Bugs and suggestions

Please see [CONTRIBUTING](CONTRIBUTING.md).

2019 - 2023 (c) [Tim Kamanin - A Full Stack Django Developer](https://timonweb.com)
2024 - present (c) [Ryan Sevelj] - Fork Maintainer
