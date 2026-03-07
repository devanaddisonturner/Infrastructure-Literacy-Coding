.PHONY: all figure figure-grayscale test pytest clean lint install help

PYTHON ?= python3
OUTPUT_DIR ?= .
SCRIPT = generate_figure1.py
TESTS = test_generate_figure1.py
BASENAME = Figure1_Infrastructure_Literacy_Model

# Default target: generate figure + run tests
all: figure test

# Generate all figure variants (PNG, SVG, JPG)
figure:
	$(PYTHON) $(SCRIPT) --output-dir $(OUTPUT_DIR)

# Generate with grayscale verification
figure-grayscale:
	$(PYTHON) $(SCRIPT) --output-dir $(OUTPUT_DIR) --grayscale-test

# Run test suite
test:
	$(PYTHON) $(TESTS)

# Run tests with pytest (if installed)
pytest:
	$(PYTHON) -m pytest $(TESTS) -v

# Lint with basic checks
lint:
	$(PYTHON) -c "\
	import ast, sys; \
	f = open('$(SCRIPT)'); src = f.read(); f.close(); \
	ast.parse(src); \
	lines = src.split('\n'); \
	issues = []; \
	[issues.append(f'L{i+1}: {len(l)} chars') for i, l in enumerate(lines) if len(l.rstrip()) > 88]; \
	print('Syntax: OK'); \
	print(f'Long lines: {len(issues)}' if issues else 'Line length: OK'); \
	[print(f'  {x}') for x in issues]; \
	sys.exit(1 if issues else 0)"

# Remove generated outputs
clean:
	rm -f $(OUTPUT_DIR)/$(BASENAME).png
	rm -f $(OUTPUT_DIR)/$(BASENAME).svg
	rm -f $(OUTPUT_DIR)/$(BASENAME).jpg
	rm -f $(OUTPUT_DIR)/$(BASENAME)_grayscale.png
	rm -rf __pycache__

# Install dependencies
install:
	$(PYTHON) -m pip install -r requirements.txt

help:
	@echo "Targets:"
	@echo "  make              Generate figure + run tests"
	@echo "  make figure       Generate PNG, SVG, JPG"
	@echo "  make figure-grayscale  Also generate grayscale"
	@echo "  make test         Run test suite"
	@echo "  make pytest       Run tests via pytest"
	@echo "  make lint         Basic syntax/style check"
	@echo "  make clean        Remove generated files"
	@echo "  make install      Install Python dependencies"
	@echo ""
	@echo "Options:"
	@echo "  OUTPUT_DIR=./dir  Set output directory"
	@echo "  PYTHON=python3.x  Set Python interpreter"
