# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a microservices-based MCP (Model Context Protocol) pipeline for embedded audio/DSP development workflows. The system consists of multiple specialized MCP servers running in Docker containers, each providing domain-specific build tools and capabilities (C++, JUCE, Faust, Bela, FPGA/VHDL, Daisy, plugins, docs, metrics). An API orchestrator provides unified HTTP access to these services.

## Architecture

### Service Structure

The repository follows a consistent pattern for each MCP service:

- **MCP Servers** (`*-mcp/` directories): Domain-specific servers using FastMCP or raw MCP protocol over WebSocket
  - Each exposes tools via the MCP protocol (WebSocket on port 70xx)
  - Use FastMCP with `stateless_http=True` for HTTP/SSE support
  - Mounted at `/mcp` for MCP protocol, `/run/*` for direct HTTP endpoints

- **API Orchestrator** (`api-orchestrator/`): FastAPI service that proxies HTTP requests to MCP services
  - Provides unified REST API at port 8080
  - Routes requests to internal Docker network service names (e.g., `mcp-cpp:7020`)
  - Handles service discovery and request forwarding

- **Shared Workspace** (`shared/`): Common volume mounted at `/workspace/shared` in all containers
  - Contains project directories: `cpp/`, `juce/`, `daisy/`, `fpga/`, `vhdl/`, `plugins/`
  - All services access projects via this shared filesystem

### Key Services

- **cpp-mcp** (port 7020): CMake-based C++ builds
- **juce-mcp** (port 7040): JUCE audio plugin framework builds
- **faust-mcp** (port 7075): Faust DSP compiler (targets: bela, cpp)
- **bela-mcp** (port 7078): Bela board deployment via SSH (upload, run, stop)
- **daisy-mcp** (port 7050): Electrosmith Daisy builds
- **fpga-mcp** (port 7060): Xilinx Vivado FPGA synthesis
- **vhdl-mcp** (port 7030): VHDL synthesis
- **plugin-mcp** (port 7072): Audio plugin validation
- **docs-mcp** (port 7070): LaTeX document compilation (pdflatex + bibtex)
- **metrics-mcp** (port 7095): Audio quality metrics (SNR calculations)
- **dsp-mcp** (port 7010): DSP utilities (minimal implementation)
- **orchestrator-mcp** (port 7090): Workflow orchestration (minimal implementation)
- **ml-mcp** (port 7080): Machine learning tools
- **kicad-mcp** (port 7015): KiCad PCB design tools

### Path Conventions

All services normalize paths to container-style:
- Input: `shared/cpp/hello` or `/workspace/shared/cpp/hello`
- Normalized: `/workspace/shared/cpp/hello`
- Pattern: `path if path.startswith("/workspace/") else "/workspace/" + path.lstrip("/")`

## Development Commands

### Environment Setup

```bash
# Install all dependencies (Homebrew packages including Colima, Docker, toolchains)
bash brew_setup.sh

# Start minimal services (dsp, cpp, docs, orchestrator, metrics)
bash up-min.sh

# Start all services (includes Bela, JUCE, Faust, FPGA, etc.)
bash up-all.sh

# Stop all services
bash down.sh
```

### Container Management

```bash
# Minimal startup uses: 4 CPU, 8GB RAM, 60GB disk
colima start --cpu 4 --memory 8 --disk 60

# Full startup uses: 6 CPU, 16GB RAM, 120GB disk
colima start --cpu 6 --memory 16 --disk 120

# Rebuild services after code changes
docker compose build

# View logs for a specific service
docker compose logs -f mcp-cpp

# Access service shell
docker exec -it mcp-cpp bash
```

### Testing Services

```bash
# Health check API orchestrator
curl http://localhost:8080/health

# Example: Build C++ project via API
curl -X POST http://localhost:8080/cpp/build \
  -H "Content-Type: application/json" \
  -d '{"project_dir": "shared/cpp/hello", "build_type": "Release"}'

# Direct MCP service access (WebSocket/HTTP)
# MCP services expose tools at ws://localhost:70xx and http://localhost:70xx/mcp
```

## Adding New MCP Services

When creating a new MCP service:

1. Create directory structure:
   ```
   service-mcp/
   ├── Dockerfile
   ├── requirements.txt
   └── server.py
   ```

