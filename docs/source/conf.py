# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

from datetime import date

import clash_royale

project = "clash-royale-python"
copyright = f"{date.today().year}, Guillaume Coussot"
author = "Guillaume Coussot"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = clash_royale.__version__
# The full version, including alpha/beta/rc tags.
release = clash_royale.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

myst_enable_extensions = [
    "colon_fence",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]

# Furo theme options
html_theme_options = {
    "navigation_with_keys": True,
    "sidebar_hide_name": False,
}

extlinks = {
    "clash-royale-api": (
        "https://developer.clashroyale.com/api-docs/index.html#/%s",
        "%s API docs",
    )
}

# Autodoc options
autodoc_member_order = "bysource"
autodoc_typehints = "signature"
autodoc_class_signature = "separated"
