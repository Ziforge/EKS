# Claude Code Workflow Guide

**Purpose:** This document defines the preferred workflows, methodologies, and standards developed during the NTNU ITD/ILD submission project. Use this as a reference for future collaborative projects.

**Last Updated:** October 22, 2025
**Version:** 1.0

---

## Core Principles

### 1. Verification-First Approach
- **Always verify before proceeding:** Read files, check existence, validate data before making assumptions
- **Test incrementally:** After each significant change, verify it works before moving to the next step
- **Proof of completion:** Provide evidence (file listings, checksums, test outputs) that tasks are complete
- **Never assume:** If unclear about file paths, data formats, or requirements - check first

### 2. Documentation Standards
- **Multiple documentation levels:**
  - `START_HERE.md` - Quick start for new users/reviewers (5 min read)
  - `README.md` - Comprehensive documentation (complete reference)
  - Specialized guides (e.g., `HRTF_PLUG_AND_PLAY.md`) for specific subsystems
  - Status files (e.g., `BUNDLE_STATUS.txt`) for inventory/checklist tracking

- **Documentation must include:**
  - Clear step-by-step instructions
  - Expected outcomes/verification steps
  - Troubleshooting sections
  - File structure diagrams (ASCII art tables/trees)
  - Version information and update dates

### 3. Task Management with TodoWrite
- **Use TodoWrite for:**
  - Multi-step tasks (3+ steps)
  - Complex operations requiring tracking
  - Tasks with dependencies
  - Tasks that take significant time

- **Task structure:**
  - `content`: Imperative form ("Download HRTF databases")
  - `activeForm`: Present continuous ("Downloading HRTF databases")
  - `status`: pending → in_progress → completed

- **Best practices:**
  - Only ONE task in_progress at a time
  - Mark completed IMMEDIATELY after finishing (no batching)
  - Update status in real-time as work progresses
  - Remove tasks that become irrelevant

### 4. Version Control Standards

#### Git Workflow
1. Initialize with meaningful `.gitignore`
2. Create descriptive commit messages with:
   - Summary line (50 chars max)
   - Blank line
   - Detailed description with bullet points
   - File counts and size info when relevant
3. Use private repositories by default for academic/sensitive work
4. Verify push success (check file count, remote status)

#### Commit Message Format
```
Brief summary of changes

- Detailed point 1
- Detailed point 2
- Statistics (e.g., "468 files, 9.3 MB of data")

Context or reasoning for changes
```

### 5. Professional Academic Standards

#### LaTeX Documents
- **Always use Read tool before editing** existing LaTeX files
- **Preserve exact indentation** from line-numbered output
- **Use first-person singular ("I")** for single-author papers
- **Verify all cross-references:**
  - Figures: `\label{fig:name}` → `\ref{fig:name}`
  - Tables: `\label{tab:name}` → `\ref{tab:name}`
  - Equations: `\label{eq:name}` → `\eqref{eq:name}`
  - Sections: `\label{sec:name}` → `\ref{sec:name}`
- **Compile twice** to resolve all cross-references
- **Check for "??" or "??" in PDF** before considering complete

#### Reports and Documentation
- **Accuracy over completion:** Don't claim features/data that don't exist
- **Explicit attribution:** Credit sources (MIT KEMAR, CIPIC, Listen/IRCAM, etc.)
- **Version tracking:** Include dates, version numbers, and change logs
- **Reproducibility:** Provide complete file paths, commands, and requirements

### 6. Plug-and-Play Philosophy

Every deliverable should work **immediately** for reviewers:

✅ **Good Examples:**
- `RUN_REALTIME_GUI.command` - Double-click to run
- HRTF databases auto-install on first run
- `START_HERE.md` guides user in 5 minutes
- Demo audio files play with any media player

❌ **Anti-patterns:**
- Requiring manual configuration
- Assuming knowledge of system paths
- Missing dependencies without clear error messages
- Broken relative imports

**Implementation checklist:**
- [ ] Test on fresh environment (no assumptions)
- [ ] Include all dependencies
- [ ] Auto-detect and fix common issues
- [ ] Provide clear error messages with solutions
- [ ] Document all requirements upfront

---

## Specific Workflows

### Research and Information Gathering

#### When searching for missing resources:
1. **Check local system first:**
   ```bash
   find ~ -name "*pattern*" 2>/dev/null
   ls -la expected/path/
   ```

2. **Search official sources:**
   - Official documentation sites (e.g., sofaconventions.org)
   - GitHub repositories
   - Academic/research institution sites

3. **Verify file integrity:**
   ```bash
   file filename.ext          # Check file type
   du -sh filename.ext        # Check size
   head -n 20 filename.ext    # Inspect contents
   ```

#### For missing HRTF databases (example from this project):
- ✅ Found SOFA repository URL via official documentation
- ✅ Used `curl` to inspect directory listings
- ✅ Downloaded specific files with `wget`
- ✅ Verified with `file` command (HDF5 format)
- ✅ Confirmed file sizes match expectations

### Code Integration