2. Use FastMCP template in `server.py`:
   ```python
   from starlette.applications import Starlette
   from starlette.routing import Mount
   from mcp.server.fastmcp import FastMCP

   mcp = FastMCP(name="ServiceName", stateless_http=True)

   @mcp.tool()
   def tool_name(param: str) -> dict:
       """Tool description"""
       return {"ok": True, "result": "..."}

   app = Starlette(routes=[Mount("/", app=mcp.streamable_http_app())])
   ```

3. Add service to `docker-compose.yml`:
   - Use consistent naming: `service-mcp` (directory), `mcp-service` (container)
   - Assign sequential port: 70XX (WebSocket/HTTP)
   - Mount `/workspace/shared` volume
   - Add to orchestrator dependencies if needed

4. Update `api-orchestrator/server.py` if HTTP proxy needed

## Special Environment Requirements

- **Bela**: Requires Bela SDK at `${HOME}/SDKs/Bela`, mounted read-only
- **JUCE**: Requires VST3 SDK at `${HOME}/SDKs/VST3_SDK`, mounted read-only
- **FPGA**: Requires Xilinx Vivado at `/opt/Xilinx`, mounted read-only
- **ccache**: C++ services use persistent ccache volume for build acceleration

## MCP Bridge

The `mcp-bridge/` directory contains integration tools for connecting MCP services to LLM tools (OpenWebUI, GPT tools). See `mcp-bridge.json` for OpenWebUI action configuration.

## Jupyter Integration

JupyterLab runs at `http://localhost:8888` (no token) with access to:
- DSP, ML, and Faust MCP services
- Shared workspace at `/home/jovyan/shared`

### Jupyter-Overleaf Workflow

The `shared/workflow/` package provides an integrated workflow for academic writing:
- Jupyter Notebook → LaTeX → PDF → Overleaf → GitHub
- Automatically installed in JupyterLab on container startup
- Integrates with docs-mcp (port 7070) for LaTeX compilation
- Integrates with overleaf-mcp (port 7105) for Overleaf sync

Usage in notebooks:
```python
from workflow import notebook_to_paper, compile_latex, sync_to_overleaf

# Convert notebook to LaTeX
result = notebook_to_paper(
    notebook="my_research.ipynb",
    output_dir="shared/docs/my_paper",
    template="twocolumn"
)

# Compile to PDF using docs-mcp
pdf = compile_latex(result['main_tex'], use_mcp=True)

# Sync to Overleaf (requires configuration)
sync_to_overleaf(
    latex_dir="shared/docs/my_paper",
    project_name="default"
)
```

