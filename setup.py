#!/usr/bin/env python

from setuptools import setup
from os import path

setup(
    name="django-tailwind",
    description="""Tailwind CSS Framework for Django projects""",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    author="Tim Kamanin",
    author_email="tim@timonweb.com",
    url="https://github.com/timonweb/django-tailwind",
    packages=["tailwind"],
    include_package_data=True,
    use_scm_version={
        "write_to": "tailwind/version.py",
        "version_scheme": "guess-next-dev",
        "local_scheme": "node-and-date",
    },
    setup_requires=["setuptools_scm"],
    install_requires=[],
    license="The MIT License (MIT)",
    zip_safe=False,
    keywords="django-tailwind",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
)
