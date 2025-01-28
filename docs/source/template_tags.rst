=============
Template Tags
=============

Django Tailwind introduces a couple of template tags for your convenience.

{% tailwind_css %} tag
======================

Usage
_____

The ``{% tailwind_css %}`` tag generates a stylesheet link for the ``'theme'`` app and that’s all you need to include Tailwind’s CSS on a page:

.. code-block:: html+jinja

   {% load tailwind_tags %}
   <!DOCTYPE html>
   <html lang="en">
     <head>
       <title>Django Tailwind</title>
       {% tailwind_css %}
     </head>
     <body></body>
   </html>

Asset versioning
________________

The tag also supports asset versioning via the ``v=`` parameter, like this:

.. code-block:: html+jinja

   {% tailwind_css v='1' %}

Depending on your production setup, you may or may not need this functionality, so it’s optional.

{% tailwind_preload_css %} tag
==============================

Usage
_____

The tag generates a preload directive for your stylesheet, which improves loading performance in production. Place it above the ``{% tailwind_css %}`` tag:

.. code-block:: html+jinja

   {% load tailwind_tags %}
   <!DOCTYPE html>
   <html lang="en">
     <head>
       <title>Django Tailwind</title>
       {% tailwind_preload_css %}
       {% tailwind_css %}
     </head>
     <body></body>
   </html>

Asset versioning
________________

It also supports asset versioning (if needed):

.. code-block:: html+jinja

   {% tailwind_preload_css v='1' %}
