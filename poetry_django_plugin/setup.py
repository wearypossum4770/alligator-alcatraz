#!/usr/bin/env python
"""Setup script for the Poetry Django Plugin."""
from setuptools import setup

setup(
    name="poetry-django-plugin",
    version="0.1.0",
    description="A Poetry plugin that automatically activates the Poetry environment when Django's manage.py is invoked",
    author="Your Name",
    author_email="you@example.com",
    packages=["poetry_django_plugin"],
    package_data={
        "poetry_django_plugin": ["manage_template.py"],
    },
    entry_points={
        "poetry.plugin": ["django = poetry_django_plugin.plugin:DjangoPlugin"],
    },
    install_requires=[
        "poetry>=1.7.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
