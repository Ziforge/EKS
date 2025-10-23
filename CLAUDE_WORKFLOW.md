# Claude Code Workflow Guide

**Purpose:** This document defines the preferred workflows, methodologies, and standards for PhD-level research and development. These standards ensure reproducibility, rigor, and academic integrity across all collaborative projects.

**Target Audience:** PhD candidates, academic researchers, and anyone requiring doctoral-level rigor in their work.

**Last Updated:** October 23, 2025
**Version:** 1.3 (PhD Standards Edition - No Emojis)

---

## Quick Reference: Non-Negotiable Requirements

**For ALL documents/papers:**
- [YES] **Disclose AI usage:** Include AI assistance statement in acknowledgements or methods
- [YES] **Avoid AI language:** No "notably", "importantly", "remarkably", "it's worth noting"
- [YES] **First-person:** Use "I" for single-author work, not passive voice
- [YES] **Cite primary sources:** Never cite without reading the original paper
- [YES] **Pin dependencies:** Exact versions in requirements.txt (numpy==1.24.3)
- [YES] **Validate algorithms:** Compare against analytical solutions or reference implementations

**AI Disclosure Template (Required):**
```latex
\section*{Acknowledgements}
The author acknowledges the use of Claude (Anthropic) for technical
writing assistance, code debugging, and workflow optimization during
this research.
```

**Forbidden Phrases:**
[NO] "It's worth noting..." | [NO] "Importantly..." | [NO] "Remarkably..." | [NO] "Interestingly..."

**Required:**
[YES] Direct statements | [YES] First-person active voice | [YES] Precise measurements with units

---

## Philosophy: PhD-Level Rigor

Doctoral research demands:
- **Reproducibility:** Every result must be independently verifiable
- **Transparency:** All methods, assumptions, and limitations documented
- **Integrity:** No claims without evidence, no shortcuts
- **Precision:** Exact measurements, proper error analysis, statistical validation
- **Thoroughness:** Comprehensive literature review, complete references
- **Innovation:** Novel contributions clearly distinguished from existing work

This workflow implements these principles at every level.

### Research Domain: DSP and Acoustics

**Specialization Focus:**
- Digital Signal Processing (real-time and offline)
- Acoustic signal processing and spatial audio
- Binaural synthesis and psychoacoustics
- Audio systems engineering (embedded, real-time)
- Physical modeling and measurement

**Domain-Specific Standards:**
- **Sample-accurate verification:** All DSP implementations verified at sample level
- **Perceptual validation:** Listening tests and psychoacoustic metrics
- **Physical accuracy:** Models validated against measurements or analytical solutions
- **Real-time constraints:** Latency, throughput, and computational complexity documented
- **Standardized formats:** SOFA, WAV, research-standard file formats
- **Measurement protocols:** Calibrated equipment, documented conditions, error analysis

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

[YES] **Good Examples:**
- `RUN_REALTIME_GUI.command` - Double-click to run
- HRTF databases auto-install on first run
- `START_HERE.md` guides user in 5 minutes
- Demo audio files play with any media player

[NO] **Anti-patterns:**
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

## PhD Research Standards

### 7. Academic Integrity and Attribution

**Citation Requirements:**
- **Primary sources:** Always cite original papers, not secondary references
- **Code attribution:** Credit libraries, algorithms, and datasets with proper citations
- **Data provenance:** Document source, version, and access date for all datasets
- **Methodology references:** Cite papers describing methods being implemented
- **No orphan claims:** Every technical statement has either a citation or derivation

**Example - Proper Attribution:**
```latex
% Good: Primary source with implementation details
The Woodworth spherical-head model~\cite{woodworth1954} provides...
ITD(\phi) = \frac{a}{c}(\sin\phi + \phi)  % Equation 2.1 from Woodworth

% Bad: No citation, unclear source
The head model gives ITD based on azimuth...
```

**HRTF Database Attribution:**
- MIT KEMAR: Gardner & Martin (1995), MIT Media Lab Technical Report #280
- CIPIC: Algazi et al. (2001), IEEE WASPAA
- Listen/IRCAM: IRCAM Listen database (2002), SOFA format
- Include URLs and access dates in bibliography

**AI Assistance Disclosure:**
- **ALWAYS disclose AI usage:** Every document that uses AI assistance must explicitly state this
- **Be specific:** Name the tool (Claude/Claude Code by Anthropic) and its role
- **Maintain academic integrity:** AI assists but does not author - you remain the sole author
- **Location:** Include disclosure in acknowledgements, methods, or dedicated AI usage statement

