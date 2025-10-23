"""
LaTeX templates for academic papers.
"""

from typing import Dict, List


class Template:
    """LaTeX document template."""

    def __init__(
        self,
        name: str,
        documentclass: str = "article",
        documentclass_options: List[str] = None,
        packages: List[str] = None,
        preamble: str = "",
        layout: str = "onecolumn"
    ):
        self.name = name
        self.documentclass = documentclass
        self.documentclass_options = documentclass_options or []
        self.packages = packages or []
        self.preamble = preamble
        self.layout = layout

    def format_document(
        self,
        title: str,
        authors: str,
        abstract: str,
        body: str,
        keywords: List[str] = None
    ) -> str:
        """Format complete LaTeX document."""

        options = ','.join(self.documentclass_options) if self.documentclass_options else ''
        doc = []

        # Document class
        if options:
            doc.append(f"\\documentclass[{options}]{{{self.documentclass}}}")
        else:
            doc.append(f"\\documentclass{{{self.documentclass}}}")

        # Packages
        for package in self.packages:
            doc.append(f"\\usepackage{{{package}}}")

        # Preamble
        if self.preamble:
            doc.append(self.preamble)

        # Begin document
        doc.append("\\begin{document}")

        # Title
        doc.append(f"\\title{{{title}}}")
        doc.append(f"\\author{{{authors}}}")
        doc.append("\\date{\\today}")
        doc.append("\\maketitle")

        # Abstract
        if abstract:
            doc.append("\\begin{abstract}")
            doc.append(abstract)
            doc.append("\\end{abstract}")

        # Keywords
        if keywords:
            kw_str = ', '.join(keywords)
            doc.append(f"\\textbf{{Keywords:}} {kw_str}")
            doc.append("")

        # Body
        doc.append(body)

        # End document
        doc.append("\\end{document}")

        return '\n'.join(doc)


# Predefined templates

ARTICLE_TEMPLATE = Template(
    name="article",
    documentclass="article",
    documentclass_options=["11pt", "a4paper"],
    packages=[
        "amsmath",
        "amssymb",
        "graphicx",
        "hyperref",
        "cite",
        "geometry"
    ],
    preamble=r"\geometry{margin=1in}",
    layout="onecolumn"
)

TWOCOLUMN_TEMPLATE = Template(
    name="twocolumn",
    documentclass="article",
    documentclass_options=["10pt", "twocolumn", "a4paper"],
    packages=[
        "amsmath",
        "amssymb",
        "graphicx",
        "hyperref",
        "cite",
        "geometry",
        "multicol"
    ],
    preamble=r"\geometry{margin=0.75in}",
    layout="twocolumn"
)

IEEE_TEMPLATE = Template(
    name="ieee",
    documentclass="IEEEtran",
    documentclass_options=["conference"],
    packages=[
        "amsmath",
        "amssymb",
        "graphicx",
        "cite"
    ],
    layout="twocolumn"
)

ACTA_ACUSTICA_TEMPLATE = Template(
    name="acta_acustica",
    documentclass="article",
    documentclass_options=["10pt", "twocolumn", "a4paper"],
    packages=[
        "amsmath",
        "amssymb",
        "graphicx",
        "hyperref",
        "cite",
        "geometry",
        "tikz",
        "siunitx",
        "booktabs"
    ],
    preamble=r"""
\geometry{margin=0.75in}
\usetikzlibrary{positioning,shapes,arrows}

% Equation interpretation environment
\newenvironment{interpretation}{\begin{quote}\small\textbf{Interpretation:}}{\end{quote}}
""",
    layout="twocolumn"
)

THESIS_TEMPLATE = Template(
    name="thesis",
    documentclass="report",
    documentclass_options=["12pt", "a4paper"],
    packages=[
        "amsmath",
        "amssymb",
        "graphicx",
        "hyperref",
        "cite",
        "geometry",
        "tikz",
        "fancyhdr",
        "setspace"
    ],
    preamble=r"""
\geometry{margin=1.25in}
\pagestyle{fancy}
\doublespacing
""",
    layout="onecolumn"
)

# Template registry
TEMPLATES: Dict[str, Template] = {
    "article": ARTICLE_TEMPLATE,
    "twocolumn": TWOCOLUMN_TEMPLATE,
    "ieee": IEEE_TEMPLATE,
    "acta_acustica": ACTA_ACUSTICA_TEMPLATE,
    "thesis": THESIS_TEMPLATE
}


def load_template(name: str) -> Template:
    """
    Load template by name.

    Args:
        name: Template name

    Returns:
        Template object

    Raises:
        ValueError: If template not found
    """
    if name not in TEMPLATES:
        raise ValueError(
            f"Template '{name}' not found. "
            f"Available templates: {list(TEMPLATES.keys())}"
        )

    return TEMPLATES[name]


def list_templates() -> List[str]:
    """List available template names."""
    return list(TEMPLATES.keys())
