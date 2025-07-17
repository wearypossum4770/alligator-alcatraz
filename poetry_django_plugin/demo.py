#!/usr/bin/env python
"""Demo script for the Poetry Django Plugin."""
import os
import sys
from pathlib import Path

# Add the plugin directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from poetry_django_plugin.command import PatchManageCommand


def main():
    """Run the demo."""
    print("Poetry Django Plugin Demo")
    print("========================")
    print()
    print("This script demonstrates how to use the Poetry Django Plugin.")
    print()
    print("1. First, install the plugin:")
    print("   pip install -e .")
    print()
    print("2. Then, patch your Django project's manage.py file:")
    print("   python -m poetry_django_plugin.command patch-manage /path/to/manage.py")
    print()
    print("3. Now, you can run Django commands as usual:")
    print("   ./manage.py runserver")
    print()
    print(
        "The plugin will automatically activate the Poetry environment before running the command."
    )
    print()
    print("Would you like to patch your manage.py file now? (y/n)")
    choice = input().lower()
    if choice == "y":
        print("Enter the path to your manage.py file (or press Enter to use the default):")
        path = input()
        if not path:
            path = "../manage.py"

        command = PatchManageCommand()
        exit_code = command.run([path])
        if exit_code == 0:
            print("Successfully patched manage.py!")
        else:
            print("Failed to patch manage.py.")
    else:
        print("Exiting...")


if __name__ == "__main__":
    main()
