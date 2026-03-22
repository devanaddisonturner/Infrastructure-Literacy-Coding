##############################################################################
# run_in_r.R
##############################################################################
#
# Infrastructure Literacy Credential Content Analysis
# R Runner — runs the Python replication scripts from within R
#
# Author:  Devan Cantrell Addison-Turner
#          PhD Candidate, Civil and Environmental Engineering
#          Stanford Doerr School of Sustainability, Stanford University
#          Natural Capital Alliance | Lepech Research Group |
#          Center for Integrated Facility Engineering (CIFE)
#          daddisonturner@stanford.edu
#          ORCID: 0000-0002-2511-3680
#
# Study:   "Infrastructure Literacy: A Conceptual Framework for Understanding
#           How Construction Career Students Think About Environmental Justice"
#           Manuscript submitted to Journal of Vocational Education and Training
#
# Data:    https://github.com/devanaddisonturner/Infrastructure-Literacy-Coding
# Zenodo:  https://doi.org/10.5281/zenodo.18893500 (v1.0.2)
# IRB:     Stanford IRB Protocol #84369
# Trial:   ClinicalTrials.gov NCT07315919
#
# Purpose
# -------
# This script provides three ways to run the Infrastructure Literacy
# replication analysis from within R:
#
#   Method A — system() call (simplest, no extra packages)
#              Calls Python directly. Use this if you just want to run
#              the replication and see terminal output.
#
#   Method B — reticulate (run Python in-process, load results into R)
#              Use this if you want to analyse the coded data in R after
#              running, or integrate replication into an R workflow.
#
#   Method C — load data directly in R (no Python needed)
#              Reads layer2_outcomes.json directly into R using jsonlite.
#              Use this if you only need the coded data for analysis and
#              do not need to run the keyword search replication.
#
# Requirements
# ------------
#   Method A: R 4.0+, Python 3.6+ installed and accessible
#   Method B: R 4.0+, reticulate package, Python 3.6+ with pypdf + openpyxl
#   Method C: R 4.0+, jsonlite package (no Python needed)
#
# Usage
# -----
#   Open this file in RStudio or R and run the section you need.
#   Or source the whole file: source("run_in_r.R")
#
# Install required R packages (run once):
#   install.packages(c("jsonlite", "reticulate"))
#
##############################################################################


# ── CONFIGURATION ─────────────────────────────────────────────────────────────
# Set this to the path of your repository folder if running from a different
# working directory. Leave as "." if running from within the repo.

REPO_DIR <- "."


# ==============================================================================
# METHOD A — system() call (simplest, recommended for most users)
# ==============================================================================
# Calls Python directly from R using system(). No extra R packages needed.
# Output prints to the R console.
#
# To run: select these lines and press Ctrl+Enter (or Cmd+Enter on Mac)

run_method_a <- function(credential = "all", layer = "both", search_only = FALSE) {

  # Detect Python command (python3 on Mac/Linux, python on Windows)
  python_cmd <- if (.Platform$OS.type == "windows") "python" else "python3"

  # Check Python is available
  python_check <- system(paste(python_cmd, "--version"), ignore.stdout = FALSE)
  if (python_check != 0) {
    stop("Python not found. Install Python 3 from https://www.python.org/downloads/")
  }

  # Validate and set working directory to repo
  if (!dir.exists(REPO_DIR)) {
    stop("Repository folder not found: '", REPO_DIR,
         "'\nSet REPO_DIR at the top of this script to the correct path.")
  }
  old_wd <- setwd(REPO_DIR)
  on.exit(setwd(old_wd))

  if (search_only) {
    # Download script with --search-only flag
    cat("Running: download_irr_source_documents.py --search-only\n\n")
    system(paste(python_cmd, "download_irr_source_documents.py --search-only"))
  } else {
    # Replicate keyword search
    args <- character(0)
    if (credential != "all") args <- c(args, paste("--credential", credential))
    if (layer      != "both") args <- c(args, paste("--layer", layer))
    cmd <- paste(python_cmd, "replicate_keyword_search.py", paste(args, collapse = " "))
    cat("Running:", cmd, "\n\n")
    system(cmd)
  }
}

# ── Quick-run examples (uncomment to execute) ──────────────────────────────

# Run full replication (all 4 credentials, both Layer 0 and Layer 1):
# run_method_a()

# Run Layer 0 only (15 primary EJ terms):
# run_method_a(layer = "0")

# Run a single credential:
# run_method_a(credential = "A")   # NCCER (JSON only — institutional purchase required)
# run_method_a(credential = "B")   # CA CTE (PDF)
# run_method_a(credential = "C")   # CPC30220 (PDF + 27 unit PDFs)
# run_method_a(credential = "D")   # City & Guilds (PDF)

# Run keyword search only (no download):
# Note: requires EJT_Binary_Coding_Results_v6.xlsx in REPO_DIR
# run_method_a(search_only = TRUE)


# ==============================================================================
# METHOD B — reticulate (run Python in-process, results available in R)
# ==============================================================================
# Runs Python inside R using the reticulate package. Replication output
# prints to the R console. Use Method C to load outcome data into R.
#
# First install: install.packages("reticulate")
# Then install Python deps: reticulate::py_install(c("pypdf", "openpyxl"))