**Required Disclosure Format:**
```latex
\section*{AI Assistance Statement}
This work was developed with assistance from Claude (Anthropic), an AI
research assistant, for code development, literature synthesis, and
technical writing support. All scientific decisions, interpretations,
and conclusions remain solely those of the author. AI-generated content
was critically reviewed and validated before inclusion.
```

Or in Acknowledgements:
```latex
\section*{Acknowledgements}
The author acknowledges the use of Claude (Anthropic) for technical
writing assistance, code debugging, and workflow optimization during
this research.
```

**Writing Style Requirements:**
- **No emojis:** Never use emojis in professional/academic documents or responses
- **Avoid AI-like language:** No superlatives, no flowery prose, no unnecessary enthusiasm
- **Be direct and technical:** Focus on precision, accuracy, and clarity
- **Use scientific tone:** Formal but readable, objective without being robotic
- **First-person for single-author:** "I implemented..." not "was implemented..."
- **Avoid hedging when certain:** "The result shows..." not "appears to suggest..."

**AI Language Red Flags (Avoid These):**
[NO] "It's worth noting that..."
[NO] "Importantly..."
[NO] "Remarkably..."
[NO] "It should be emphasized..."
[NO] "Interestingly..."
[NO] "Notably..."
[NO] "Significantly..." (unless referring to statistical significance)
[NO] Excessive use of "comprehensive", "robust", "novel"

**Good Scientific Writing:**
[YES] "The ITD model produces accurate results within the specified error bounds."
[YES] "This implementation achieves 95% computational efficiency compared to..."
[YES] "Results show RMS error of 8.2 μs (σ = 1.4 μs), below the 10 μs threshold."
[YES] "I validated the algorithm against Woodworth's analytical solution."

### 8. Reproducibility Standards

**Code Reproducibility:**
- **Exact versions:** Pin all dependencies (`numpy==1.24.3`, not `numpy>=1.0`)
- **Random seeds:** Set and document all random seeds
- **Platform documentation:** OS, architecture, compiler versions
- **Computational resources:** CPU/GPU specs, execution time, memory usage
- **Environment files:** `requirements.txt`, `environment.yml`, Docker containers

**Data Reproducibility:**
- **Raw data preservation:** Never modify original data files
- **Processing pipeline:** Document all preprocessing steps with code
- **Versioning:** SHA256 checksums for datasets
- **Accessibility:** Public datasets with DOIs when possible
- **Generated data:** Include scripts to regenerate from raw data

**Example - Reproducibility Manifest:**
```yaml
experiment: binaural_synthesis_validation
date: 2025-10-23
environment:
  os: macOS 14.5
  python: 3.12.0
  packages:
    numpy: 1.24.3
    scipy: 1.11.2
  hardware:
    cpu: Apple M2
    ram: 16GB
datasets:
  mit_kemar:
    source: https://sound.media.mit.edu/resources/KEMAR/
    version: compact
    sha256: <hash>
    access_date: 2025-10-15
parameters:
  sample_rate: 48000
  head_radius: 0.0875  # meters, ±0.0005
  speed_of_sound: 343.0  # m/s, 20°C
random_seed: 42
```

### 9. Experimental Rigor

**DSP Algorithm Validation:**
1. **Analytical verification:** Compare against closed-form solutions where available
2. **Unit tests:** Test edge cases, boundary conditions, numeric stability
3. **Known-answer tests:** Verify against reference implementations
4. **Perceptual validation:** ABX tests, listening studies with statistical analysis
5. **Performance profiling:** CPU usage, memory, latency measurements

**Measurement Protocols:**
- **Calibration:** Document calibration procedures and dates
- **Environmental conditions:** Temperature, humidity, background noise levels
- **Equipment specifications:** Make, model, serial numbers, firmware versions
- **Uncertainty analysis:** Propagate measurement errors through calculations
- **Multiple trials:** Report mean, std dev, confidence intervals

