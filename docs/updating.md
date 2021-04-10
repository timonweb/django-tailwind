# Updating *Tailwind CSS* and its dependencies

If there's a new release of the *Tailwind CSS* came out you can update your `theme` project
without updating *Django Tailwind*.

## Checking if there are updates for *Tailwind CSS* and its dependencies

Before doing an update, you can check if there are any updates. Run the following command:
```bash
python manage.py tailwind check-updates
```
Behind the scenes this command it runs the `npm outdated` command in the context of your `theme/static_src` directory.

If there are updates, you'll see a table dependencies with the latest compatible versions.
If there are no updates, this command will return no output.

## Updating Tailwind CSS and its dependencies

If you want to use the latest version of *Tailwind CSS*, run the following command:

```bash
python manage.py tailwind update
```
Behind the scenes this command runs the `npm update` command in the context of your `theme/static_src` directory.

If there are updates, you'll see a log of updated dependencies.
If there are no updates, this command will return no output.
