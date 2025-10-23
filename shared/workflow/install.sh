#!/bin/bash
# Install jupyter-overleaf-workflow in JupyterLab container
# Run this inside the mcp-jupyter container

cd /home/jovyan/shared/workflow
pip install -e .

echo "✅ Jupyter-Overleaf Workflow installed!"
echo ""
echo "Usage in notebooks:"
echo "  from workflow import notebook_to_paper, compile_latex, sync_to_overleaf"
echo ""