**Example - ITD Measurement Validation:**
```python
def validate_itd_implementation():
    """
    Validate ITD function against Woodworth (1954) analytical solution.

    Test conditions:
    - Head radius: a = 8.75 cm (±0.5 mm, Knowles KEMAR)
    - Speed of sound: c = 343 m/s (20°C, dry air)
    - Azimuth range: ±90° (±0.1°)

    Acceptance criteria:
    - RMS error < 10 μs (JND for ITD ~ 10-20 μs)
    - Max error < 20 μs at any azimuth

    References:
    - Woodworth & Schlosberg (1954), Experimental Psychology
    - Kuhn (1977), "Model for interaural time differences"
    """
    a = 0.0875  # meters
    c = 343.0   # m/s

    # Test azimuths (degrees)
    azimuths = np.linspace(-90, 90, 181)
    phi_rad = np.deg2rad(azimuths)

    # Analytical solution (Woodworth formula)
    itd_analytical = (a / c) * (np.sin(phi_rad) + phi_rad)

    # Our implementation
    itd_computed = compute_itd(azimuths, head_radius=a)

    # Error analysis
    error = itd_computed - itd_analytical
    rms_error = np.sqrt(np.mean(error**2))
    max_error = np.max(np.abs(error))

    # Report with units
    print(f"RMS error: {rms_error*1e6:.2f} μs")
    print(f"Max error: {max_error*1e6:.2f} μs")

    # Statistical test
    assert rms_error < 10e-6, f"RMS error {rms_error*1e6:.1f} μs exceeds 10 μs threshold"
    assert max_error < 20e-6, f"Max error {max_error*1e6:.1f} μs exceeds 20 μs threshold"

    return {
        'rms_error_us': rms_error * 1e6,
        'max_error_us': max_error * 1e6,
        'passed': True
    }
```

### 10. Literature Review Standards

**Before implementing ANY algorithm:**
1. **Search academic databases:** IEEE Xplore, ACM Digital Library, Google Scholar
2. **Review seminal papers:** Find the original publication introducing the method
3. **Check for improvements:** Look for more recent refinements or corrections
4. **Implementation notes:** Check if authors provide reference implementations
5. **Validation data:** Find datasets or test cases used in original papers

**Minimum Citation Requirements:**
- **For each algorithm:** ≥1 primary source paper
- **For each dataset:** Original publication + access URL
- **For each metric:** Definition paper + any modifications
- **For each claim:** Supporting evidence or derivation

**Literature Search Checklist:**
- [ ] Searched Google Scholar for primary sources
- [ ] Checked IEEE Xplore for related work
- [ ] Reviewed Audio Engineering Society (AES) publications
- [ ] Checked arXiv for recent preprints
- [ ] Verified no contradicting results in recent literature
- [ ] Documented search terms and date

### 11. Statistical Rigor

**When reporting experimental results:**
- **Sample size:** Justify based on power analysis
- **Statistical tests:** Choose appropriate test (t-test, ANOVA, non-parametric)
- **Effect size:** Report Cohen's d, η², or other effect size measures
- **P-values:** Report exact values, not just p<0.05
- **Confidence intervals:** 95% CI for all estimates
- **Multiple comparisons:** Apply Bonferroni or FDR correction when needed

**Example - Perceptual Study Reporting:**
```
Listening Test Results:
- Participants: N=15 (normal hearing, age 22-34, mean=26.3±3.1 years)
- Trials: 50 per condition (total 750 trials)
- Task: ABX discrimination (parametric vs. measured HRTF)
- Results: 78.2% correct (95% CI: [74.1%, 82.3%])
- Chance level: 50%
- Statistical test: One-sample t-test vs. chance
- t(14) = 12.4, p < 0.001, Cohen's d = 3.2 (large effect)
- Conclusion: Participants reliably discriminate between conditions
```

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
- [YES] Found SOFA repository URL via official documentation
- [YES] Used `curl` to inspect directory listings
- [YES] Downloaded specific files with `wget`
- [YES] Verified with `file` command (HDF5 format)
- [YES] Confirmed file sizes match expectations

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
   [YES] Found installation
    Installing dependencies...
    Starting application...
   ```

### Documentation Creation

#### Structure for Technical Guides
```markdown
# Title - Clear and Specific

## Overview
Brief 2-3 sentence summary of what this document covers.

## What's Included
Bulleted list of components/features with status indicators ([YES]/[WARNING])

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
│ [YES] Complete                         │
│ [WARNING]  Warning/Attention needed        │
│ [NO] Error/Missing                    │
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
- **Use status indicators:** [YES] [WARNING] [NO] for visual clarity
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

### [NO] Don't Do This:

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

[YES] **Functionality:** Everything works as documented
[YES] **Reproducibility:** Anyone can recreate results
[YES] **Maintainability:** Code is clean and documented
[YES] **Professional:** Presentation is polished
[YES] **Complete:** No missing pieces or TODO markers
[YES] **Backed up:** Version controlled and pushed to remote
[YES] **User-friendly:** Plug-and-play experience for reviewers

---

**End of Workflow Guide v1.0**

*This document will evolve with each project. Update version number and date when making significant changes.*
