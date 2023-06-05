# Copyright 2023, QC Design GmbH and the plaquette-ibm contributors
# SPDX-License-Identifier: Apache-2.0
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).absolute().parent.parent / "src"))


# -- Project information -----------------------------------------------------

project = "plaquette-ibm-backend"
copyright = "2022, QC Design GmbH"
author = "QC Design GmbH"
url = "https://docs.plaquette.design/projects/ibm-backend"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
]

intersphinx_mapping = {
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

autodoc_member_order = "groupwise"
show_authors = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/qc-design/plaquette-ibm-backend/",
    "source_branch": "main",
    "source_directory": "docs/",
    "light_logo": "logo_light.png",  # relative to html_static_path
    "dark_logo": "logo_dark.png",
}
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

html_static_path = ["_static"]
html_css_files = ["css/custom.css"]

html_show_sourcelink = True
todo_include_todos = True
