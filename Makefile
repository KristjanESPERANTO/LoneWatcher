# Find Python files
PYTHON_FILES := $(shell git ls-files "*.py" "*.pyw")

lint:
	@if [ "$(PYTHON_FILES)" != "" ]; then \
		pylint $(PYTHON_FILES); \
	else \
		echo "No Python files found in git"; \
	fi
