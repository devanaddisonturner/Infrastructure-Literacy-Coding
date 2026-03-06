# Infrastructure Literacy Curriculum Coding

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://img.shields.io/badge/DOI-pending-blue.svg)]()

Three-layer systematic content analysis of construction career and technical education (CTE) curricula across four credentials in three national systems (United States, Australia, United Kingdom).

**Companion to:** Addison-Turner, D. C. (2026). Infrastructure Literacy: A Conceptual Framework for Understanding How Construction Career Students Think About Environmental Justice. *Environmental Education Research*.

## Key Finding

Across 344 individually coded learning outcomes from four construction credentials in three national systems, **zero outcomes** address environmental justice, community health equity, or the distributional consequences of infrastructure decisions. The absence is structural, not terminological.

## Three-Layer Design

| Layer | Method | Scope | Result |
|-------|--------|-------|--------|
| **Layer 0** | Binary keyword search | 15 primary EJ terms x 4 credentials | 0 of 60 |
| **Layer 1** | Near-synonym expansion | 30 additional terms x 4 credentials | 0 of 120 |
| **Layer 2** | Thematic audit | 344 individual learning outcomes x 3 binary criteria | 0 of 344 |

## Credentials Analyzed

| Credential | System | Coded Level | N |
|-----------|--------|-------------|---|
| NCCER Core Curriculum (6th ed.) | USA | Sub-Objective | 103 |
| CA CTE Building & Construction Standards | USA | Performance Indicator | 170 |
| CPC30220 Certificate III in Carpentry | Australia | Unit of Competency | 27 |
| City & Guilds 6706-23 Level 2 Diploma | UK | Learning Outcome | 44 |

## Quick Start

### Requirements

- Python 3.8 or higher
- openpyxl library

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

## Repository Structure

```
Infrastructure-Literacy-Coding/
  README.md                      This file
  LICENSE                        CC-BY-4.0
  CITATION.cff                   Citation metadata for Zenodo/GitHub
  requirements.txt               Python dependencies
  generate_coding_results.py     Main script (generates xlsx)
  data/
    layer2_outcomes.json          344 coded learning outcomes
    borderline_cases.json         8 borderline cases with justifications
  output/
    (generated xlsx saved here)
```

## Data Files

### `data/layer2_outcomes.json`

JSON array of 344 objects, each containing:

| Field | Type | Description |
|-------|------|-------------|
| `num` | int | Sequential row number (1-344) |
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
- **CPC30220:** Units of Competency (coarser than Element level; see Methodology sheet)
- **City & Guilds:** Learning Outcomes (finest grain available)

The zero-percent finding is invariant across granularity levels. Coding CPC30220 at Element level (~87 elements) would increase the denominator while maintaining the zero numerator.

## Replication

To independently verify these results:

1. Obtain the four credential documents (see Source Documents sheet in the generated xlsx or `SOURCE_DOCUMENTS` in the script).
2. Apply the three-criterion coding protocol to each learning outcome.
3. Compare your codes to `data/layer2_outcomes.json`.

The NCCER Core Curriculum requires institutional purchase. The other three credentials are publicly available at the URLs documented in the script.

## Citation

If you use this dataset or code, please cite:

```bibtex
@article{addisonturner2026infrastructure,
  author  = {Addison-Turner, Devan Cantrell},
  title   = {Infrastructure Literacy: A Conceptual Framework for
             Understanding How Construction Career Students Think
             About Environmental Justice},
  journal = {Environmental Education Research},
  year    = {2026},
}
```

## Contact

Devan Cantrell Addison-Turner
Stanford University, Doerr School of Sustainability
daddisonturner@stanford.edu
ORCID: [0000-0002-2511-3680](https://orcid.org/0000-0002-2511-3680)
