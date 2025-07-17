"""Command to patch Django's manage.py file."""

import os
import re
import sys
from pathlib import Path
from typing import List

from cleo.commands.command import Command
from cleo.helpers import argument, option
from poetry.console.application import Application


class PatchManageCommand(Command):
    """
    Patch Django's manage.py file to automatically activate the Poetry environment.

    patch-manage
        {path? : Path to the manage.py file}
        {--p|project=? : Django project name}
    """

    help = "Patch Django's manage.py file to automatically activate the Poetry environment."

    def handle(self) -> int:
        """Handle the command."""
        path = self.argument("path")
        project = self.option("project")

        if not path:
            # Try to find manage.py in the current directory
            if os.path.exists("manage.py"):
                path = "manage.py"
            else:
                self.line_error("Could not find manage.py file.")
                return 1

        path = Path(path)
        if not path.exists():
            self.line_error(f"File {path} does not exist.")
            return 1

        # Read the manage.py file
        with open(path, "r") as f:
            content = f.read()

        # Extract the project name if not provided
        if not project:
            match = re.search(
                r'os\.environ\.setdefault\("DJANGO_SETTINGS_MODULE", "([^"]+)\.settings"\)', content
            )
            if match:
                project = match.group(1)
            else:
                self.line_error(
                    "Could not determine the Django project name. Please provide it with --project option."
                )
                return 1

        # Read the template
        template_path = Path(__file__).parent / "manage_template.py"
        with open(template_path, "r") as f:
            template = f.read()

        # Replace the project name
        template = template.replace("{{ project_name }}", project)

        # Backup the original file
        backup_path = path.with_suffix(".py.bak")
        if not backup_path.exists():
            with open(backup_path, "w") as f:
                f.write(content)
            self.line(f"Backup created at {backup_path}")

        # Write the patched file
        with open(path, "w") as f:
            f.write(template)

        self.line(f"Successfully patched {path}")
        return 0


def register_command(application: Application) -> None:
    """Register the command with the application."""
    application.add(PatchManageCommand())
