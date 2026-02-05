# Costly Signaling ABM - Reproducibility Pipeline
# ================================================
#
# This Makefile reproduces all results from:
# "The Paradox of Monumental Architecture: An Agent-Based Model of
# Costly Signaling Under Resource Uncertainty"
#
# Lipo, Hunt (2026) Proceedings of the Royal Society B
#
# Quick Start:
#   make install    - Install the package
#   make figures    - Generate all figures (uses existing data)
#   make all        - Complete pipeline

.PHONY: help install figures data-quick data-full manuscript lint test clean verify all

# Default target
help:
	@echo ""
	@echo "Costly Signaling ABM - Reproducibility Pipeline"
	@echo "================================================"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Installation:"
	@echo "  install        Install package and dependencies"
	@echo "  venv           Create virtual environment and install"
	@echo ""
	@echo "Data Generation:"
	@echo "  data-quick     Generate validation data (~30 min)"
	@echo "  data-full      Full sensitivity analysis (~24-48 hours)"
	@echo ""
	@echo "Figure Generation:"
	@echo "  figures        Generate all 11 publication figures"
	@echo ""
	@echo "Quality Assurance:"
	@echo "  lint           Run ruff linter on source code"
	@echo "  test           Run unit tests"
	@echo "  verify         Verify installation and outputs"
	@echo ""
	@echo "Complete Pipeline:"
	@echo "  all            Install + generate figures"
	@echo "  reproduce-all  Full reproduction from scratch"
	@echo ""
	@echo "Utilities:"
	@echo "  clean          Remove generated files"
	@echo ""

# Create virtual environment
venv:
	@echo "Creating virtual environment..."
	python -m venv venv
	@echo "Activating and installing dependencies..."
	. venv/bin/activate && pip install --upgrade pip && pip install -e .
	@echo ""
	@echo "Virtual environment created. Activate with:"
	@echo "  source venv/bin/activate"

# Installation
install:
	@echo "Installing costly-signaling-abm package..."
	pip install -e .
	@echo "Installation complete."

# Quick data generation (~30 minutes)
data-quick:
	@echo "Generating validation data (estimated time: 30 minutes)..."
	python scripts/run_temporal_validation.py
	python scripts/run_parameter_sensitivity_validation.py
	@echo "Validation data generation complete."

# Full sensitivity analysis (~24-48 hours)
data-full:
	@echo "WARNING: Full sensitivity analysis takes 24-48 hours."
	@echo "Starting sensitivity analysis..."
	python -c "from costly.sensitivity_analysis import run_sensitivity_analysis; run_sensitivity_analysis()"
	@echo "Sensitivity analysis complete."

# Generate all publication figures
figures:
	@echo "Generating publication figures..."
	@echo ""
	@echo "Figure 2: Price Equation"
	python scripts/figure_generation/create_price_equation_figure.py
	@echo ""
	@echo "Figure 3: Modified Price Equation"
	python scripts/figure_generation/create_modified_price_equation.py
	@echo ""
	@echo "Figure 4: Model Dynamics"
	python scripts/figure_generation/create_figure_2_model_dynamics.py
	@echo ""
	@echo "Figures 5-7: Environmental Scenarios"
	python scripts/figure_generation/create_environmental_figures_moderate.py
	@echo ""
	@echo "Figures 8-11: Results and Case Study"
	python scripts/figure_generation/create_all_figures_colorblind.py
	@echo ""
	@echo "Figure 9: Validation"
	python scripts/figure_generation/create_price_equation_validation.py
	@echo ""
	@echo "Figure 10: Temporal Dynamics"
	python scripts/figure_generation/create_figure_10_temporal_dynamics.py
	@echo ""
	@echo "Figure generation complete. Check figures/final/"

# Run linter
lint:
	@echo "Running ruff linter..."
	ruff check src/ scripts/
	@echo "Linting complete."

# Run tests
test:
	@echo "Running tests..."
	pytest tests/ -v
	@echo "Tests complete."

# Verify installation
verify:
	@echo "Verifying installation..."
	@python -c "from costly import SpatialSimulation; print('Package import: OK')"
	@echo "Checking figures..."
	@ls figures/final/Figure_*.png 2>/dev/null | wc -l | xargs -I {} echo "Figures found: {}"
	@echo "Verification complete."

# Complete pipeline (quick)
all: install figures
	@echo ""
	@echo "================================================"
	@echo "Pipeline complete!"
	@echo "================================================"
	@echo ""
	@echo "Generated figures are in: figures/final/"

# Full reproduction from scratch
reproduce-all: install data-quick figures
	@echo ""
	@echo "================================================"
	@echo "Full reproduction complete!"
	@echo "================================================"

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	rm -f figures/final/*.png
	rm -f data/*.pkl
	rm -rf __pycache__ src/costly/__pycache__ scripts/__pycache__
	rm -rf .pytest_cache .ruff_cache
	@echo "Clean complete."
