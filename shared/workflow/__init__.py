"""
Jupyter to Overleaf Workflow
A tool for converting Jupyter notebooks to academic LaTeX papers with Overleaf integration.

This work was developed with assistance from Claude (Anthropic).
"""

__version__ = "1.0.0"

from .converter import notebook_to_paper, extract_figures, extract_equations
from .overleaf import sync_to_overleaf, pull_from_overleaf, list_overleaf_projects
from .github import push_to_github, create_github_repo
from .templates import Template, load_template
from .latex import compile_latex, check_latex_installation

__all__ = [
    "notebook_to_paper",
    "extract_figures",
    "extract_equations",
    "sync_to_overleaf",
    "pull_from_overleaf",
    "list_overleaf_projects",
    "push_to_github",
    "create_github_repo",
    "Template",
    "load_template",
    "compile_latex",
    "check_latex_installation",
]
