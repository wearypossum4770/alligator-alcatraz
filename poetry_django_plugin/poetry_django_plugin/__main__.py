"""Main entry point for the Poetry Django Plugin."""

import sys

from poetry_django_plugin.command import PatchManageCommand


def main():
    """Run the patch-manage command."""
    command = PatchManageCommand()
    sys.exit(command.run(sys.argv[1:]))


if __name__ == "__main__":
    main()
