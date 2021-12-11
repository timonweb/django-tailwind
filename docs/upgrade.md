# Upgrading from v2 to v3

If you're coming from *Django-Tailwind* `2.x`, your *Tailwind CSS* project probably depends on *Tailwind CSS* `2.x`. If
you want to use latest features of the version `3.x`, you need to upgrade your *Tailwind CSS* app from `2.x` to `3`.

In the following instructions, I assume that your *Tailwind CSS* app name is set as `TAILWIND_APP_NAME = 'theme'` in `settings.py`. 

If it's different for you, please replace the `theme` with an app name of your choice, while following my steps.

Let's do this!

1. Update *Django-Tailwind* to `3.x` by running the following command:

     ```bash
     pip install --upgrade django-tailwind
     ```
   
2. Next, update dependencies and plugins via `npm`. Go to **theme/static_src** directory and run the following command:

     ```bash
     npm install -D tailwindcss@latest \
       @tailwindcss/typography@latest \
       @tailwindcss/forms@latest \
       @tailwindcss/aspect-ratio@latest \
       @tailwindcss/line-clamp@latest \
       postcss@latest \
       autoprefixer@latest
     ```

3. Now, open **theme/static_src/bs.config.js** and replace `...tailwindConfig.purge` with `...tailwindConfig.content`,
4. Then, open **theme/static_src/tailwind.config.js** in a code editor, and
5. Remove the `mode` property. In Tailwind `3.0`, `jit` is always on, so there's no use of `mode: jit` string anymore,
6. Rename `purge` to `content`,
7. Remove dark mode configuration by deleting the line containing `darkMode`,
8. Staying with the open **theme/static_src/tailwind.config.js** file, refer to the [official Tailwind CSS upgrade guide](https://tailwindcss.com/docs/upgrade-guide) and see if there's anything else you need to change in your **tailwind.config.js**. In most cases everything should already be fine, but depending on your configuration, some parts may need your attention.

And that's it. You're now on the latest Django-Tailwind `3.0` with the latest Tailwind CSS `3.0` installed and ready to go.
