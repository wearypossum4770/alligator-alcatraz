# Poetry Django Plugin

A Poetry plugin that automatically activates the Poetry environment when Django's manage.py is invoked.

## Installation

```bash
poetry add --dev poetry-django-plugin
```

## Usage

Once installed, the plugin will automatically activate the Poetry environment when `./manage.py` is invoked.

## How it works

The plugin patches Django's manage.py script to ensure that the Poetry environment is activated before any Django commands are executed.
