# Settings

*Django Tailwind* comes with preconfigured settings.
You can override them in the `settings.py` file of your Django project.

## `TAILWIND_APP_NAME`
This defines the *Tailwind* theme Django app containing your *Tailwind CSS* styles. It is recommended to name this app `'theme'`. You should generate the app during the installation phase by running the following command:
```bash
python manage.py tailwind init
```
Please refer to the [Installation](installation.md) section for more information on the installation process.

## `NPM_BIN_PATH` (npm-based installation only)

> **Note:** This setting only applies to npm-based installations. Skip if using the standalone binary mode.

This defines the path to the `npm` executable on your system.

> *Tailwind CSS* requires you to have *Node.js* installed on your machine.
> *Node.js* is a *JavaScript* runtime that allows running *JavaScript* code outside a browser. Most current frontend tools depend on *Node.js*.
>
> If you don't have *Node.js* installed, please follow the installation instructions on [the official Node.js page](https://nodejs.org/).

The default value is:
```python
NPM_BIN_PATH = "npm"
```

Please note that on *Windows* the path might look different (pay attention to the "backslashes" in the path):

```python
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
```

## `TAILWIND_USE_STANDALONE_BINARY`

This setting determines whether to use the Tailwind CSS standalone binary instead of npm-based installation.

The default value is:
```python
TAILWIND_USE_STANDALONE_BINARY = False
```

When set to `True`, Django Tailwind will use the [pytailwindcss](https://github.com/timonweb/pytailwindcss) package to run the Tailwind CSS standalone binary. This eliminates the need for Node.js and npm.

> **Note:** In most cases, you don't need to set this manually. Django Tailwind automatically detects standalone installations by checking for the presence of `package.json` in your theme app. If you initialized your app with `--tailwind-version 4s`, this detection happens automatically.

To explicitly enable standalone mode:

```python
# settings.py
TAILWIND_USE_STANDALONE_BINARY = True
```

## `TAILWIND_STANDALONE_BINARY_VERSION`

This setting specifies which version of the Tailwind CSS standalone binary to use.

The default value is:
```python
TAILWIND_STANDALONE_BINARY_VERSION = "v4.1.16"
```

You can specify any valid Tailwind CSS version tag. To upgrade to a newer version:

```python
# settings.py
TAILWIND_STANDALONE_BINARY_VERSION = "v4.2.0"
```

After changing this setting, run `python manage.py tailwind install` to download the new binary version.

> **Note:** This setting only applies when using standalone binary mode. For npm-based installations, the version is controlled by the `package.json` file in your theme app.

**Finding available versions:**

Visit the [Tailwind CSS releases page](https://github.com/tailwindlabs/tailwindcss/releases) to see all available versions. Use the tag name (e.g., `v4.1.16`) as the value for this setting.

## `TAILWIND_STANDALONE_START_COMMAND_ARGS`

> **Note:** This setting only applies when using standalone binary mode.

This setting defines the command-line arguments passed to the Tailwind CSS standalone binary when running in watch mode (via `python manage.py tailwind start`).

The default value is:
```python
TAILWIND_STANDALONE_START_COMMAND_ARGS = (
    "-i static_src/src/styles.css -o static/css/dist/styles.css --watch"
)
```

You can customize this to use different input/output paths or add additional Tailwind CLI options:

```python
# settings.py
TAILWIND_STANDALONE_START_COMMAND_ARGS = (
    "-i theme/static_src/input.css -o theme/static/output.css --watch --minify"
)
```

> **Note:** The output path automatically uses the value from `TAILWIND_CSS_PATH` in the default configuration. If you override this setting, ensure your paths are correct.

## `TAILWIND_STANDALONE_BUILD_COMMAND_ARGS`

> **Note:** This setting only applies when using standalone binary mode.

This setting defines the command-line arguments passed to the Tailwind CSS standalone binary when building for production (via `python manage.py tailwind build`).

The default value is:
```python
TAILWIND_STANDALONE_BUILD_COMMAND_ARGS = (
    "-i static_src/src/styles.css -o static/css/dist/styles.css --minify"
)
```

You can customize this to use different input/output paths or modify build options:

```python
# settings.py
TAILWIND_STANDALONE_BUILD_COMMAND_ARGS = (
    "-i theme/static_src/input.css -o theme/static/output.css --minify --optimize"
)
```

> **Note:** The output path automatically uses the value from `TAILWIND_CSS_PATH` in the default configuration. If you override this setting, ensure your paths match your project structure.

## `TAILWIND_CSS_PATH`
This defines the path to the generated *Tailwind CSS* stylesheet. If you created a theme app via the `python manage.py tailwind init` command, you likely don't need to change this value.

However, if you integrated *Tailwind CSS* in another way or want to use a *CDN* version of the bundle, you might want to change the path.

The default value is:
```python
TAILWIND_CSS_PATH = "css/dist/styles.css"
```

## `TAILWIND_DEV_MODE` (deprecated)
Determines whether the `browser-sync` snippet is added to the page via the `{% tailwind_css %}` tag. It is set to `False` by default. If you use a legacy pre-`3.1.0` configuration and rely on `browser-sync`, add `TAILWIND_DEV_MODE=True` to your `settings.py`.
