"""Sphinx configuration."""
from __future__ import annotations

import importlib.metadata
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from niapi.metadata import __project__ as project

# -- Environmental Data ------------------------------------------------------
path = Path("..").resolve()
tls_verify = False
sys.path.insert(0, path.as_posix())
load_dotenv()

# -- Project information -----------------------------------------------------
project = project
copyright = "2023, Jacob Coffee"
author = "Jacob Coffee"
release = os.getenv("_NIAPI_DOCS_BUILD_VERSION", importlib.metadata.version("litestar").rsplit(".")[0])

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinxcontrib.mermaid",
    "sphinx_copybutton",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_click",
    "sphinx_toolbox.collapse",
    # "sphinx_design",  # not available in 7.0
    "sphinxcontrib.autodoc_pydantic",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "anyio": ("https://anyio.readthedocs.io/en/stable/", None),
    "click": ("https://click.palletsprojects.com/en/8.1.x/", None),
    "structlog": ("https://www.structlog.org/en/stable/", None),
    "opentelemetry": ("https://opentelemetry-python.readthedocs.io/en/latest/", None),
    "litestar": ("https://docs.litestar.dev/2/", None),
    "msgspec": ("https://jcristharif.com/msgspec/", None),
}

napoleon_google_docstring = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_attr_annotations = True

autoclass_content = "both"
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "exclude-members": "__weakref__",
    "show-inheritance": True,
    "class-signature": "separated",
    "typehints-format": "short",
}

nitpicky = False
nitpick_ignore = []
nitpick_ignore_regex = []

with Path("nitpick-exceptions").open() as file:
    for line in file:
        if line.strip() == "" or line.startswith("#"):
            continue
        dtype, target = line.split(None, 1)
        target = target.strip()
        nitpick_ignore.append((dtype, target))

with Path("nitpick-exceptions-regex").open() as file:
    for line in file:
        if line.strip() == "" or line.startswith("#"):
            continue
        dtype, target = line.split(None, 1)
        target = target.strip()
        nitpick_ignore_regex.append((dtype, target))

autosectionlabel_prefix_document = True
suppress_warnings = [
    "autosectionlabel.*",
    "ref.python",  # TODO: remove when https://github.com/sphinx-doc/sphinx/issues/4961 is fixed
]

# -- Style configuration -----------------------------------------------------
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_show_sourcelink = True
html_title = "Docs"
html_favicon = "_static/badge.svg"
html_logo = "_static/badge.svg"

html_theme_options = {
    "show_toc_level": 2,
    "logo": {
        "link": "https://github.com/JacobCoffee/niapi",
    },
    "navbar_align": "left",
    "icon_links": [
        {
            "name": "Github",
            "url": "https://github.com/JacobCoffee/niapi",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
    ],
    "external_links": [
        {"name": "Dashboard", "url": os.getenv("NIAPI_URL")},
    ],
    "announcement": "This documentation is currently under development.",
    "navbar_end": ["navbar-icon-links"],
    "navbar_persistent": ["search-button", "theme-switcher"],
}
