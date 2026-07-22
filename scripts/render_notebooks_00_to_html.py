#!/usr/bin/env python3
"""
render_notebooks_00_to_html.py — Renders both Notebook 00s to HTML inside web/rendered_notebooks/
"""
import os
import sys
import nbformat

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(errors='replace')

from render_nb_17_to_html import convert_nb_to_html

if __name__ == "__main__":
    convert_nb_to_html("00_interactive_data_playground_local_and_processed.ipynb", "00_interactive_data_playground_local_and_processed.html")
    convert_nb_to_html("00_master_capstone_oted_66_domains.ipynb", "00_master_capstone_oted_66_domains.html")
