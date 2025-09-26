import os
import sys


sys.path.insert(0, os.path.abspath('../'))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')

import django
django.setup()
project = 'news_project'
copyright = '2025, Jaelyn'
author = 'Jaelyn'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
