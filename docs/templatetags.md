# Template tags

*Django Tailwind* introduces a couple of template tags for your convenience.

## {% tailwind_css %} tag

### Usage
The `{% tailwind_css %}` tag generates a stylesheet link for the `'theme'` app and that's all you need to include *Tailwind's CSS* on a page:

```html
{% load tailwind_tags %}
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>Django Tailwind</title>
    {% tailwind_css %}
  </head>
  <body></body>
</html>
```

### Asset versioning
The tag also supports asset versioning via the `v=` parameter, like this:

```html
{% tailwind_css v='1' %}
```

Depending on your production setup, you may or may not need this functionality, so it's optional.

### Hot reloading
This tag also includes the `browser-sync` script that reloads a page whenever the template changes.
This script is only included on the page when two conditions are met:
* The debug mode is enabled in `settings.py`: `DEBUG=True`;
* Your IP address matches `INTERNAL_IPS` defined in `settings.py`. For local development, it usually should contain `127.0.0.1` to work properly:
  ```python
  INTERNAL_IPS = ['127.0.0.1']
  ```

## {% tailwind_preload_css %} tag

The tag generates a preload directive for your stylesheet, which improves loading performance in production.
Place it above the `{% tailwind_css %}` tag:

```html
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
```

It also supports asset versioning (if needed):

```html
{% tailwind_preload_css v='1' %}
```
