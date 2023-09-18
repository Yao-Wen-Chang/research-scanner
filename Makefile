VENV_NAME = myenv
PYTHON = python3
VENV_DIR = .venv





# Check if the virtual environment exists
ifeq ($(wildcard $(VENV_DIR)/bin/activate),)
  VENV_EXISTS = 0
else
  VENV_EXISTS = 1
endif


# Set up the virtual environment if it doesn't exist
.PHONY: venv
venv:
ifeq ($(VENV_EXISTS),0)
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created in $(VENV_DIR)"
else
	@echo "Virtual environment $(VENV_DIR) already exists."
endif

# Install project dependencies into the virtual environment
.PHONY: install
install: venv
	@echo "Installing dependencies..."
	@$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "Dependencies installed."

# Clean up the virtual environment
.PHONY: clean
clean: 
	@echo "Removing virtual environment..."
	@rm -rf $(VENV_DIR) 
	@find . -type f -name *.pyc -delete
	@find . -type d -name __pycache__ -delete
	@echo "Virtual environment removed."