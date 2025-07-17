"""Patch for Django's manage.py script."""

import os
import sys
from pathlib import Path

from poetry.console.application import Application
from poetry.console.commands.env_command import EnvCommand


def ensure_poetry_env():
    """Ensure that the Poetry environment is activated."""
    try:
        # Create a dummy EnvCommand to access Poetry's environment
        command = EnvCommand()
        command._poetry = Application().poetry

        # Get the virtual environment
        env = command.env

        if env:
            # Get the virtual environment path
            env_path = env.path

            # Check if we're already in the Poetry environment
            if os.environ.get("VIRTUAL_ENV") == str(env_path):
                return

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

                print(f"Poetry environment activated: {env_path}")
    except Exception as e:
        print(f"Failed to activate Poetry environment: {e}", file=sys.stderr)
