# Updating *Tailwind CSS* and its dependencies

When a new release of *Tailwind CSS* comes out, you can update your `theme` project without updating *Django Tailwind*.

The update process differs depending on whether you're using npm-based or standalone binary installation.

## Updating Standalone Binary Installations

If you're using the standalone binary mode (initialized with `--tailwind-version 4s`), updating is done via Django settings:

1. **Check available versions** by visiting the [Tailwind CSS releases page](https://github.com/tailwindlabs/tailwindcss/releases)

2. **Update the version** in your `settings.py`:

   ```python
   # settings.py
   TAILWIND_STANDALONE_BINARY_VERSION = "v4.2.0"  # Change to desired version
   ```

3. **Download the new binary**:

   ```bash
   python manage.py tailwind install
   ```

4. **Rebuild your CSS**:

   ```bash
   python manage.py tailwind build
   ```

> **Note:** The `check-updates` and `update` management commands are not available for standalone installations. Version management is handled through the `TAILWIND_STANDALONE_BINARY_VERSION` setting.

## Updating npm-based Installations

### Checking for updates to *Tailwind CSS* and its dependencies

Before updating, you can check if there are any updates. Run the following command:

```bash
python manage.py tailwind check-updates
```

This command runs the `npm outdated` command behind the scenes in the context of your `theme/static_src` directory.

If there are updates, you'll see a table of dependencies with the latest compatible versions. If there are no updates, this command will return no output.

> **Note:** This command only works with npm-based installations.

### Updating *Tailwind CSS* and its dependencies

To use the latest version of *Tailwind CSS*, run the following command:

```bash
python manage.py tailwind update
```

This command runs the `npm update` command behind the scenes in the context of your `theme/static_src` directory.

If there are updates, you'll see a log of updated dependencies. If there are no updates, this command will return no output.

> **Note:** This command only works with npm-based installations.