#### Python Package Structure
- **Prefer editing existing files** over creating new ones
- **Respect package imports:**
  - Absolute imports for installed packages: `from package.module import func`
  - Relative imports within package: `from .module import func`
- **Test imports before committing:**
  ```bash
  python3 -c "import module; print('OK')"
  ```

#### Real-time Systems
When building launchers for real-time applications:
1. **Detect installation directory dynamically:**
   ```bash
   SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
   ```
2. **Check dependencies before running:**
   ```bash
   if ! command -v python3 &> /dev/null; then
       echo "Error: Python 3 not found"
       exit 1
   fi
   ```
3. **Auto-install missing components:**
   ```bash
   if [ ! -d "$TARGET_DIR" ]; then
       echo "Installing..."
       cp -r "$SOURCE_DIR" "$TARGET_DIR"
   fi
   ```
4. **Provide clear status messages:**
   ```
   ✅ Found installation
   📦 Installing dependencies...
   🚀 Starting application...
   ```

### Documentation Creation

#### Structure for Technical Guides
```markdown
# Title - Clear and Specific

## Overview
Brief 2-3 sentence summary of what this document covers.

## What's Included
Bulleted list of components/features with status indicators (✅/⚠️)

## Quick Start
Step-by-step instructions (numbered) for most common use case

## Detailed Usage
### Feature 1
- Description
- Parameters
- Examples
- Troubleshooting

## Verification
How to confirm everything is working correctly

## References
Links to relevant documentation, papers, repositories
```

#### ASCII Art for Clarity
Use boxes and tables for important information:

```
╔═══════════════════════════════════════╗
║  IMPORTANT: Key Information Here      ║
╚═══════════════════════════════════════╝

┌─────────────────────────────────────┐
│ Status Indicators:                  │
├─────────────────────────────────────┤
│ ✅ Complete                         │
│ ⚠️  Warning/Attention needed        │
│ ❌ Error/Missing                    │
└─────────────────────────────────────┘
```

### File Operations

#### Before Writing Files
1. **Read existing file first** (if it exists)
2. **Preserve formatting** (indentation, line endings)
3. **Verify write success:**
   ```bash
   ls -lh path/to/file
   head -n 10 path/to/file
   ```

#### Before Editing Files
1. **Always use Read tool first** to see current content
2. **Match exact indentation** from line-numbered output (ignore line number prefix)
3. **Make minimal changes** - don't rewrite entire files unnecessarily
4. **Verify edit with grep/head** after completion

#### Directory Operations
1. **Check parent directory exists** before creating subdirectories
2. **Use `mkdir -p`** to create nested directories safely
3. **Verify with `ls -la`** after creation

---

## Error Recovery Patterns

### Pattern 1: Missing Dependencies
**Problem:** Import/library not found
**Steps:**
1. Check if package is installed: `python3 -c "import package"`
2. Check requirements.txt for version
3. Install with pip: `pip3 install package`
4. Verify installation: `pip3 show package`
5. Retry original operation

### Pattern 2: File Not Found
**Problem:** Expected file doesn't exist
**Steps:**
1. List parent directory: `ls -la parent/`
2. Search for similar names: `find . -name "*partial_name*"`
3. Check documentation for correct path
4. If missing, download from source or regenerate
5. Verify with `file` command

### Pattern 3: Reference/Link Broken
**Problem:** LaTeX references show "??" or links are broken
**Steps:**
1. Search for label: `grep -n "\\label{target}" file.tex`
2. Check reference syntax: `\ref{target}` or `\eqref{target}`
3. Ensure label exists before reference in document
4. Compile twice: `pdflatex file.tex` (run 2x)
5. Verify in PDF output

### Pattern 4: Permission Denied
**Problem:** Cannot execute script
**Steps:**
1. Check current permissions: `ls -l script.sh`
2. Add execute permission: `chmod +x script.sh`
3. Verify: `ls -l script.sh`
4. Test execution: `./script.sh`

---

## Communication Standards

### Progress Updates
- **Show, don't just tell:** Include file listings, sizes, checksums
- **Use status indicators:** ✅ ⚠️ ❌ for visual clarity
- **Provide context:** Explain *why* a step is needed, not just *what*
- **Be proactive:** Mention potential issues before user discovers them

### Error Reporting
When something fails:
1. **State the problem clearly**
2. **Show the error message** (exact text)
3. **Explain what was attempted**
4. **Provide 2-3 solution options**
5. **Ask for user preference** if multiple approaches exist

### Questions to User
- **Be specific:** "Should I use Synthetic or MIT KEMAR HRTFs?" not "Which one?"
- **Provide context:** Explain implications of each choice
- **Offer recommendation:** Based on project requirements
- **Use AskUserQuestion tool** for structured choices

---

## Project-Specific Patterns (NTNU ITD/ILD)

### HRTF Database Management
- **Always include all available modes:** Synthetic, MIT KEMAR, CIPIC, Listen/IRCAM
- **Verify file formats:**
  - MIT KEMAR: WAV files (44.1 kHz)
  - CIPIC: MATLAB .mat files
  - Listen/IRCAM: SOFA (HDF5) files
