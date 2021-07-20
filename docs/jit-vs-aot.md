# mode: Just in time VS Ahead of time

*Tailwind CSS* comes with two stylesheet generation modes to choose from:

1. Just in time (`jit`) - is the recommended mode. In this mode, Tailwind builds your stylesheet dynamically as you add/remove classes from your templates.
2. Ahead of time (`aot`) - is a legacy mode. In this mode, Tailwind builds the stylesheet with all classes available in the framework. As a result, you might end up with a huge stylesheet. To alleviate this, the production mode uses *Purge CSS* that removes unused styles from the stylesheet and dramatically reduces its size. But still, it's not as good as the `jit` mode.
   
If you run the `python manage.py tailwind init` command, you'll see a prompt to choose one of the modes. You can always change the selected mode later by editing your generated `theme/static_src/tailwind.config.js` file.
