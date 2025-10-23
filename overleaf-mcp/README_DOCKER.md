# Overleaf MCP Docker Setup

This directory contains the Overleaf MCP server adapted for the MCP pipeline Docker environment.

## Configuration

### Step 1: Get Overleaf Credentials

1. **Git Token**:
   - Go to Overleaf Account Settings → Git Integration
   - Click "Create Token"
   - Copy the token

2. **Project ID**:
   - Open your Overleaf project
   - Find it in the URL: `https://www.overleaf.com/project/[PROJECT_ID]`

### Step 2: Edit projects.json

Edit `overleaf-mcp/projects.json` with your Overleaf credentials:

```json
{
  "projects": {
    "default": {
      "name": "My Thesis",
      "projectId": "YOUR_OVERLEAF_PROJECT_ID",
      "gitToken": "YOUR_OVERLEAF_GIT_TOKEN"
    },
    "paper2": {
      "name": "Another Paper",
      "projectId": "ANOTHER_PROJECT_ID",
      "gitToken": "ANOTHER_GIT_TOKEN"
    }
  }
}
```

### Step 3: Rebuild and Start

```bash
# Rebuild the service
docker compose build overleaf-mcp

# Start the service
docker compose up -d overleaf-mcp

# Check logs
docker compose logs -f overleaf-mcp
```

## Available Tools

The Overleaf MCP server exposes the following tools via FastMCP:

### `health`
Health check endpoint

### `list_projects`
List all configured Overleaf projects

### `list_files`
List files in an Overleaf project
- `project_name`: Project identifier (optional, defaults to "default")
- `extension`: File extension filter (default: ".tex")

### `read_file`
Read a file from an Overleaf project
- `file_path`: Path to the file (required)
- `project_name`: Project identifier (optional)

### `get_sections`
Get all sections from a LaTeX file
- `file_path`: Path to the LaTeX file (required)
- `project_name`: Project identifier (optional)

### `get_section_content`
Get content of a specific section
- `file_path`: Path to the LaTeX file (required)
- `section_title`: Title of the section (required)
- `project_name`: Project identifier (optional)

### `status_summary`
Get a comprehensive project status summary
- `project_name`: Project identifier (optional)

## Service Details

- **Container Name**: `mcp-overleaf`
- **Port**: 7105
- **Protocol**: HTTP/SSE (FastMCP)
- **Mount**: `/workspace/shared` (shared with other services)

## Testing

The service is running when you see:
```
INFO:     Uvicorn running on http://0.0.0.0:7105 (Press CTRL+C to quit)
```

## Integration with API Orchestrator

To add Overleaf endpoints to the API orchestrator, add routes in `api-orchestrator/server.py`:

```python
class OverleafListFilesReq(BaseModel):
    project_name: str = "default"
    extension: str = ".tex"

@app.post("/overleaf/list_files")
def overleaf_list_files(req: OverleafListFilesReq):
    return _proxy("mcp-overleaf", 7105, "/run/list_files", req.dict())
```

## Notes

- Each tool call clones the Overleaf Git repository fresh, ensuring you always get the latest content
- Git credentials are stored in `projects.json` (not committed to version control)
- The server uses Python and FastMCP, not the original Node.js implementation
- LaTeX section parsing supports `\section`, `\subsection`, and `\subsubsection` commands
