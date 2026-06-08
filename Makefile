# --- Configuration ---
PYTHON       = python3
VENV_DIR     = .venv
VENV_ACTIVATE= $(VENV_DIR)/bin/activate
# For Windows compatibility (Git Bash/MSYS), swap the activate path
ifeq ($(OS),Windows_NT)
    VENV_ACTIVATE = $(VENV_DIR)/Scripts/activate
endif

# --- Phony Targets ---
.PHONY: all venv install test clean deep-clean help

# Default target
all: install test

help:
	@echo "Available commands:"
	@echo "  make venv       - Create the virtual environment"
	@echo "  make install    - Install the package in editable mode"
	@echo "  make test       - Run the unittest suite"
	@echo "  make clean      - Remove build and test caches"
	@echo "  make deep-clean - Remove caches AND the virtual environment"

# 1. Create Virtual Environment
venv: $(VENV_ACTIVATE)

$(VENV_ACTIVATE):
	@echo "=== Creating Virtual Environment ==="
	$(PYTHON) -m venv $(VENV_DIR)
	# Upgrade pip immediately inside the venv
	. $(VENV_ACTIVATE) && pip install --upgrade pip

# 2. Install Package in Editable Mode
install: $(VENV_ACTIVATE)
	@echo "=== Installing Package in Editable Mode ==="
	. $(VENV_ACTIVATE) && pip install -e .

# 3. Run the Unittest Suite
test: $(VENV_ACTIVATE)
	@echo "=== Running Tests ==="
	. $(VENV_ACTIVATE) && python -m unittest discover -s tests -v

# 4. Clean temporary Python files (Like cleaning .o and binary files in C)
clean:
	@echo "=== Cleaning Python Cache Files ==="
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf *.egg-info .pytest_cache

# 5. Nuke everything including the environment
deep-clean: clean
	@echo "=== Removing Virtual Environment ==="
	rm -rf $(VENV_DIR)
