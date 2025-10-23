"""
LaTeX compilation utilities with docs-mcp integration.
"""

import subprocess
import requests
from pathlib import Path
from typing import Dict, Optional


class LaTeXCompiler:
    """LaTeX compiler with local and MCP options."""

    def __init__(self, docs_mcp_url: str = "http://localhost:7070"):
        self.docs_mcp_url = docs_mcp_url.rstrip('/')

    def compile_local(self, tex_file: str, runs: int = 3) -> Dict:
        """
        Compile LaTeX locally using pdflatex.

        Args:
            tex_file: Path to .tex file
            runs: Number of pdflatex runs (default: 3 for proper refs)

        Returns:
            dict: Compilation results
        """
        tex_path = Path(tex_file)
        if not tex_path.exists():
            return {'success': False, 'error': 'TeX file not found'}

        tex_dir = tex_path.parent
        tex_name = tex_path.name
        base_name = tex_path.stem

        results = []

        try:
            # First run: pdflatex
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', tex_name],
                cwd=tex_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            results.append({
                'command': 'pdflatex (1st run)',
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            })

            # Run bibtex if .bib exists
            bib_file = tex_dir / f"{base_name}.bib"
            if bib_file.exists():
                result = subprocess.run(
                    ['bibtex', base_name],
                    cwd=tex_dir,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                results.append({
                    'command': 'bibtex',
                    'returncode': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                })

            # Additional pdflatex runs
            for i in range(2, runs + 1):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', tex_name],
                    cwd=tex_dir,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                results.append({
                    'command': f'pdflatex ({i}{"nd" if i==2 else "rd"} run)',
                    'returncode': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                })

            # Check if PDF was created
            pdf_file = tex_dir / f"{base_name}.pdf"
            success = pdf_file.exists()

            return {
                'success': success,
                'pdf_path': str(pdf_file) if success else None,
                'steps': results
            }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'LaTeX compilation timeout',
                'steps': results
            }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'pdflatex not found. Install LaTeX (TeX Live, MiKTeX, or MacTeX)',
                'steps': results
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'steps': results
            }

    def compile_via_mcp(self, tex_dir: str, main_tex: str = "main.tex") -> Dict:
        """
        Compile LaTeX using docs-mcp service.

        Args:
            tex_dir: Directory containing LaTeX files
            main_tex: Main .tex file name

        Returns:
            dict: Compilation results from MCP service
        """
        try:
            url = f"{self.docs_mcp_url}/run/latex_build"
            payload = {
                "tex_dir": tex_dir,
                "main_tex": main_tex
            }

            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'Cannot connect to docs-mcp service. Is it running?'
            }
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'LaTeX compilation timeout (MCP)'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'MCP compilation failed: {str(e)}'
            }


def compile_latex(
    tex_file: str,
    use_mcp: bool = False,
    mcp_url: str = "http://localhost:7070"
) -> Dict:
    """
    Compile LaTeX document.

    Args:
        tex_file: Path to .tex file
        use_mcp: Use docs-mcp service instead of local compilation
        mcp_url: docs-mcp service URL

    Returns:
        dict: Compilation results
    """
    compiler = LaTeXCompiler(mcp_url)

    if use_mcp:
        tex_path = Path(tex_file)
        tex_dir = str(tex_path.parent.resolve())
        tex_name = tex_path.name
        return compiler.compile_via_mcp(tex_dir, tex_name)
    else:
        return compiler.compile_local(tex_file)


def check_latex_installation() -> Dict:
    """
    Check if LaTeX is installed locally.

    Returns:
        dict: Installation status and version info
    """
    try:
        result = subprocess.run(
            ['pdflatex', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            return {
                'installed': True,
                'version': version_line
            }
        else:
            return {
                'installed': False,
                'error': 'pdflatex returned error'
            }

    except FileNotFoundError:
        return {
            'installed': False,
            'error': 'pdflatex not found',
            'install_instructions': {
                'macOS': 'brew install --cask mactex',
                'Ubuntu/Debian': 'sudo apt-get install texlive-full',
                'Windows': 'Download MiKTeX from https://miktex.org/'
            }
        }
    except Exception as e:
        return {
            'installed': False,
            'error': str(e)
        }
