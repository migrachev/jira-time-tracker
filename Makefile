.PHONY: install lint test run clean

# Set the Python interpreter and venv directory
PYTHON = python
VENV_DIR = venv
ACTIVATE = source $(VENV_DIR)/bin/activate

# Default target: install dependencies
install:
	$(PYTHON) -m venv $(VENV_DIR)
	$(ACTIVATE) && pip install -U pip && pip install -r requirements.txt

# Run code linter
lint:
	$(ACTIVATE) && flake8 src/

# Run tests
test:
	$(ACTIVATE) && pytest tests/

# Run the main script
run:
	$(ACTIVATE) && $(PYTHON) src/log_time/main.py

# Remove venv and __pycache__
clean:
	rm -rf $(VENV_DIR) __pycache__ */__pycache__ .pytest_cache