- **Check file integrity:** Use `file` command
- **Document sources:** Credit repositories and provide URLs

### Audio File Verification
```bash
# Check audio format
file demo.wav

# Check duration and sample rate
soxi demo.wav  # or ffprobe

# Verify stereo/binaural
soxi -c demo.wav  # should show 2 channels
```

### LaTeX Compilation Workflow
```bash
# First compilation
pdflatex document.tex

# Check for undefined references
grep "??" document.log

# Second compilation (resolve cross-refs)
pdflatex document.tex

# Check for remaining warnings
grep "Warning" document.log

# Verify output
pdfinfo document.pdf
```

---

## Quality Checklist

Before considering any deliverable complete:

### Code Quality
- [ ] Runs without errors on fresh environment
- [ ] All imports resolve correctly
- [ ] Requirements.txt is complete and accurate
- [ ] Tests pass (if applicable)
- [ ] No hardcoded paths (use relative or auto-detect)

### Documentation Quality
- [ ] START_HERE.md exists and is accurate
- [ ] README.md is comprehensive
- [ ] All file paths are correct
- [ ] Installation instructions tested
- [ ] Troubleshooting section included

### File Organization
- [ ] Clear directory structure
- [ ] No duplicate files
- [ ] All referenced files exist
- [ ] No broken symbolic links
- [ ] Appropriate .gitignore configured

### Version Control
- [ ] All files committed
- [ ] Descriptive commit messages
- [ ] Pushed to remote (if applicable)
- [ ] Repository is private (for sensitive work)
- [ ] README updated to reflect current state

### Submission Readiness
- [ ] All assignment requirements met
- [ ] Bonus features documented
- [ ] References/citations complete
- [ ] No "TODO" markers remaining
- [ ] Professional presentation

---

## Anti-Patterns to Avoid

### ❌ Don't Do This:

1. **Assuming file existence:**
   ```bash
   # Bad
   cat /path/to/file.txt

   # Good
   if [ -f /path/to/file.txt ]; then
       cat /path/to/file.txt
   else
       echo "File not found"
   fi
   ```

2. **Editing without reading:**
   ```python
   # Bad: Edit file without reading first
   edit_file("config.py", old="value1", new="value2")

   # Good: Read, verify, then edit
   read_file("config.py")
   # [verify content exists]
   edit_file("config.py", old="value1", new="value2")
   ```

3. **Vague communication:**
   ```
   # Bad
   "I updated the file"

   # Good
   "Updated HRTF_PLUG_AND_PLAY.md:
   - Changed '3 HRTF modes' to '4 HRTF modes'
   - Added Listen/IRCAM section with 3 SOFA files
   - Updated total size from 5.3 MB to 9.3 MB"
   ```

4. **Creating unnecessary files:**
   ```
   # Bad: Create new documentation when existing README could be updated
   # Good: Update existing README.md with new section
   ```

5. **Ignoring errors:**
   ```bash
   # Bad
   command || true  # Hide failures

   # Good
   if ! command; then
       echo "Command failed, investigating..."
       # Handle error appropriately
   fi
   ```

---

## Adaptation Notes

**How to update this workflow:**

1. **Add new patterns** as they emerge from projects
2. **Document failures** and how they were resolved
3. **Refine existing patterns** based on what works
4. **Remove obsolete patterns** that no longer apply
5. **Version this document** (increment version number at top)

**To reference this workflow in future conversations:**

> "Please follow the methodologies in CLAUDE_WORKFLOW.md for this project"

Or for specific sections:

> "Use the HRTF Database Management workflow from CLAUDE_WORKFLOW.md"

---

## Example: Applying This Workflow

### Scenario: Adding new feature to existing project

**Step 1: Verify current state**
```bash
git status
ls -la relevant/directory/
```

**Step 2: Create todo list**
Use TodoWrite to track:
- Research requirements
- Implement feature
- Test feature
- Update documentation
- Commit changes

**Step 3: Read before edit**
```bash
# Read existing files
read relevant/file.py
read README.md
```

**Step 4: Implement incrementally**
- Make smallest change possible
- Test immediately
- Mark todo as complete
- Move to next step

**Step 5: Document changes**
- Update README.md
- Add code comments
- Create examples if needed

**Step 6: Version control**
```bash
git add .
git commit -m "Add feature X

- Implemented Y functionality
- Updated documentation
- Added tests

Resolves issue #Z"
git push
```

**Step 7: Verify completion**
- Run tests
- Check all files present
- Verify documentation accurate
- Mark all todos complete

---

## Success Metrics

A project following this workflow should achieve:

✅ **Functionality:** Everything works as documented
✅ **Reproducibility:** Anyone can recreate results
✅ **Maintainability:** Code is clean and documented
✅ **Professional:** Presentation is polished
✅ **Complete:** No missing pieces or TODO markers
✅ **Backed up:** Version controlled and pushed to remote
✅ **User-friendly:** Plug-and-play experience for reviewers

---

**End of Workflow Guide v1.0**

*This document will evolve with each project. Update version number and date when making significant changes.*
