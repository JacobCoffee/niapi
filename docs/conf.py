import importlib.metadata
import os

project = "niapi"
copyright = "2023, Jacob Coffee"
author = "Jacob Coffee"
release = os.getenv("_NIAPI_DOCS_BUILD_VERSION", importlib.metadata.version("litestar").rsplit(".")[0])

extensions = [
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_design",
    "auto_pytabs.sphinx_ext",
    "tools.sphinx_ext",
    "sphinx_copybutton",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "anyio": ("https://anyio.readthedocs.io/en/stable/", None),
    "click": ("https://click.palletsprojects.com/en/8.1.x/", None),
    "structlog": ("https://www.structlog.org/en/stable/", None),
    "opentelemetry": ("https://opentelemetry-python.readthedocs.io/en/latest/", None),
    "litestar": ("https://docs.litestar.dev/2", None),
}

napoleon_google_docstring = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_attr_annotations = True

autoclass_content = "class"
autodoc_class_signature = "separated"
autodoc_default_options = {"special-members": "__init__", "show-inheritance": True, "members": True}
autodoc_member_order = "bysource"
autodoc_typehints_format = "short"

nitpicky = True
autosectionlabel_prefix_document = True
suppress_warnings = [
    "autosectionlabel.*",
    "ref.python",  # TODO: remove when https://github.com/sphinx-doc/sphinx/issues/4961 is fixed
]

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = ["style.css"]
html_show_sourcelink = False
html_title = "Network Information API"

html_theme_options = (
    {
        "use_page_nav": False,
        "github_repo_name": "niapi",
        "logo": {
            "link": "https://github.com/JacobCoffee/niapi",
        },
    },
)
