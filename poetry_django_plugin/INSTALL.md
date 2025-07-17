# Installation Guide

## Installing the Plugin

1. Navigate to the plugin directory:
   ```bash
   cd /path/to/poetry_django_plugin
   ```

2. Install the plugin in development mode:
   ```bash
   poetry install
   ```

3. Build the plugin:
   ```bash
   poetry build
   ```

4. Install the plugin:
   ```bash
   pip install dist/*.whl
   ```

## Patching manage.py

After installing the plugin, you can patch your Django project's manage.py file:

```bash
poetry run python -m poetry_django_plugin.command patch-manage /path/to/manage.py
```

Or, if you're in the same directory as manage.py:

```bash
poetry run python -m poetry_django_plugin.command patch-manage
```

## Usage

Once the plugin is installed and manage.py is patched, you can run Django commands as usual:

```bash
./manage.py runserver
```

The plugin will automatically activate the Poetry environment before running the command.
