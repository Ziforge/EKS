import os
import json
import subprocess
import tempfile
import shutil
from typing import Optional
from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="OverleafServer", stateless_http=True)

# Load projects configuration
PROJECTS_CONFIG = {}
try:
    with open("/app/projects.json", "r") as f:
        PROJECTS_CONFIG = json.load(f)
except Exception as e:
    print(f"Warning: Could not load projects.json: {e}")

def get_project_config(project_name: Optional[str] = None):
    """Get project configuration from projects.json"""
    if not PROJECTS_CONFIG.get("projects"):
        raise Exception("No projects configured in projects.json")

    if project_name and project_name in PROJECTS_CONFIG["projects"]:
        return PROJECTS_CONFIG["projects"][project_name]

    if "default" in PROJECTS_CONFIG["projects"]:
        return PROJECTS_CONFIG["projects"]["default"]

    raise Exception(f"Project '{project_name or 'default'}' not found in configuration")

def clone_overleaf_repo(project_id: str, git_token: str) -> str:
    """Clone Overleaf project via Git"""
    temp_dir = tempfile.mkdtemp()
    git_url = f"https://git:{git_token}@git.overleaf.com/{project_id}"

    result = subprocess.run(
        ["git", "clone", git_url, temp_dir],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise Exception(f"Failed to clone repository: {result.stderr}")

    return temp_dir

def list_files_in_repo(repo_dir: str, extension: str = ".tex"):
    """List files with given extension in repository"""
    files = []
    for root, dirs, filenames in os.walk(repo_dir):
        # Skip .git directory
        if '.git' in root:
            continue
        for filename in filenames:
            if filename.endswith(extension):
                rel_path = os.path.relpath(os.path.join(root, filename), repo_dir)
                files.append(rel_path)
    return files

def read_file_from_repo(repo_dir: str, file_path: str) -> str:
    """Read file content from repository"""
    full_path = os.path.join(repo_dir, file_path)
    if not os.path.exists(full_path):
        raise Exception(f"File not found: {file_path}")

    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_latex_sections(content: str):
    """Parse LaTeX document for sections"""
    import re
    sections = []

    # Match \section, \subsection, \subsubsection commands
    section_pattern = r'\\(section|subsection|subsubsection)\{([^}]+)\}'
    matches = list(re.finditer(section_pattern, content))

    for i, match in enumerate(matches):
        section_type = match.group(1)
        section_title = match.group(2)
        start_pos = match.end()

        # Find content until next section or end
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)

        section_content = content[start_pos:end_pos].strip()

        sections.append({
            "type": section_type,
            "title": section_title,
            "content": section_content
        })

    return sections

@mcp.tool()
def health():
    """Health check endpoint"""
    return {"ok": True, "service": "overleaf-mcp"}

@mcp.tool()
def list_projects() -> dict:
    """List all configured Overleaf projects"""
    if not PROJECTS_CONFIG.get("projects"):
        return {"projects": [], "message": "No projects configured"}

    projects = []
    for key, config in PROJECTS_CONFIG["projects"].items():
        projects.append({
            "key": key,
            "name": config.get("name", "Unknown"),
            "projectId": config.get("projectId", "")
        })

    return {"projects": projects}

@mcp.tool()
def list_files(project_name: Optional[str] = None, extension: str = ".tex") -> dict:
    """
    List files in an Overleaf project

    Args:
        project_name: Project identifier (default uses 'default' project)
        extension: File extension filter (default: .tex)
    """
    config = get_project_config(project_name)
    repo_dir = None

    try:
        repo_dir = clone_overleaf_repo(config["projectId"], config["gitToken"])
        files = list_files_in_repo(repo_dir, extension)
        return {
            "ok": True,
            "project": config.get("name", "Unknown"),
            "files": files,
            "count": len(files)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        if repo_dir:
            shutil.rmtree(repo_dir, ignore_errors=True)

@mcp.tool()
def read_file(file_path: str, project_name: Optional[str] = None) -> dict:
    """
    Read a file from an Overleaf project

    Args:
        file_path: Path to the file in the project
        project_name: Project identifier (default uses 'default' project)
    """
    config = get_project_config(project_name)
    repo_dir = None

    try:
        repo_dir = clone_overleaf_repo(config["projectId"], config["gitToken"])
        content = read_file_from_repo(repo_dir, file_path)
        return {
            "ok": True,
            "file_path": file_path,
            "content": content,
            "size": len(content)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        if repo_dir:
            shutil.rmtree(repo_dir, ignore_errors=True)

@mcp.tool()
def get_sections(file_path: str, project_name: Optional[str] = None) -> dict:
    """
    Get all sections from a LaTeX file

    Args:
        file_path: Path to the LaTeX file
        project_name: Project identifier (default uses 'default' project)
    """
    config = get_project_config(project_name)
    repo_dir = None

    try:
        repo_dir = clone_overleaf_repo(config["projectId"], config["gitToken"])
        content = read_file_from_repo(repo_dir, file_path)
        sections = parse_latex_sections(content)
        return {
            "ok": True,
            "file_path": file_path,
            "sections": sections,
            "count": len(sections)
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        if repo_dir:
            shutil.rmtree(repo_dir, ignore_errors=True)

@mcp.tool()
def get_section_content(file_path: str, section_title: str, project_name: Optional[str] = None) -> dict:
    """
    Get content of a specific section

    Args:
        file_path: Path to the LaTeX file
        section_title: Title of the section to retrieve
        project_name: Project identifier (default uses 'default' project)
    """
    config = get_project_config(project_name)
    repo_dir = None

    try:
        repo_dir = clone_overleaf_repo(config["projectId"], config["gitToken"])
        content = read_file_from_repo(repo_dir, file_path)
        sections = parse_latex_sections(content)

        # Find matching section
        for section in sections:
            if section["title"] == section_title:
                return {
                    "ok": True,
                    "section": section
                }

        return {"ok": False, "error": f"Section '{section_title}' not found"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        if repo_dir:
            shutil.rmtree(repo_dir, ignore_errors=True)

@mcp.tool()
def status_summary(project_name: Optional[str] = None) -> dict:
    """
    Get a comprehensive project status summary

    Args:
        project_name: Project identifier (default uses 'default' project)
    """
    config = get_project_config(project_name)
    repo_dir = None

    try:
        repo_dir = clone_overleaf_repo(config["projectId"], config["gitToken"])

        # List all .tex files
        tex_files = list_files_in_repo(repo_dir, ".tex")

        summary = {
            "ok": True,
            "project_name": config.get("name", "Unknown"),
            "project_id": config["projectId"],
            "tex_files": tex_files,
            "tex_file_count": len(tex_files)
        }

        # Try to parse main file structure
        if tex_files:
            main_file = next((f for f in tex_files if "main" in f.lower()), tex_files[0])
            content = read_file_from_repo(repo_dir, main_file)
            sections = parse_latex_sections(content)

            summary["main_file"] = main_file
            summary["sections"] = [{"type": s["type"], "title": s["title"]} for s in sections]
            summary["section_count"] = len(sections)

        return summary
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        if repo_dir:
            shutil.rmtree(repo_dir, ignore_errors=True)

app = Starlette(routes=[Mount("/", app=mcp.streamable_http_app())])
