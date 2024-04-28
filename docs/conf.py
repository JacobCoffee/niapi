"""Sphinx configuration."""

from __future__ import annotations

import importlib.metadata
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from app.metadata import __project__

# -- Environmental Data ------------------------------------------------------
path = Path("..").resolve()
tls_verify = False
sys.path.insert(0, path.as_posix())
load_dotenv()

# -- Project information -----------------------------------------------------
current_year = datetime.now().year
project = __project__
copyright = f"{current_year}, Jacob Coffee"
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
    # "sphinxcontrib.autodoc_pydantic",  # needs pydantic v2 support
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

nitpicky = False  # This is too much of a headache right now
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
html_theme = "shibuya"
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]
html_show_sourcelink = True
html_title = "Docs"
html_favicon = "_static/badge.svg"
html_logo = "_static/badge.svg"
html_context = {
    "source_type": "github",
    "source_user": "JacobCoffee",
    "source_repo": "niapi",
}

brand_colors = {
    "--brand-main": "133, 199, 242",
    "--brand-secondary": "99, 99, 99",
    "--brand-alert": "241, 81, 82",
}

html_theme_options = {
    "logo_target": "/",
    "announcement": "This documentation is currently under development.",
    "github_url": "https://github.com/JacobCoffee/niapi",
    "discord_url": "https://discord.gg/ZVG8hN6RrJ/",
    "twitter_url": "https://twitter.com/_scriptr",
    "youtube_url": "https://youtube.com/@monorepo",
    "nav_links": [
        {"title": "Dashboard", "url": "https://niapi.app/"},
        {
            "title": "Sponsor me",
            "url": "https://github.com/sponsors/JacobCoffee",
            "icon": "accessibility",
        },
    ],
    # TODO: commented sections appear to not work?
    "light_css_variables": {
        # RGB
        "--sy-rc-theme": brand_colors["--brand-main"],
        "--sy-rc-text": brand_colors["--brand-main"],
        "--sy-rc-invert": brand_colors["--brand-main"],
        # "--sy-rc-bg": brand_colors["--brand-secondary"],
        # Hex
        "--sy-c-link": "#for ",
        # "--sy-c-foot-bg": "#191919",
        "--sy-c-foot-divider": "#85c7f2",
        # "--sy-c-foot-text": "#191919",
        "--sy-c-bold": "#85c7f2",
        "--sy-c-heading": "#85c7f2",
        # "--sy-c-text-weak": "#85c7f2",
        "--sy-c-text": "#101010",
        "--sy-c-bg-weak": "#383838",
    },
    "dark_css_variables": {
        # RGB
        "--sy-rc-theme": brand_colors["--brand-main"],
        "--sy-rc-text": brand_colors["--brand-main"],
        "--sy-rc-invert": brand_colors["--brand-main"],
        "--sy-rc-bg": brand_colors["--brand-secondary"],
        # Hex
        # "--sy-c-link": "#85c7f2",
        "--sy-c-foot-bg": "#191919",
        "--sy-c-foot-divider": "#85c7f2",
        "--sy-c-foot-text": "#fff",
        "--sy-c-bold": "#85c7f2",
        "--sy-c-heading": "#85c7f2",
        "--sy-c-text-weak": "#85c7f2",
        "--sy-c-text": "#fff",
        "--sy-c-bg-weak": "#383838",
    },
}
