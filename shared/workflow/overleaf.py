"""
Overleaf integration via MCP service.
"""

import requests
from typing import Dict, List, Optional
from pathlib import Path


class OverleafClient:
    """Client for Overleaf MCP service."""

    def __init__(self, mcp_url: str = "http://localhost:7105"):
        self.mcp_url = mcp_url.rstrip('/')

    def _call_tool(self, tool_name: str, params: Dict) -> Dict:
        """Call MCP tool via HTTP."""
        url = f"{self.mcp_url}/run/{tool_name}"
        response = requests.post(url, json=params, timeout=60)
        response.raise_for_status()
        return response.json()

    def list_projects(self) -> List[Dict]:
        """List all configured Overleaf projects."""
        result = self._call_tool("list_projects", {})
        return result.get('projects', [])

    def list_files(self, project_name: str = "default", extension: str = ".tex") -> List[str]:
        """List files in Overleaf project."""
        result = self._call_tool("list_files", {
            "project_name": project_name,
            "extension": extension
        })
        return result.get('files', [])

    def read_file(self, file_path: str, project_name: str = "default") -> str:
        """Read file from Overleaf project."""
        result = self._call_tool("read_file", {
            "file_path": file_path,
            "project_name": project_name
        })
        return result.get('content', '')

    def get_status(self, project_name: str = "default") -> Dict:
        """Get project status summary."""
        return self._call_tool("status_summary", {
            "project_name": project_name
        })


def sync_to_overleaf(
    latex_dir: str,
    project_name: str = "default",
    commit_message: Optional[str] = None,
    mcp_url: str = "http://localhost:7105"
) -> Dict:
    """
    Sync local LaTeX files to Overleaf project.

    Note: This function prepares files for manual Overleaf upload or Git push.
    Direct file upload via Overleaf API requires authentication beyond Git token.

    Args:
        latex_dir: Local directory with LaTeX files
        project_name: Overleaf project identifier
        commit_message: Git commit message
        mcp_url: Overleaf MCP service URL

    Returns:
        dict: Sync status and instructions
    """
    latex_path = Path(latex_dir)
    if not latex_path.exists():
        return {'success': False, 'error': 'Directory not found'}

    # Get Overleaf project info
    client = OverleafClient(mcp_url)
    try:
        projects = client.list_projects()
        project = next((p for p in projects if p['key'] == project_name), None)

        if not project:
            return {'success': False, 'error': f'Project {project_name} not found'}

        # Get current files
        current_files = client.list_files(project_name, extension='')

        # Find LaTeX files to sync
        tex_files = list(latex_path.glob('*.tex'))
        bib_files = list(latex_path.glob('*.bib'))
        fig_files = list(latex_path.glob('*.pdf')) + list(latex_path.glob('*.png'))

        all_files = tex_files + bib_files + fig_files

        return {
            'success': True,
            'project': project,
            'files_to_sync': [str(f.name) for f in all_files],
            'message': 'Files ready for sync',
            'instructions': f"""
To sync these files to Overleaf:

Method 1: Git Push (Recommended)
1. Clone Overleaf project:
   git clone https://git:TOKEN@git.overleaf.com/{project['projectId']}

2. Copy files:
   cp {latex_dir}/* overleaf-project/

3. Commit and push:
   cd overleaf-project
   git add .
   git commit -m "{commit_message or 'Update from Jupyter workflow'}"
   git push

Method 2: Manual Upload
1. Go to https://www.overleaf.com/project/{project['projectId']}
2. Click "Upload" and select files from {latex_dir}
3. Overleaf will compile automatically
"""
        }

    except Exception as e:
        return {'success': False, 'error': str(e)}


def pull_from_overleaf(
    project_name: str = "default",
    output_dir: str = ".",
    files: Optional[List[str]] = None,
    mcp_url: str = "http://localhost:7105"
) -> Dict:
    """
    Pull files from Overleaf project to local directory.

    Args:
        project_name: Overleaf project identifier
        output_dir: Local output directory
        files: Specific files to pull (None = all .tex files)
        mcp_url: Overleaf MCP service URL

    Returns:
        dict: Pull results
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    client = OverleafClient(mcp_url)

    try:
        # Get files list if not specified
        if files is None:
            files = client.list_files(project_name, extension='.tex')
            # Also get .bib files
            files += client.list_files(project_name, extension='.bib')

        pulled_files = []
        for file_path in files:
            try:
                content = client.read_file(file_path, project_name)

                output_file = output_path / file_path
                output_file.parent.mkdir(parents=True, exist_ok=True)

                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                pulled_files.append(str(output_file))

            except Exception as e:
                print(f"Warning: Could not pull {file_path}: {e}")

        return {
            'success': True,
            'output_dir': str(output_path),
            'files_pulled': pulled_files,
            'count': len(pulled_files)
        }

    except Exception as e:
        return {'success': False, 'error': str(e)}


def list_overleaf_projects(mcp_url: str = "http://localhost:7105") -> List[Dict]:
    """
    List all configured Overleaf projects.

    Args:
        mcp_url: Overleaf MCP service URL

    Returns:
        list: Project information dictionaries
    """
    client = OverleafClient(mcp_url)
    return client.list_projects()


def get_overleaf_status(
    project_name: str = "default",
    mcp_url: str = "http://localhost:7105"
) -> Dict:
    """
    Get Overleaf project status.

    Args:
        project_name: Project identifier
        mcp_url: Overleaf MCP service URL

    Returns:
        dict: Project status information
    """
    client = OverleafClient(mcp_url)
    return client.get_status(project_name)
