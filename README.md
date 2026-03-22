# Infrastructure Literacy Curriculum Coding

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18893500.svg)](https://doi.org/10.5281/zenodo.18893500)

Three-layer systematic content analysis of construction career and technical education (CTE) curricula across four credentials in three national systems (United States, Australia, United Kingdom). Also includes the reproducible generation script for **Figure 1: Conceptual Model of Infrastructure Literacy**.

**Companion to:** Addison-Turner, D. C. (2026). Infrastructure Literacy: A Conceptual Framework for Understanding How Construction Career Students Think About Environmental Justice. *Journal of Vocational Education and Training*.

## Key Finding

Across 431 individually coded learning outcomes from four construction credentials in three national systems, **zero outcomes** address environmental justice, community health equity, or the distributional consequences of infrastructure decisions. The absence is structural, not terminological.

## Three-Layer Design

| Layer | Method | Scope | Result |
|-------|--------|-------|--------|
| **Layer 0** | Binary keyword search | 15 primary EJ terms x 4 credentials | 0 of 60 |
| **Layer 1** | Near-synonym expansion | 30 additional terms x 4 credentials | 0 of 120 |
| **Layer 2** | Thematic audit | 431 individual learning outcomes x 3 binary criteria | 0 of 431 |

## Credentials Analyzed

| Credential | System | Coded Level | N |
|-----------|--------|-------------|---|
| NCCER Core Curriculum (6th ed.) | USA | Sub-Objective | 103 |
| CA CTE Building & Construction Standards | USA | Performance Indicator | 170 |
| CPC30220 Certificate III in Carpentry | Australia | Element of Competency | 114 |
| City & Guilds 6706-23 Level 2 Diploma | UK | Learning Outcome | 44 |

## Quick Start

### Requirements

- Python 3.8 or higher
- `openpyxl` — coding workbook generation
- `matplotlib`, `numpy`, `Pillow` — Figure 1 generation

Install all at once:
```
pip install -r requirements.txt
```

### No Code Required

If you just want to view the coding data, open `output/EJT_Binary_Coding_Results.xlsx` in Excel. No Python installation needed.

---

### Windows Setup

**Step 1: Install Python (if not already installed)**

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python 3 installer for Windows
3. Run the installer — **check "Add Python to PATH"** at the bottom of the first screen
4. Click "Install Now"

**Step 2: Download this repository**

Option A (zip): Click the green "Code" button on GitHub, then "Download ZIP". Unzip to a folder you can find easily (e.g., `C:\Users\YourName\Desktop\Infrastructure-Literacy-Coding`).

**Alternative: Windows PowerShell**

PowerShell is built into all modern Windows versions (press Win + X → Windows PowerShell):
```
cd $env:USERPROFILE/Downloads/Infrastructure-Literacy-Coding
python generate_coding_results.py
```

Option B (git):
```
git clone https://github.com/daddisonturner/Infrastructure-Literacy-Coding.git
```

**Step 3: Install the dependency**

Open Command Prompt (search "cmd" in Start menu) and type:
```
pip install openpyxl
```

**Step 4: Run the script**

Option A — IDLE (Python's built-in editor):
1. Navigate to the repository folder in File Explorer
2. Right-click `generate_coding_results.py` → "Edit with IDLE"
3. Press F5 (or Run > Run Module)
4. Output appears in `output/EJT_Binary_Coding_Results.xlsx`

Option B — Command Prompt:
```
cd C:\Users\YourName\Desktop\Infrastructure-Literacy-Coding
python generate_coding_results.py
```

Option C — IDLE Shell (>>> prompt):
```python
>>> import os; os.chdir(r"C:\Users\YourName\Desktop\Infrastructure-Literacy-Coding")
>>> exec(open("generate_coding_results.py").read())
```

Option D — R / RStudio:
```r
source("run_in_r.R")   # loads helper functions
run_method_a()         # runs generate_coding_results.py via system()
```

---

### macOS Setup

**Step 1: Install Python (if not already installed)**

macOS includes Python 2 but not Python 3. Install Python 3:

Option A (recommended): Go to [python.org/downloads](https://www.python.org/downloads/) and download the macOS installer.

Option B (Homebrew):
```
brew install python3
```

**Step 2: Download this repository**

Option A (zip): Click the green "Code" button on GitHub, then "Download ZIP". Unzip to a folder (e.g., your Desktop).

Option B (git):
```
git clone https://github.com/daddisonturner/Infrastructure-Literacy-Coding.git
```

**Step 3: Install the dependency**

Open Terminal (Applications > Utilities > Terminal) and type:
```
pip3 install openpyxl
```

**Step 4: Run the script**

Option A — IDLE:
1. Open IDLE (search "IDLE" in Spotlight or find it in Applications > Python 3.x)
2. File > Open > navigate to the repository folder > select `generate_coding_results.py`
3. Press F5 (or Run > Run Module)
4. Output appears in `output/EJT_Binary_Coding_Results.xlsx`

Option B — Terminal:
```
cd ~/Desktop/Infrastructure-Literacy-Coding
python3 generate_coding_results.py
```

Option C — IDLE Shell (>>> prompt):
```python
>>> import os; os.chdir(os.path.expanduser("~/Desktop/Infrastructure-Literacy-Coding"))
>>> exec(open("generate_coding_results.py").read())
```

Option D — R / RStudio (macOS or Windows):
```r
source("run_in_r.R")   # loads helper functions
run_method_a()         # runs Python via system() — no extra R packages needed
outcomes <- load_outcomes_in_r()  # load 431 outcomes directly into R (no Python needed)
```
See `run_in_r.R` for full documentation of all three R methods.

---

### Changing Settings

To toggle between blinded and unblinded output, edit the `CONFIGURATION` section near the top of `generate_coding_results.py`:

```python
UNBLINDED = False  # ← Change to True for unblinded output
CODER_NAME = "Devan Cantrell Addison-Turner"  # ← Change to your name
```

Or use command line flags (Command Prompt / Terminal only):
```
python generate_coding_results.py --unblinded
python generate_coding_results.py --unblinded --coder "Your Name"
python generate_coding_results.py --output custom_filename.xlsx
```

### From Another Python Script or Jupyter Notebook

```python
from generate_coding_results import main
main(output_file="results.xlsx", unblinded=True, coder_name="Your Name")
```

Output is saved to `output/EJT_Binary_Coding_Results.xlsx`.

## Figure 1 Generation

`generate_figure1.py` produces the conceptual model diagram in three formats.

### Quick start

```
python generate_figure1.py
```

Outputs are saved to `figures/`:

| File | Format | Use |
|------|--------|-----|
| `Figure1_Infrastructure_Literacy_Model.png` | PNG, 300 DPI | Journal submission |
| `Figure1_Infrastructure_Literacy_Model.svg` | SVG, vector | Editing / scaling |
| `Figure1_Infrastructure_Literacy_Model.jpg` | JPEG, 300 DPI | Supplementary |

### Options

```
python generate_figure1.py --output-dir ./figures   # default
python generate_figure1.py --grayscale-test         # also save grayscale proof
```

### Tests

```
python test_generate_figure1.py      # standalone
python -m pytest test_generate_figure1.py -v
```

The test suite (27 tests) verifies file existence, dimensions, DPI, SVG validity, grayscale differentiation, geometric correctness, and idempotency.

### Makefile shortcuts

```
make figure             # PNG + SVG + JPG
make figure-grayscale   # also grayscale proof
make coding             # EJT coding workbook
make all                # figure + coding + tests
make install            # install all dependencies
```

## Repository Structure

```
Infrastructure-Literacy-Coding/
  README.md                        This file
  LICENSE                          CC-BY-4.0
  CITATION.cff                     Citation metadata for Zenodo/GitHub
  Makefile                         Shortcuts for all generation tasks
  requirements.txt                 Python dependencies (all scripts)
  generate_coding_results.py       Generates EJT coding workbook (xlsx)
  generate_figure1.py              Generates Figure 1 (PNG/SVG/JPG)
  test_generate_figure1.py         Test suite for Figure 1 script
  data/
    layer2_outcomes.json            431 coded learning outcomes
    borderline_cases.json           8 borderline cases with justifications
  figures/
    (generated figure files saved here)
  output/
    (generated xlsx saved here)
```

## Data Files

### `data/layer2_outcomes.json`

JSON array of 431 objects, each containing:

| Field | Type | Description |
|-------|------|-------------|
| `num` | int | Sequential row number (1-431) |
| `credential` | string | Source credential name |
| `unit` | string | Module/unit within credential |
| `outcome_id` | string | Official outcome identifier |
| `description` | string | Full text of the learning outcome |
| `crit_a` | int (0/1) | Distributional consequences criterion |
| `crit_b` | int (0/1) | Community health equity criterion |
| `crit_c` | int (0/1) | Environmental justice concepts criterion |
| `result` | string | "Present" or "Absent" |
| `notes` | string | Coder notes (borderline justifications) |

### `data/borderline_cases.json`

JSON array of 8 objects documenting outcomes that required explicit coding justification (e.g., environmental regulations mentioned in compliance-only contexts).

## Coding Protocol

Each learning outcome was independently evaluated against three binary criteria:

1. **Criterion A (Distributional Burdens):** Does this outcome require learners to evaluate distributional consequences of infrastructure decisions?
2. **Criterion B (Community Health Equity):** Does this outcome address community health in an equity framework (beyond occupational safety)?
3. **Criterion C (Environmental Justice):** Does this outcome engage environmental justice concepts, even implicitly?

**Decision rule:** "Present" if any criterion is met (A OR B OR C). "Absent" if none are met.

## Granularity Note

The four credentials use different structural hierarchies. Each was coded at the level its governing body defines as the fundamental learning outcome:

- **NCCER:** Sub-Objectives (finest grain available)
- **CA CTE:** Performance Indicators (finest grain available)
- **CPC30220:** Elements of Competency (114 elements across 27 core units; extracted from official unit PDFs on training.gov.au, March 2026)
- **City & Guilds:** Learning Outcomes (finest grain available)

The zero-percent finding is invariant across granularity levels. All four credentials are coded at their respective sub-unit structural level.

## Replication

To independently verify these results:

1. Obtain the four credential documents (see Source Documents sheet in the generated xlsx or `SOURCE_DOCUMENTS` in the script).
2. Apply the three-criterion coding protocol to each learning outcome.
3. Compare your codes to `data/layer2_outcomes.json`.

The NCCER Core Curriculum requires institutional purchase. The other three credentials are publicly available at the URLs documented in the script.


## Replication — Keyword Search Verification

To independently verify the zero-percent finding:

### Step 1 — Download source credential documents (first time only)
```
python3 download_irr_source_documents.py        # macOS / Linux
python  download_irr_source_documents.py        # Windows Command Prompt
python  download_irr_source_documents.py        # Windows PowerShell
```
Downloads the three publicly available credential PDFs (CA CTE, CPC30220, City & Guilds)
and produces a verification archive. NCCER requires institutional purchase (see script header).

### Step 2 — Run keyword search replication
```
python3 replicate_keyword_search.py             # macOS / Linux
python  replicate_keyword_search.py             # Windows
```
Searches all 45 terms (15 primary + 30 near-synonym) across all four credentials and
compares results against the primary coding. Expected output: 0 discrepancies, 0% confirmed.

### Options
```
python3 replicate_keyword_search.py --credential A          # single credential
python3 replicate_keyword_search.py --layer 0               # Layer 0 only
python3 replicate_keyword_search.py --credential C --layer 1
python3 download_irr_source_documents.py --search-only      # skip download
```

### Run from R
```r
source("run_in_r.R")
run_method_a()                    # full replication via system()
run_method_a(credential = "B")   # single credential
run_method_b()                    # via reticulate (Python in-process)
outcomes <- load_outcomes_in_r()  # load 431 outcomes into R data frame (no Python)
```

> **IDLE users:** See the Usage section in each script's header for step-by-step IDLE instructions.

### Makefile shortcuts
```
make download          # download source PDFs
make replicate         # run keyword search
make replicate-search-only  # search only, no download
```

## Citation

If you use this dataset or code, please cite:

```bibtex
@article{addisonturner2026infrastructure,
  author  = {Addison-Turner, Devan Cantrell},
  title   = {Infrastructure Literacy: A Conceptual Framework for
             Understanding How Construction Career Students Think
             About Environmental Justice},
  journal = {Journal of Vocational Education and Training},
  year    = {2026},
}
```

## Contact

Devan Cantrell Addison-Turner
Stanford University, Doerr School of Sustainability
daddisonturner@stanford.edu
ORCID: [0000-0002-2511-3680](https://orcid.org/0000-0002-2511-3680)
