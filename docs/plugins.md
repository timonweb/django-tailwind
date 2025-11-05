# Installing Tailwind CSS Plugins

> **Important:** Plugin installation via the `plugin_install` command is **only available for npm-based installations**. If you're using the standalone binary mode (initialized with `--tailwind-version 4s`), the `plugin_install` command is not supported. Standalone installations are limited to core Tailwind CSS features only.

Django Tailwind provides built-in support for managing Tailwind CSS plugins. This guide covers how to install, configure, and manage plugins in your Tailwind CSS projects.

## Overview

Tailwind CSS plugins extend the framework's functionality by adding new utilities, components, and base styles. Django Tailwind makes it easy to install and configure these plugins through management commands.

## Installing Plugins (npm-based Installation Only)

> **Note:** All commands in this section require an npm-based installation. These commands will not work with standalone binary installations.

### Using the plugin_install Command

The easiest way to install a Tailwind plugin is using the `plugin_install` management command:

```bash
python manage.py tailwind plugin_install <plugin-name>
```

This command will:
1. Install the plugin as a development dependency via npm
2. Automatically add the plugin configuration to your `styles.css` file
3. Handle duplicate prevention if the plugin is already installed

### Examples

**Install DaisyUI:**
```bash
python manage.py tailwind plugin_install daisyui
```

**Install Tailwind Typography:**
```bash
python manage.py tailwind plugin_install @tailwindcss/typography
```

## How Plugin Installation Works

When you run `python manage.py tailwind plugin_install <plugin-name>`, the following happens:

1. **NPM Installation**: The plugin is installed as a development dependency in your theme app's `package.json`
2. **Styles Configuration**: The plugin directive is added to your `styles.css` file right after the `@import "tailwindcss";` line
3. **Duplicate Prevention**: If the plugin is already installed, the command will detect it and skip installation

### Before Plugin Installation

Your `styles.css` file looks like this:
```css
@import "tailwindcss";
@source "../../**/*.{html,py,js}";

/* Your custom styles here */
```

### After Plugin Installation

After installing DaisyUI, your `styles.css` file will look like this:
```css
@import "tailwindcss";
@plugin "daisyui";
@source "../../**/*.{html,py,js}";

/* Your custom styles here */
```

## Popular Tailwind CSS Plugins

Here are some popular Tailwind CSS plugins you can install:

### DaisyUI
A comprehensive component library built on top of Tailwind CSS.

```bash
python manage.py tailwind plugin_install daisyui
```

**Features:**
- Semantic component classes (btn, card, modal, etc.)
- Multiple themes
- Accessible components
- Works with existing Tailwind utilities

### Tailwind Typography
Beautiful typographic defaults for HTML you don't control.

```bash
python manage.py tailwind plugin_install @tailwindcss/typography
```

**Usage:**
```html
<article class="prose lg:prose-xl">
  <h1>My Article Title</h1>
  <p>This content will have beautiful typography applied automatically.</p>
</article>
```

### Tailwind Forms
Better default styles for form elements.

```bash
python manage.py tailwind plugin_install @tailwindcss/forms
```

**Features:**
- Consistent form styling across browsers
- Better default appearance for form controls
- Easy to customize with Tailwind utilities

## Installing Plugins During Project Initialization (npm-based Only)

### DaisyUI Integration

For npm-based Tailwind v4 projects, you can include DaisyUI directly during project initialization:

```bash
python manage.py tailwind init --include-daisy-ui
```

This is equivalent to running:
```bash
python manage.py tailwind init
python manage.py tailwind plugin_install daisyui
```
