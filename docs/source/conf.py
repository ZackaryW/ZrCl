# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../../src"))

# os.system run subgen.py
os.system("subgen.py")

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ZrCl'
copyright = '2024, ZackaryW'
author = 'ZackaryW'
release = '0.3.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
autodoc_mock_imports = [
    "screeninfo",
    "pygetwindow",
    "pyautogui",
    "pyscreeze",
    "pywin32",
    "PIL",
    "keyring",
    "numpy",
    "easyocr",
    "orjson",
    "pandas",
    "py7zr",
    "marisa_trie",
    "requests",
    "thefuzz",
    "readchar"
]

extensions = [
    'sphinx.ext.napoleon',
    "sphinx.ext.todo",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
]
templates_path = ['_templates']
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autodoc_default_options = {
    "member-order": "bysource",
}
add_module_names = False


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

def setup(app):
    app.add_css_file('custom.css')