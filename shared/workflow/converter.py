"""
Notebook to LaTeX conversion utilities.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional
import nbformat
from nbconvert import LatexExporter
from .templates import load_template


def notebook_to_paper(
    notebook: str,
    output_dir: str,
    template: str = "article",
    save_figures: bool = True,
    figure_format: str = "pdf",
    include_code: bool = False,
    extract_citations: bool = True,
    **kwargs
) -> Dict:
    """
    Convert Jupyter notebook to academic LaTeX paper.

    Args:
        notebook: Path to .ipynb file
        output_dir: Output directory for LaTeX files
        template: Template name or Template object
        save_figures: Save figures to output directory
        figure_format: Figure format (pdf, png, svg)
        include_code: Include code cells in paper
        extract_citations: Extract citations to BibTeX

    Returns:
        dict: Conversion results with paths and statistics
    """
    # Load notebook
    with open(notebook, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Load template
    if isinstance(template, str):
        template_obj = load_template(template)
    else:
        template_obj = template

    # Extract metadata
    metadata = _extract_metadata(nb)

    # Extract figures if requested
    figures = []
    if save_figures:
        figures = extract_figures(nb, output_dir, format=figure_format)

    # Extract equations
    equations = extract_equations(nb)

    # Extract citations
    citations = []
    if extract_citations:
        citations = _extract_citations(nb)

    # Convert to LaTeX
    latex_exporter = LatexExporter()
    latex_exporter.template_name = 'article'

    if not include_code:
        # Remove code cells
        nb_copy = nb.copy()
        nb_copy.cells = [cell for cell in nb_copy.cells if cell.cell_type != 'code']
        body, resources = latex_exporter.from_notebook_node(nb_copy)
    else:
        body, resources = latex_exporter.from_notebook_node(nb)

    # Apply template
    latex_content = template_obj.format_document(
        title=metadata.get('title', 'Untitled'),
        authors=metadata.get('authors', 'Author'),
        abstract=metadata.get('abstract', ''),
        body=body,
        keywords=metadata.get('keywords', [])
    )

    # Write main.tex
    main_tex = output_path / 'main.tex'
    with open(main_tex, 'w', encoding='utf-8') as f:
        f.write(latex_content)

    # Write references.bib if citations found
    if citations:
        bib_file = output_path / 'references.bib'
        with open(bib_file, 'w', encoding='utf-8') as f:
            for citation in citations:
                f.write(citation + '\n\n')

    return {
        'success': True,
        'output_dir': str(output_path),
        'main_tex': str(main_tex),
        'figures': figures,
        'equations': len(equations),
        'citations': len(citations),
        'metadata': metadata
    }


def extract_figures(notebook, output_dir: str, format: str = 'pdf') -> List[str]:
    """
    Extract figures from notebook outputs.

    Args:
        notebook: Notebook object or path
        output_dir: Directory to save figures
        format: Output format (pdf, png, svg)

    Returns:
        list: Paths to saved figures
    """
    if isinstance(notebook, str):
        with open(notebook, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    else:
        nb = notebook

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    figures = []
    figure_count = 0

    for cell in nb.cells:
        if cell.cell_type == 'code' and hasattr(cell, 'outputs'):
            for output in cell.outputs:
                if hasattr(output, 'data'):
                    # Check for image data
                    if 'image/png' in output.data:
                        figure_count += 1
                        fig_path = output_path / f'figure{figure_count}.png'
                        import base64
                        with open(fig_path, 'wb') as f:
                            f.write(base64.b64decode(output.data['image/png']))
                        figures.append(str(fig_path))

    return figures


def extract_equations(notebook) -> List[Dict]:
    """
    Extract LaTeX equations from markdown cells.

    Args:
        notebook: Notebook object or path

    Returns:
        list: List of equation dictionaries
    """
    if isinstance(notebook, str):
        with open(notebook, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    else:
        nb = notebook

    equations = []

    # Patterns for inline and display math
    display_pattern = r'\$\$(.*?)\$\$'
    inline_pattern = r'\$(.*?)\$'

    for cell_idx, cell in enumerate(nb.cells):
        if cell.cell_type == 'markdown':
            # Find display equations
            for match in re.finditer(display_pattern, cell.source, re.DOTALL):
                equations.append({
                    'type': 'display',
                    'content': match.group(1).strip(),
                    'cell': cell_idx
                })

            # Find inline equations
            for match in re.finditer(inline_pattern, cell.source):
                # Skip if part of display equation
                if not re.search(r'\$\$.*?' + re.escape(match.group(0)) + r'.*?\$\$',
                                cell.source, re.DOTALL):
                    equations.append({
                        'type': 'inline',
                        'content': match.group(1).strip(),
                        'cell': cell_idx
                    })

    return equations


def _extract_metadata(nb) -> Dict:
    """Extract metadata from notebook first cell."""
    metadata = {
        'title': 'Untitled',
        'authors': '',
        'institution': '',
        'abstract': '',
        'keywords': []
    }

    if len(nb.cells) > 0:
        first_cell = nb.cells[0]
        if first_cell.cell_type == 'markdown':
            source = first_cell.source

            # Extract title
            title_match = re.search(r'#\s+(?:Paper Title:)?\s*(.+)', source)
            if title_match:
                metadata['title'] = title_match.group(1).strip()

            # Extract authors
            authors_match = re.search(r'\*\*Authors?:\*\*\s*(.+)', source)
            if authors_match:
                metadata['authors'] = authors_match.group(1).strip()

            # Extract institution
            inst_match = re.search(r'\*\*Institution:\*\*\s*(.+)', source)
            if inst_match:
                metadata['institution'] = inst_match.group(1).strip()

            # Extract keywords
            kw_match = re.search(r'\*\*Keywords:\*\*\s*(.+)', source)
            if kw_match:
                keywords = kw_match.group(1).strip()
                metadata['keywords'] = [k.strip() for k in keywords.split(',')]

    # Extract abstract from second cell
    if len(nb.cells) > 1:
        second_cell = nb.cells[1]
        if second_cell.cell_type == 'markdown':
            abstract_match = re.search(r'ABSTRACT:\s*(.+)', second_cell.source, re.DOTALL)
            if abstract_match:
                metadata['abstract'] = abstract_match.group(1).strip()

    return metadata


def _extract_citations(nb) -> List[str]:
    """Extract citations from markdown cells."""
    citations = []
    citation_pattern = r'\[(\d+)\]'

    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            # Look for references section
            if 'References' in cell.source or 'REFERENCES' in cell.source:
                # Extract individual citations
                lines = cell.source.split('\n')
                for line in lines:
                    if re.match(r'\[\d+\]', line):
                        citations.append(line.strip())

    return citations
