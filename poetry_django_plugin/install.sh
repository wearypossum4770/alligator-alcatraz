#!/bin/bash
# Installation script for the Poetry Django Plugin

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Please install Poetry first."
    echo "See https://python-poetry.org/docs/#installation for installation instructions."
    exit 1
fi

# Install the plugin
echo "Installing the Poetry Django Plugin..."
poetry install
poetry build
pip install dist/*.whl

# Patch manage.py
echo "Would you like to patch your Django project's manage.py file? (y/n)"
read -r choice
if [[ $choice =~ ^[Yy]$ ]]; then
    echo "Enter the path to your manage.py file (or press Enter to use the default):"
    read -r path
    if [ -z "$path" ]; then
        path="../manage.py"
    fi
    
    poetry run python -m poetry_django_plugin.command patch-manage "$path"
    if [ $? -eq 0 ]; then
        echo "Successfully patched manage.py!"
    else
        echo "Failed to patch manage.py."
    fi
else
    echo "Skipping manage.py patching."
fi

echo "Installation complete!"
