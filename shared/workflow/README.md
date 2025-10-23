# Jupyter-Overleaf Workflow

This package is pre-installed in the MCP Pipeline JupyterLab environment.

## Quick Start

In any Jupyter notebook:

```python
from workflow import notebook_to_paper, compile_latex, sync_to_overleaf

# Convert notebook to LaTeX
result = notebook_to_paper(
    notebook="my_research.ipynb",
    output_dir="shared/docs/my_paper",
    template="twocolumn"
)

# Compile to PDF using docs-mcp
pdf = compile_latex(result['main_tex'], use_mcp=True)

# Sync to Overleaf (requires configuration)
sync_to_overleaf(
    latex_dir="shared/docs/my_paper",
    project_name="default"
)
```

## Features

- **Notebook to LaTeX** - Automatic conversion with academic templates
- **LaTeX Compilation** - Via docs-mcp service (port 7070)
- **Overleaf Integration** - Via overleaf-mcp service (port 7105)
- **GitHub Automation** - Push papers to GitHub
- **Templates** - article, twocolumn, ieee, thesis, acta_acustica

## Templates

```python
from workflow import load_template, list_templates

# List available templates
print(list_templates())

# Use a template
notebook_to_paper("research.ipynb", "output", template="ieee")
```

## Full Documentation

See the main repository: https://github.com/Ziforge/jupyter-overleaf-workflow

## License

CC BY-NC-SA 4.0 - Free for educational use

---

This work was developed with assistance from Claude (Anthropic).
