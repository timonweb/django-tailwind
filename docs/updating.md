# Updating *Tailwind CSS* and its dependencies

When a new release of *Tailwind CSS* comes out, you can update your `theme` project without updating *Django Tailwind*.

## Checking if there are updates for *Tailwind CSS* and its dependencies

Before doing an update, you can check if there are any updates. Run the following command:
```bash
python manage.py tailwind check-updates
```
This command runs the `npm outdated` command behind the scenes in the context of your `theme/static_src` directory.

If there are updates, you'll see a table of dependencies with the latest compatible versions.
If there are no updates, this command will return no output.

## Updating Tailwind CSS and its dependencies

If you want to use the latest version of *Tailwind CSS*, run the following command:

```bash
python manage.py tailwind update
```
This command runs the `npm update` command behind the scenes in the context of your `theme/static_src` directory.

If there are updates, you'll see a log of updated dependencies.
If there are no updates, this command will return no output.
