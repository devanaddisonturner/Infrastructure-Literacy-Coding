.PHONY: all figure figure-grayscale coding test pytest clean lint install help

PYTHON     ?= python3
FIGURE_DIR ?= figures
FIG_SCRIPT  = generate_figure1.py
FIG_TESTS   = test_generate_figure1.py
FIG_BASE    = Figure1_Infrastructure_Literacy_Model
COD_SCRIPT  = generate_coding_results.py
COD_OUTPUT  = output/EJT_Binary_Coding_Results.xlsx

# Default: generate both outputs + run tests
all: figure coding test

# ── Figure 1 ────────────────────────────────────────────────

# Generate all Figure 1 variants (PNG, SVG, JPG)
figure:
	$(PYTHON) $(FIG_SCRIPT) --output-dir $(FIGURE_DIR)

# Generate with grayscale verification
figure-grayscale:
	$(PYTHON) $(FIG_SCRIPT) --output-dir $(FIGURE_DIR) --grayscale-test

# ── Coding workbook ─────────────────────────────────────────

# Generate EJT Binary Coding Results workbook
coding:
	$(PYTHON) $(COD_SCRIPT)

# Generate unblinded workbook (includes coder name)
coding-unblinded:
	$(PYTHON) $(COD_SCRIPT) --unblinded

# ── Tests ───────────────────────────────────────────────────

# Run Figure 1 test suite (standalone)
test:
	$(PYTHON) $(FIG_TESTS)

# Run tests with pytest (if installed)
pytest:
	$(PYTHON) -m pytest $(FIG_TESTS) -v

# ── Code quality ────────────────────────────────────────────

# Basic syntax/style check
lint:
	$(PYTHON) -c "\
	import ast, sys; \
	for f in ['$(FIG_SCRIPT)', '$(COD_SCRIPT)']: \
	    src = open(f).read(); ast.parse(src); \
	    lines = src.split('\n'); \
	    issues = [f'L{i+1}: {len(l)} chars' for i, l in enumerate(lines) if len(l.rstrip()) > 88]; \
	    print(f'{f}: syntax OK, long lines: {len(issues)}' if issues else f'{f}: OK'); \
	    [print(f'  {x}') for x in issues]; \
	sys.exit(0)"

# ── Housekeeping ────────────────────────────────────────────

# Remove all generated outputs
clean:
	rm -f $(FIGURE_DIR)/$(FIG_BASE).png
	rm -f $(FIGURE_DIR)/$(FIG_BASE).svg
	rm -f $(FIGURE_DIR)/$(FIG_BASE).jpg
	rm -f $(FIGURE_DIR)/$(FIG_BASE)_grayscale.png
	rm -f $(COD_OUTPUT)
	rm -rf __pycache__

# Install all dependencies
install:
	$(PYTHON) -m pip install -r requirements.txt

help:
	@echo "Targets:"
	@echo "  make                 Generate figure + coding workbook + run tests"
	@echo "  make figure          Generate Figure 1 (PNG, SVG, JPG)"
	@echo "  make figure-grayscale  Also generate grayscale verification image"
	@echo "  make coding          Generate EJT coding workbook (blinded)"
	@echo "  make coding-unblinded  Generate workbook with coder name"
	@echo "  make test            Run Figure 1 test suite"
	@echo "  make pytest          Run tests via pytest"
	@echo "  make lint            Basic syntax/style check"
	@echo "  make clean           Remove all generated files"
	@echo "  make install         Install Python dependencies"
	@echo ""
	@echo "Options:"
	@echo "  FIGURE_DIR=./dir     Set figure output directory (default: figures)"
	@echo "  PYTHON=python3.x     Set Python interpreter"

# ── Replication ───────────────────────────────────────────────────────────────
.PHONY: download replicate

download:  ## Download source credential PDFs and run keyword search replication
	python3 download_irr_source_documents.py

replicate:  ## Run keyword search replication against downloaded PDFs
	python3 replicate_keyword_search.py

replicate-search-only:  ## Run keyword search only (no download, requires spreadsheet)
	python3 download_irr_source_documents.py --search-only

r-replicate:  ## Run keyword search replication from R (requires R + run_in_r.R)
	Rscript -e "source('run_in_r.R'); run_method_a()"

r-data:  ## Load outcome data into R and print summary
	Rscript -e "source('run_in_r.R'); outcomes <- load_outcomes_in_r()"
