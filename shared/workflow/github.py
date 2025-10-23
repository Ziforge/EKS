"""
GitHub integration utilities.
"""

import subprocess
from pathlib import Path
from typing import Dict, Optional


def push_to_github(
    local_dir: str,
    repo_name: str,
    commit_message: str,
    branch: str = "main"
) -> Dict:
    """
    Push local directory to GitHub repository.

    Args:
        local_dir: Local directory path
        repo_name: GitHub repository (username/repo)
        commit_message: Commit message
        branch: Branch name (default: main)

    Returns:
        dict: Push results
    """
    try:
        dir_path = Path(local_dir)

        # Check if git repo exists
        if not (dir_path / '.git').exists():
            # Initialize git repo
            subprocess.run(['git', 'init'], cwd=dir_path, check=True)
            subprocess.run(
                ['git', 'remote', 'add', 'origin',
                 f'https://github.com/{repo_name}.git'],
                cwd=dir_path,
                check=True
            )

        # Add files
        subprocess.run(['git', 'add', '.'], cwd=dir_path, check=True)

        # Commit
        subprocess.run(
            ['git', 'commit', '-m', commit_message],
            cwd=dir_path,
            check=True
        )

        # Push
        subprocess.run(
            ['git', 'push', '-u', 'origin', branch],
            cwd=dir_path,
            check=True
        )

        return {
            'success': True,
            'repository': repo_name,
            'branch': branch,
            'message': commit_message
        }

    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'error': str(e)
        }


def create_github_repo(
    name: str,
    description: str = "",
    private: bool = True
) -> Dict:
    """
    Create GitHub repository using GitHub CLI.

    Requires gh CLI installed and authenticated.

    Args:
        name: Repository name
        description: Repository description
        private: Make repository private

    Returns:
        dict: Repository creation results
    """
    try:
        visibility = "--private" if private else "--public"

        cmd = [
            'gh', 'repo', 'create', name,
            visibility,
            '--description', description
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        return {
            'success': True,
            'repository': name,
            'url': f'https://github.com/{name}',
            'output': result.stdout
        }

    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'error': str(e),
            'stderr': e.stderr
        }
    except FileNotFoundError:
        return {
            'success': False,
            'error': 'GitHub CLI (gh) not found. Install: brew install gh'
        }


def create_release(
    repo_name: str,
    version: str,
    notes: str,
    local_dir: Optional[str] = None
) -> Dict:
    """
    Create GitHub release.

    Args:
        repo_name: Repository name (username/repo)
        version: Release version (e.g., v1.0.0)
        notes: Release notes
        local_dir: Local directory (if not in repo)

    Returns:
        dict: Release creation results
    """
    try:
        cmd = [
            'gh', 'release', 'create', version,
            '--title', version,
            '--notes', notes
        ]

        if local_dir:
            result = subprocess.run(
                cmd,
                cwd=local_dir,
                capture_output=True,
                text=True,
                check=True
            )
        else:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

        return {
            'success': True,
            'repository': repo_name,
            'version': version,
            'url': result.stdout.strip()
        }

    except subprocess.CalledProcessError as e:
        return {
            'success': False,
            'error': str(e),
            'stderr': e.stderr
        }
