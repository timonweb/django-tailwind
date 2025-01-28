=================================================================
Tailwind CSS integration for Django a.k.a. Django + Tailwind = 💚
=================================================================

.. note::
   This is a maintained fork of Tim Kamanin's original django-tailwind project. The original project is no longer maintained. This fork updates the project to work with the latest version of Tailwind CSS while preserving the original functionality.

.. image:: https://github.com/rsevs3/django-tailwind-4/blob/main/docs/source/img/django-tailwind-demo-800.gif
   :alt: Django + Tailwind Demo

Goal
====

This project aims to provide a comfortable way of using the *Tailwind CSS* framework within a Django project.

Features
========

* An opinionated *Tailwind CSS* setup that makes your life easier;
* Hot reloading of CSS, configuration files, and *Django* templates. No more manual page refreshes!
* Out of the box support for CSS imports, SASS-like variables, and nesting;
* Includes official *Tailwind CSS* plugins like *typography*, *form*, *line-clamp*, and *aspect-ratio*;
* Supports the latest *Tailwind CSS* `v4.x`;

For instructions on upgrading from ``v2`` to ``v3``, see this post on `Tim Kamanin's blog <https://timonweb.com/django/django-tailwind-with-support-for-the-latest-tailwind-css-v3-is-out>`_.

Requirements
============

Python 3.10 or newer with Django >= 3.2 or newer.

Documentation
=============

The full documentation is at `https://django-tailwind-4.readthedocs.io <https://django-tailwind-4.readthedocs.io>`_

Installation
============

.. code-block:: console

   pip install django-tailwind-4

[RECOMMENDED IN DEV] If you want to use automatic page reloads during development use the `[reload]` extras, which installs the `django-browser-reload` package in addition:

.. code-block:: console

   pip install 'django-tailwind-4[reload]'

Check docs for the `Installation <https://django-tailwind-4.readthedocs.io/en/latest/installation.html>`_ instructions.

Bugs and suggestions
====================

Please see `CONTRIBUTING <CONTRIBUTING.md>`_.

2019 - 2023 (c) `Tim Kamanin - A Full Stack Django Developer <https://timonweb.com>`_

2024 - present (c) `Ryan Sevelj - Fork Maintainer <https://github.com/rsevs3/>`_


