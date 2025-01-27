# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "django-tailwind-4"
copyright = "2025, Ryan Sevelj"
author = "Ryan Sevelj"

__version__ = "0.1.4"
# The full version, including alpha/beta/rc tags.
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
extensions = [
    "sphinx.ext.intersphinx",
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_copybutton",
    "sphinx_inline_tabs",
    "sphinx.ext.todo",
    "sphinx.ext.graphviz",
]

exclude_patterns = ["_build", "build", "Thumbs.db", ".DS_Store"]

intersphinx_mapping = {
    "django": (
        "https://docs.djangoproject.com/en/stable",
        "https://docs.djangoproject.com/en/stable/_objects/",
    ),
    "python": ("https://docs.python.org/3", None),
    "Unicode Standard": ("https://www.unicode.org/", None),
}

pygments_style = "default"
pygments_dark_style = "monokai"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
# html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# sphinx-copybutton is a lightweight code-block copy button
# config options are here https://sphinx-copybutton.readthedocs.io/en/latest/
# This config removes Python Repl + continuation, Bash line prefixes,
# ipython and qtconsole + continuation, jupyter-console + continuation and preceding line numbers
copybutton_prompt_text = (
    r"^\d{1,4}|^.\d{1,4}|>>> |\s{2,6}|\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}:"
)

copybutton_prompt_is_regexp = True

# datalad download-url http://www.tldp.org/LDP/Bash-Beginners-Guide/Bash-Beginners-Guide.pdf \
# --dataset . \
# -m "add beginners guide on bash" \
# -O books/bash_guide.pdf
# is correctly pasted with the following setting
copybutton_line_continuation_character = "\\"
