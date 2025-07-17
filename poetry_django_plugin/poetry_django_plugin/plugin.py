"""Poetry Django Plugin implementation."""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union

from poetry.console.application import Application
from poetry.console.commands.env_command import EnvCommand
from poetry.plugins.application_plugin import ApplicationPlugin

from poetry_django_plugin.command import register_command


class DjangoPlugin(ApplicationPlugin):
    """Poetry plugin that automatically activates the Poetry environment when Django's manage.py is invoked."""

    def activate(self, application: Application) -> None:
        """Activate the plugin."""
        # Register our command
        register_command(application)

        # Check if we're running manage.py
        if len(sys.argv) > 0 and Path(sys.argv[0]).name == "manage.py":
            self._activate_poetry_env()

    def _activate_poetry_env(self) -> None:
        """Activate the Poetry environment."""
        # Create a dummy EnvCommand to access Poetry's environment
        command = EnvCommand()
        command._poetry = Application().poetry

        # Get the virtual environment
        env = command.env

        if env:
            # Get the virtual environment path
            env_path = env.path

            # Activate the virtual environment
            bin_dir = "Scripts" if sys.platform == "win32" else "bin"
            activate_script = os.path.join(env_path, bin_dir, "activate_this.py")

            if os.path.exists(activate_script):
                with open(activate_script) as f:
                    exec(f.read(), {"__file__": activate_script})

                # Update PATH environment variable
                os.environ["PATH"] = (
                    os.path.join(env_path, bin_dir) + os.pathsep + os.environ["PATH"]
                )

                # Update PYTHONPATH environment variable
                site_packages = os.path.join(
                    env_path,
                    "lib",
                    f"python{sys.version_info.major}.{sys.version_info.minor}",
                    "site-packages",
                )
                if os.path.exists(site_packages):
                    sys.path.insert(0, site_packages)

                # Set VIRTUAL_ENV environment variable
                os.environ["VIRTUAL_ENV"] = str(env_path)

                # Remove PYTHONHOME if it exists
                if "PYTHONHOME" in os.environ:
                    del os.environ["PYTHONHOME"]