run_method_b <- function(credential = "all", layer = "both") {

  if (!requireNamespace("reticulate", quietly = TRUE)) {
    stop("Package 'reticulate' is required. Install with: install.packages('reticulate')")
  }

  library(reticulate)

  # Check Python is configured
  if (!py_available()) {
    message("Python not configured. Attempting to find Python...")
    use_python(Sys.which(if (.Platform$OS.type == "windows") "python" else "python3"),
               required = TRUE)
  }

  # Install Python dependencies if needed
  tryCatch({
    py_import("pypdf")
  }, error = function(e) {
    message("pypdf not found — installing...")
    py_install("pypdf")
  })

  tryCatch({
    py_import("openpyxl")
  }, error = function(e) {
    message("openpyxl not found — installing...")
    py_install("openpyxl")
  })

  # Validate and set working directory to repo
  if (!dir.exists(REPO_DIR)) {
    stop("Repository folder not found: '", REPO_DIR,
         "'\nSet REPO_DIR at the top of this script to the correct path.")
  }
  old_wd <- setwd(REPO_DIR)
  on.exit(setwd(old_wd))

  # Source the replicate script
  cat("Loading replicate_keyword_search.py via reticulate...\n\n")

  # Set sys.argv to pass flags
  sys <- import("sys")
  args <- c("replicate_keyword_search.py")
  if (credential != "all") args <- c(args, "--credential", credential)
  if (layer      != "both") args <- c(args, "--layer", layer)
  sys$argv <- args

  # Run the script
  source_python("replicate_keyword_search.py")

  cat("\nDone. Replication output printed above.\n")
  cat("To load the coded data into R as a data frame, use Method C:\n")
  cat("  outcomes <- load_outcomes_in_r()\n")
}

# ── Quick-run examples (uncomment to execute) ──────────────────────────────

# Full replication:
# run_method_b()

# Single credential:
# run_method_b(credential = "B")


# ==============================================================================
# METHOD C — load data directly in R (no Python needed)
# ==============================================================================
# Reads layer2_outcomes.json directly into an R data frame using jsonlite.
# Use this to analyse the coded data in R without running any Python.
#
# First install: install.packages("jsonlite")

load_outcomes_in_r <- function(repo_dir = REPO_DIR) {

  if (!requireNamespace("jsonlite", quietly = TRUE)) {
    stop("Package 'jsonlite' is required. Install with: install.packages('jsonlite')")
  }

  library(jsonlite)

  json_path <- file.path(repo_dir, "data", "layer2_outcomes.json")
  if (!file.exists(json_path)) {
    stop("layer2_outcomes.json not found at: ", json_path,
         "\nMake sure REPO_DIR is set to the repository folder.")
  }

  outcomes <- fromJSON(json_path)

  # Summary
  cat("Loaded", nrow(outcomes), "learning outcomes\n\n")
  cat("Outcomes by credential:\n")
  print(table(outcomes$credential))
  cat("\nAll results absent:", all(outcomes$result == "Absent"), "\n")
  cat("Any criteria met:  ", any(outcomes$crit_a | outcomes$crit_b | outcomes$crit_c), "\n\n")

  invisible(outcomes)
}

# ── Quick-run examples (uncomment to execute) ──────────────────────────────

# Load outcomes into R data frame:
# outcomes <- load_outcomes_in_r()

# Then analyse in R:
# table(outcomes$credential)                           # counts by credential
# outcomes[outcomes$credential == "CPC30220 (Australia)", ]  # CPC30220 rows
# outcomes[outcomes$result == "Present", ]             # should be empty (zero finding)

# Filter to a single credential:
# nccer <- subset(outcomes, credential == "NCCER Core (6th ed., USA)")
# head(nccer[, c("outcome_id", "description")])


# ==============================================================================
# LOAD BORDERLINE CASES
# ==============================================================================
# The 8 borderline cases that required explicit coding justification.

load_borderline_cases <- function(repo_dir = REPO_DIR) {

  if (!requireNamespace("jsonlite", quietly = TRUE)) {
    stop("Package 'jsonlite' is required. Install with: install.packages('jsonlite')")
  }

  library(jsonlite)

  bc_path <- file.path(repo_dir, "data", "borderline_cases.json")
  if (!file.exists(bc_path)) {
    stop("borderline_cases.json not found at: ", bc_path)
  }

  bc <- fromJSON(bc_path)
  cat("Loaded", NROW(bc), "borderline cases\n")
  invisible(bc)
}

# borderline <- load_borderline_cases()


# ==============================================================================
# QUICK REFERENCE
# ==============================================================================
cat("
Infrastructure Literacy — R Runner loaded.

Method A (system call, simplest):
  run_method_a()                     # full replication
  run_method_a(credential = 'B')     # single credential
  run_method_a(layer = '0')          # Layer 0 only
  run_method_a(search_only = TRUE)   # keyword search, no download

Method B (reticulate, in-process):
  run_method_b()                     # full replication via reticulate (output to console)

Method C (data only, no Python):
  outcomes <- load_outcomes_in_r()   # load 431 outcomes into R data frame
  borderline <- load_borderline_cases()  # load 8 borderline case justifications

Required packages:
  install.packages(c('jsonlite', 'reticulate'))
")
