import sphinx_rtd_theme
import os
import sys

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# -- Project information -----------------------------------------------------

project = 'bnp'
copyright = '2020, mocobt'
author = 'mocobt'

# The full version, including alpha/beta/rc tags
release = '0.1'
master_doc = 'index'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = []
html_static_path = ['_static']
