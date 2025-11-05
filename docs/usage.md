# Usage

## Running in Development Mode

### Option 1: Combined Development Server (Recommended)

To start both Django server and Tailwind watcher simultaneously, run:

```bash
python manage.py tailwind dev
```

This will start both processes using Honcho and provide a seamless development experience. Use `CTRL + C` to terminate both processes.

> This mode doesn't work on Windows due to limitations with Honcho. If you're using Windows, please use Option 2 below.

### Option 2: Separate Processes

To start only the Tailwind watcher in development mode, run the following command in a terminal:

```bash
python manage.py tailwind start
```

This will start a long-running process that watches files for changes. Use `CTRL + C` to terminate the process.

**Note:** When using the separate process approach, you'll need to run `python manage.py runserver` in another terminal to start the Django development server.

## How Development Mode Works

Several things happen behind the scenes:

1. The stylesheet is updated every time you add or remove a CSS class in a Django template.
   - **npm-based installations:** Uses npm scripts and PostCSS to watch and compile changes
   - **Standalone installations:** Uses the Tailwind CSS standalone binary to watch files directly
2. The `django-browser-reload` watches for changes in HTML and CSS files. When a Django template or CSS file is updated, the browser refreshes automatically, providing a smooth development experience without needing to reload the page manually.

## Customizing the Development Setup

### Procfile.tailwind Configuration

When you run `python manage.py tailwind dev` for the first time, a `Procfile.tailwind` file is automatically created in your project root with the following default content:

```
django: python manage.py runserver
tailwind: python manage.py tailwind start
```

This file defines the processes that Honcho will run simultaneously. Each line follows the format: `process_name: command_to_run`.

### Customization Examples

You can edit `Procfile.tailwind` to customize your development commands:

```
django: python manage.py runserver 0.0.0.0:8080
tailwind: python manage.py tailwind start
```

### Process Management

- **Starting processes:** `python manage.py tailwind dev` starts all processes defined in the Procfile
- **Stopping processes:** Press `Ctrl+C` to stop all processes gracefully
- **Process output:** Each process is color-coded in the terminal for easy identification

## Building for Production

To create a production build of your theme, run:

```bash
python manage.py tailwind build
```

This will replace the development build with a bundle optimized for production. No further actions are necessary; you can deploy!

**Implementation details:**
- **npm-based installations:** Runs the build script defined in package.json (typically with `NODE_ENV=production`)
- **Standalone installations:** Uses the Tailwind CSS standalone binary with `--minify` flag

The resulting CSS file is functionally identical regardless of which installation method you use.
