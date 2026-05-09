import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'FRC Program Docs'
copyright = '2026'
author = 'boring89'
release = '0.1'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# 支援 Markdown
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