Available templates:
- `article` - Single column
- `twocolumn` - Conference format
- `ieee` - IEEE style
- `acta_acustica` - Acta Acustica journal (default for George's work)
- `thesis` - Dissertation format

See `shared/workflow/README.md` for full documentation.

---

# Academic Writing Guidelines for PhD Work

## User Profile and Specialization

**PhD Candidate:** George Redpath
**Email:** ghredpath@hotmail.com
**Institutions:**
- Norwegian University of Science and Technology (NTNU) - Primary
- Aalborg University (AAU) - Collaboration
**Department:** Electronic Systems

**Core Specialization:**
- DSP (Digital Signal Processing) and Acoustics
- **Instrument Design** (primary research interest)
- Drums and Percussion
- Modular Synthesizers

**Interdisciplinary Influences:**
- Design philosophy and aesthetics
- Art and cultural contexts
- History and evolution of musical instruments
- Philosophy of sound and music
- Cultural impact on instrument design

**Research Focus:**
- Binaural audio synthesis and spatial hearing
- HRTF modeling and implementation
- Physical modeling of acoustic instruments
- Intersection of technical performance and artistic expression in instrument design
- Cultural and historical influences on modern instrument development

## Core Principles

### 1. Claude Usage Disclosure
- **ALWAYS** clarify that Claude was used in all documents
- Include acknowledgment: "This work was developed with assistance from Claude (Anthropic)"
- Maintain transparency about AI collaboration in academic integrity

### 2. Language and Tone
- Write in **clear, professional, human-readable scientific prose**
- Be natural and direct - avoid robotic or overly formal constructions
- Use active voice when appropriate to maintain readability
- Technical precision does not require stilted language
- Academic writing should be rigorous but accessible to human readers

### 3. Forbidden Qualifiers
**NEVER** use these unnecessary hedging phrases:
- "Simplified"
- "Defensible"
- "Straightforward"
- "Trivial"
- "Obviously"
- "Clearly"
- "Simply"
- "Easily"

Instead: State facts directly. If something is simple, the mathematics/implementation will demonstrate that without commentary.

### 4. Claude's Interaction Style (when responding to George)
**DO NOT** include Claude's meta-commentary in documents:
- Keep "Let me...", "I will...", "I'm going to..." OUT of written documents
- These phrases are fine when Claude is talking to George directly
- But NEVER put them in papers, reports, LaTeX documents, or code comments
- Documents should contain only the actual content, not narration of the writing process

### 5. No Emojis
- **NEVER** use emojis in any academic document unless explicitly requested
- This includes reports, papers, documentation, README files, and LaTeX documents

## LaTeX and Document Standards

### Paper Format
- **REQUIRED**: All research papers MUST use Acta Acustica template
- **Always use 2-column format** as per Acta Acustica standards
- No exceptions: IEEE, AES, or other templates should not be used
- All papers must contain verified and reliable references from peer-reviewed sources
- Use BibTeX for all citations with proper entry types (@article, @inproceedings, @book)
- Include DOI links where available
- Follow Acta Acustica citation style guidelines exactly

### Diagrams and Figures
- **All diagrams must be created in TikZ**
- No raster images for technical diagrams unless showing experimental data
- Include physical interpretations with all equations
- Every figure must have a descriptive caption explaining the physics and perceptual meaning

### Mermaid Diagrams
- **When using Mermaid diagrams, color ONLY the boundaries/borders**
- Do NOT fill the entire shape with color as it reduces legibility
- Use stroke/border colors to differentiate elements while keeping backgrounds light or transparent
- Example: `style NodeA stroke:#ff0000,stroke-width:3px` (good)
- Avoid: `style NodeA fill:#ff0000` (bad - reduces text legibility)

### Equations
- Every equation must be accompanied by:
  1. **Physical interpretation**: What does this represent in the physical world?
  2. **Perceptual interpretation**: What does this mean for human perception/hearing?
  3. **Symbol definitions**: Define all symbols in tables
  4. **Units**: Always specify units for physical quantities

### Example Format:
```latex
\begin{equation}
\Delta t(\varphi) = \frac{a}{c}(\varphi + \sin\varphi)
\label{eq:woodworth_itd}
\end{equation}

\textbf{Physical interpretation:} The interaural time difference $\Delta t$ results from the path-length difference around the spherical head of radius $a$, where the arc term $a\varphi$ accounts for surface diffraction and $a\sin\varphi$ represents the direct chord component.

\textbf{Perceptual interpretation:} An ITD of $10\,\mu$s corresponds to approximately $1°$ azimuth discrimination at the frontal midline, representing the just-noticeable difference for spatial localization at low frequencies below 1.5 kHz where phase cues dominate.
```

## Code and Implementation Documentation

### Python Code
- Follow PEP 8 style guidelines
- Include comprehensive docstrings with:
  - Physical meaning of parameters
  - Units for all physical quantities
  - References to equations in accompanying papers
- Type hints for all function signatures

### README Files
- Always include:
  - Clear installation instructions
  - Exact commands to reproduce results
  - System requirements with tested configurations
  - Expected outputs with example values
- No marketing language or hype
- Focus on reproducibility

## Version Control and Sharing

### GitHub
- **All repositories are PRIVATE by default**
- Upload all work privately to GitHub unless explicitly told to make public
- Only make repositories public when George explicitly instructs "make this public"
- Include proper .gitignore files
- Always include LICENSE file (specify which license to use)
- Comprehensive README.md at repository root
- **Author**: George Redpath (ghredpath@hotmail.com)
- All commits should be authored by George Redpath
- Include proper attribution in all files

### Overleaf Integration
- **REQUIRED**: All LaTeX documents must be uploaded to Overleaf
- Use Overleaf MCP integration (available as of October 2025)
- Maintain synchronization between local LaTeX files and Overleaf projects
- Share Overleaf projects with supervisors as needed

### Workflow
1. Write LaTeX locally with TikZ diagrams
2. Compile and verify locally with pdflatex
3. Upload/sync to Overleaf for collaboration
4. Push final versions to private GitHub repository
5. Only make public with explicit permission

## Document Structure Requirements

### Technical Reports
1. **Abstract**: Concise summary without qualifiers
2. **Introduction**: State problem, prior work, contributions
3. **Methodology**: Detailed technical approach with equations
4. **Results**: Quantitative data with figures
5. **Discussion**: Interpretation and limitations
6. **Conclusion**: Summary and future work
7. **References**: BibTeX formatted, verified sources

### Code Documentation
1. **README.md**: Installation, usage, examples
2. **requirements.txt** or **environment.yml**: Exact dependencies
3. **LICENSE**: Appropriate open-source license
4. **CLAUDE.md**: Project-specific guidelines (like this file)

### Figure Standards
- Vector graphics (PDF) for all technical diagrams
- TikZ source code included in repository
- Minimum 300 DPI for any raster images (experimental data)
- Colorblind-friendly color schemes
- Clear axis labels with units

## Reproducibility Standards

Every computational result must be:
1. **Deterministic**: Fixed random seeds where applicable
2. **Documented**: All parameters recorded
3. **Verifiable**: Include test cases with expected outputs
4. **Timestamped**: Record software versions and dates

### Example:
```python
# Reproducible experiment
np.random.seed(42)  # Fixed seed for reproducibility
fs = 44100  # Hz - sample rate
a = 0.09    # m - head radius
c = 343     # m/s - sound speed at 20°C
# Processing timestamp: 2025-10-23
```

## Common Mistakes to Avoid

1. ❌ Using hedging language ("simplified", "defensible") in documents
2. ❌ Including Claude's meta-commentary ("Let me...", "I will...") in documents
3. ❌ Including emojis in technical documents
4. ❌ Missing physical/perceptual interpretations for equations
5. ❌ Undefined symbols or missing units
6. ❌ Raster diagrams instead of TikZ
7. ❌ Forgetting to upload LaTeX to Overleaf
8. ❌ Making repositories public without explicit permission
9. ❌ Missing Claude usage acknowledgment
10. ❌ Robotic or stilted writing - documents should be natural and human-readable
11. ❌ Single-column format for academic papers
12. ❌ Wrong author attribution (always: George Redpath)

## Quality Checklist

Before finalizing any academic document:

- [ ] Author: George Redpath correctly attributed
- [ ] Claude usage acknowledged
- [ ] No hedging qualifiers ("simplified", "defensible")
- [ ] No Claude meta-commentary in documents ("Let me...", "I will...")
- [ ] Natural, human-readable prose (not robotic or stilted)
- [ ] No emojis (unless explicitly requested)
- [ ] Two-column format (for papers)
- [ ] All equations have physical + perceptual interpretations
- [ ] All symbols defined with units
- [ ] All diagrams in TikZ (vector format)
- [ ] References verified and formatted in BibTeX
- [ ] Code is reproducible with fixed seeds
- [ ] README includes installation and usage
- [ ] LaTeX uploaded to Overleaf
- [ ] Repository is private (unless George explicitly says "make this public")
- [ ] Follows Acta Acustica template (for papers)

---

## Thesis-Specific Guidelines

For PhD thesis chapters and papers:

### Structure
- Follow NTNU thesis template requirements
- Each chapter should be publishable as standalone paper
- Consistent notation across all chapters
- Comprehensive symbol glossary

### Collaboration
- Supervisor: Peter Svensson (TTT4295 Acoustic Signal Processing)
- Acknowledge all collaborators and funding sources
- Share Overleaf projects with supervisors

### Defense Preparation
- All figures must be presentation-ready
- Code repositories must be public or shared with committee
- Reproducibility is critical for thesis defense

---

## Research Standards and Ethics

### Experimental Data
- All experimental data must be archived with metadata
- Include sampling rates, equipment specifications, calibration data
- Store raw data separately from processed data
- Document all processing steps for reproducibility
- Use version control for data processing scripts

### Statistical Analysis
- Report effect sizes, not just p-values
- Include confidence intervals where appropriate
- State statistical tests used and assumptions checked
- For listening tests: report listener demographics and screening criteria
- Power analysis for sample size justification

### Open Science Practices
- Preregister studies where applicable
- Share data and code in repositories (Zenodo, OSF, GitHub)
- Use FAIR principles: Findable, Accessible, Interoperable, Reusable
- License data appropriately (CC-BY-4.0 recommended for data)
- License code appropriately (MIT or GPL-3.0 for academic code)

## Literature Review Standards

### Citation Requirements
- Prioritize peer-reviewed journal articles and conference proceedings
- Check citation count and journal impact factor for quality
- Include seminal/foundational papers in the field
- Balance recent work (last 5 years) with classic references
- For acoustics: prioritize JASA, Acta Acustica, IEEE/ACM TASLP, AES journals

### Key Journals and Conferences for DSP/Acoustics
**Journals:**
- Journal of the Acoustical Society of America (JASA)
- Acta Acustica united with Acustica
- IEEE/ACM Transactions on Audio, Speech, and Language Processing
- Applied Acoustics
- Journal of the Audio Engineering Society (JAES)

**Conferences:**
- AES Convention and Conference proceedings
- ICASSP (IEEE International Conference on Acoustics, Speech and Signal Processing)
- DAFX (International Conference on Digital Audio Effects)
- Interspeech
- ICA (International Congress on Acoustics)

### Reference Management
- Use Zotero or Mendeley for bibliography management
- Export to BibTeX for LaTeX integration
- Keep .bib files under version control
- Consistent naming: `author_year_keyword.bib`

### Citation Patterns and Strategies

Based on analysis of George's academic writing (Neuroverse dissertation, Physical Modeling papers), follow these citation strategies:

#### Citation Style
- **IEEE-style numbered citations**: [1], [2], [3] etc.
- Multiple citations grouped: [1], [2], [5] or [11–14]
- No author-year citations in-text (those belong in references section only)
- Citations appear AFTER punctuation in most cases

#### Citation Density by Section

**Literature Review:**
- Dense citation clusters (2-5 citations per paragraph)
- Multiple citations per sentence when establishing state of the art
- Example pattern: "Recent studies [1], [2], [5] demonstrate... while earlier work [8], [9] suggested..."
- Purpose: Establish comprehensive coverage of existing research

**Methods/Implementation:**
- Moderate citation density (1-2 per paragraph)
- Cite specific technical validation sources
- Reference established algorithms and frameworks
- Example: "We implement the Woodworth ITD model [12] with bilinear transform [15]"
- Purpose: Technical validation and methodology justification

**Results:**
- Sparse citations (only when interpreting with theory)
- Cite references only when connecting results to existing literature
- No citations needed for raw data presentation
- Purpose: Let results speak for themselves unless theoretical connection is needed

**Discussion:**
- Moderate citation density (1-3 per paragraph)
- Connect findings back to literature
- Compare with prior work explicitly
- Purpose: Position results within existing body of knowledge

#### Citation Purpose Categories

When citing sources, each citation should serve one of these purposes:

**1. Theoretical Grounding**
- Cite frameworks that structure the research
- Examples from Neuroverse: Dunn's Sensory Processing Framework [11][12], Polyvagal Theory [22], Predictive Coding [20]
- Use when: Establishing conceptual foundations

**2. Technical Validation**
- Reference established algorithms and methods
- Examples from papers: Schroeder (1962), Moorer (1979), Unity documentation
- Use when: Justifying implementation choices with proven techniques

**3. Design Justification**
- Support design decisions with perceptual/empirical research
- Examples: FORCE Technology Sound Wheel [25], Gestalt principles, color theory
- Use when: Explaining why certain design choices were made

**4. Empirical Support**
- Include studies demonstrating specific effects
- Examples: Mills (1958) for minimum audible angle, Marco et al. (2011) for sensory profiles
- Use when: Claiming empirical facts about perception or performance

#### Source Type Hierarchy

Prioritize sources in this order:

1. **Peer-reviewed journal articles** (highest priority)
   - JASA, Acta Acustica, IEEE Trans, J Med Internet Res
   - Use for: Core theoretical claims and empirical findings

2. **Peer-reviewed conference proceedings**
   - AES Convention, DAFX, ICASSP, NIME
   - Use for: Technical implementations and novel methods

3. **Established technical books**
   - Schlosberg & Woodworth, Bilbao, Smith
   - Use for: Foundational concepts and classical methods

4. **Industry/institutional standards**
   - FORCE Technology, Unity documentation, IRCAM standards
   - Use for: Practical frameworks and implementation details

5. **Dissertations and theses**
   - Use sparingly, only when no published source available

6. **Preprints and arXiv**
   - Only when very recent and no peer-reviewed version exists

#### Key References from George's Work

**Sensory Processing & Neurodivergence:**
- Dunn, W. (1997, 2007) - Sensory Processing Framework
- Marco et al. (2011) - Sensory processing in ASD children
- Cascio et al. (2012) - Tactile perception in autism

**Digital Signal Processing:**
- Schroeder, M. R. (1962) - Colorless artificial reverberation
- Moorer, J. A. (1979) - Synthesis of music by computers
- Brown, C. P., & Duda, R. O. (1998) - Binaural sound synthesis

**Virtual Reality & Immersion:**
- Kim et al. (2021) - VR interventions for ASD
- Ringland et al. (2016) - Sensory sensitivities in virtual worlds
- Bradley and Newbutt (2022) - VR for autistic individuals

**Spatial Audio & Perception:**
- Mills, A. W. (1958) - Minimum audible angle
- Woodworth & Schlosberg (1954) - Experimental psychology
- Blauert, J. (1997) - Spatial Hearing

**Physical Modeling:**
- Karplus & Strong (1983) - Digital synthesis of plucked strings
- Smith, J. O. (2006, 2021) - Physical audio signal processing
- Bilbao, S. (2009) - Numerical sound synthesis

#### Citation Anti-Patterns to Avoid

❌ **Overcitation in obvious contexts**
- Don't cite basic facts: "Sound propagates through air [1]"

❌ **Citation required statements without citations**
- Never claim empirical facts without citation
- Never reference "studies show..." without specific citations

❌ **Circular self-citation**
- Cite your own work only when necessary for continuity
- Prioritize external validation over self-citation

❌ **Outdated sources when newer exist**
- Check if seminal papers have been updated or superseded
- Balance classic references with recent developments

❌ **Missing DOIs or incomplete references**
- Always include DOI when available
- Complete page numbers, volume/issue for journal articles

#### Example Citation Patterns

**Dense (Literature Review):**
```
Recent advances in binaural synthesis have focused on real-time HRTF
interpolation [1]–[4], head-tracking integration [5], [6], and perceptual
optimization [7]–[9]. While traditional approaches rely on large HRTF databases
[10], parametric models offer computational advantages [11], [12].
```

**Moderate (Methods):**
```
We implement the Brown-Duda structural model [15] for frequency-dependent ILD,
converting the analog prototype to digital IIR filters via bilinear transform [16].
ITD is computed using the Woodworth spherical head model [17].
```

**Sparse (Results):**
```
Figure 3 shows the measured frequency response. The 6 dB attenuation at 8 kHz
matches the predicted ILD for 90° azimuth [15], confirming the implementation.
```

**Reference Group (Discussion):**
```
Our perceptual results align with Mills' findings [18] on minimum audible angle
discrimination. The measured 2° threshold at frontal positions and 8° at lateral
positions closely match the classic psychoacoustic literature [18]–[20].
```

## Instrument Design Research Standards

### Design Documentation
- Document design rationale linking technical and artistic decisions
- Include sketches, CAD drawings, and prototypes in research portfolio
- Photograph all physical prototypes from multiple angles
- Record audio examples at different stages of development
- Maintain design journals with cultural and philosophical influences

### Historical and Cultural Context
- Research historical precedents for instrument types
- Document cultural practices and traditional playing techniques
- Include ethnographic research where applicable
- Cite musicological and organological literature
- Acknowledge cultural origins and avoid appropriation

### Design Philosophy
- Articulate aesthetic goals alongside technical specifications
- Discuss user experience and performer interaction
- Consider accessibility and inclusivity in design
- Address sustainability and material choices
- Document the relationship between form and function

### Technical Specifications for Instruments
- Frequency range and harmonic content
- Material properties: resonance, damping, density
- Physical dimensions with tolerances
- Manufacturing methods and reproducibility
- Tuning systems and temperament considerations

### Evaluation Criteria
- Technical performance metrics (frequency response, dynamic range)
- Playability and ergonomics (user testing with musicians)
- Aesthetic evaluation (peer review, audience response)
- Durability and longevity testing
- Cost-effectiveness and accessibility

### Interdisciplinary References
- Cite design theory literature (e.g., Norman, Bonsiepe)
- Reference art and aesthetics philosophy (e.g., Dewey, Scruton)
- Include musicology and organology sources
- Cross-reference cultural studies and anthropology
- Connect to philosophy of technology and embodiment

### Key Literature for Instrument Design
**Books:**
- "The Design of Everyday Things" - Donald Norman
- "Musical Instruments: History, Technology, and Performance" - Murray Campbell et al.
- "Sonic Experience: A Guide to Everyday Sounds" - Jean-François Augoyard
- "The Oxford Handbook of Sound Studies"
- "Handmade Electronic Music: The Art of Hardware Hacking" - Nicolas Collins

**Journals:**
- Organised Sound
- Computer Music Journal
- Journal of New Music Research
- Leonardo Music Journal
- Musical Instruments (journal)

## Signal Processing Standards

### Sampling and Resolution
- Always state sampling rate with units (e.g., 44.1 kHz, 48 kHz)
- Specify bit depth for audio (16-bit, 24-bit, 32-bit float)
- Include anti-aliasing filter specifications
- Document A/D and D/A converter specifications

### DSP Implementation
- Specify filter types: FIR vs IIR, order, cutoff frequencies
- Include frequency response plots (magnitude and phase)
- Report latency and computational complexity (FLOPs, memory)
- For real-time systems: report buffer sizes and processing time
- Use double precision for intermediate calculations, single for output

### Audio Quality Metrics
- Always include objective metrics: SNR, THD, RMSE, PESQ, POLQA
- For perceptual validation: listening tests with statistical analysis
- Report test conditions: headphones/speakers, room characteristics
- Include frequency response measurements ±1 dB tolerance

## Collaboration and Supervision

### NTNU
- Primary Supervisor: Peter Svensson (TTT4295 Acoustic Signal Processing)
- Share Overleaf projects for paper review
- Weekly progress reports recommended
- Follow NTNU thesis formatting guidelines

### AAU Collaboration
- Coordinate with AAU co-supervisors when applicable
- Align research outputs with both institutions' requirements
- Joint publications should acknowledge both institutions

### Meeting Documentation
- Maintain meeting notes with action items
- Track decisions and rationale in version control
- Document feedback and revisions to papers/code

## Professional Development

### Conference Presentations
- Prepare figures at high resolution for projectors (minimum 1920×1080)
- Practice timing: 12 min for 15 min slot, 18 min for 20 min slot
- Prepare backup PDF in addition to PowerPoint/Keynote
- Include QR codes to GitHub repos or supplementary materials

### Networking
- Maintain updated ResearchGate and Google Scholar profiles
- Share preprints on arXiv when appropriate
- Engage with research community on relevant platforms
- Respond professionally to peer review feedback

### Publication Strategy
- Aim for journal publications over conference papers for PhD
- Balance high-impact journals with timely publication
- Consider open-access options for broader reach
- Target 2-3 journal papers per year for PhD completion

## Computational Resources

### High-Performance Computing
- For large-scale simulations: use NTNU's IDUN cluster
- Document resource requirements: CPU hours, memory, storage
- Use job scripts for reproducibility
- Archive results with proper metadata

### Software Dependencies
- Pin exact versions in requirements.txt or environment.yml
- Use Docker/Singularity containers for complex dependencies
- Document system requirements and tested platforms
- Include installation troubleshooting in README

### Data Storage
- Backup strategy: 3-2-1 rule (3 copies, 2 media types, 1 offsite)
- Use NTNU network storage for institutional data
- Large datasets: consider Zenodo or institutional repository
- GDPR compliance for any human subject data

## Contact and Support

For questions about these guidelines or Claude integration:
- **PhD Candidate:** George Redpath
- **Email:** ghredpath@hotmail.com
- **Primary Institution:** NTNU Department of Electronic Systems
- **Supervisor:** Peter Svensson (TTT4295 Acoustic Signal Processing)
