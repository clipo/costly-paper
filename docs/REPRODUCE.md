# Reproducibility Guide

This guide explains how to reproduce all results from:

**"The Paradox of Monumental Architecture: An Agent-Based Model of Costly Signaling Under Resource Uncertainty"**

Lipo, C.P., DiNapoli, R.J., Hunt, T.L. (2026)

---

## Quick Start

If you just want to generate the figures using pre-existing data:

```bash
# Install the package
pip install -e .

# Generate all figures
make figures
```

This takes approximately 5-10 minutes and produces all 11 publication figures in `figures/final/`.

---

## System Requirements

### Hardware
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 5GB (mostly for sensitivity analysis data files)
- **CPU**: Any modern processor (simulation is CPU-bound)

### Software
- **Python**: 3.8 or higher
- **Operating System**: macOS, Linux, or Windows
- **Optional**: pandoc (for Word document generation)

### Python Dependencies
```
numpy>=1.21.0
matplotlib>=3.5.0
tqdm>=4.62.0
scipy>=1.7.0
python-docx>=0.8.11
```

---

## Installation

### Option 1: Using pip (recommended)

```bash
# Clone the repository
git clone https://github.com/clipo/costly-signaling-abm.git
cd costly-signaling-abm

# Install in development mode
pip install -e .
```

### Option 2: Using Make

```bash
make install
```

### Option 3: Virtual environment (cleanest)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e .
```

---

## Reproduction Workflows

### Workflow 1: Quick Reproduction (5-10 minutes)

Uses pre-generated data files to create all figures:

```bash
make figures
```

**What this does:**
- Generates all 11 publication figures
- Uses existing sensitivity analysis data in `data/`
- Outputs figures to `figures/final/`

### Workflow 2: Validation Data Reproduction (15-30 minutes)

Regenerates the validation data used in Figure 10 (panels E and F):

```bash
make data-quick
```

**What this does:**
- Runs temporal validation (1000 replicates, ~10 min)
- Runs parameter sensitivity validation (500 replicates, ~15 min)
- Saves results to `data/temporal_validation_results_*.pkl`
- Saves results to `data/parameter_sensitivity_results_*.pkl`

### Workflow 3: Full Reproduction (24-48 hours)

Regenerates all data from scratch, including the complete sensitivity analysis:

```bash
make reproduce-all
```

**What this does:**
1. Installs the package
2. Generates validation data (~30 min)
3. Runs full sensitivity analysis (~24-48 hours)
   - 208 parameter combinations
   - 50 replicates per combination
   - 10,400 total simulations
4. Generates all figures
5. Creates Word manuscript

**Note**: The full sensitivity analysis is computationally intensive. Consider running overnight or on a compute cluster.

---

## Data Files

### Pre-generated Data (in `data/`)

| File Pattern | Size | Purpose |
|--------------|------|---------|
| `sensitivity_analysis_results_*.pkl` | 760-850 MB | Main sensitivity analysis (10,400 sims) |
| `temporal_validation_results_*.pkl` | 250-520 KB | Temporal dynamics validation |
| `parameter_sensitivity_results_*.pkl` | 2-6 KB | Parameter sensitivity validation |

### Data → Figure Mapping

| Figure | Data Source | Generation Time |
|--------|-------------|-----------------|
| Figure 1 | External map file | N/A |
| Figures 2, 6-7 | None (conceptual diagrams) | ~5 seconds |
| Figures 3-5 | Generated deterministically | ~10 seconds |
| Figure 8 | `sensitivity_analysis_results_*.pkl` | ~1 min |
| Figure 9 | Validation data | ~1-2 min |
| Figure 10 | Live ABM simulation (100 replicates) | ~2-3 min |
| Figure 11 | Live ABM simulation | ~3 min |

---

## Figure Generation Scripts

All figure generation scripts are in `scripts/figure_generation/`:

| Figure | Script | Description |
|--------|--------|-------------|
| 2 | `create_price_equation_figure.py` | Price Equation for Multilevel Selection |
| 3-5 | `create_environmental_figures_moderate.py` | Frequency, Magnitude, Shortfall Scenarios |
| 6 | `create_modified_price_equation.py` | Modified Price Equation Framework |
| 7 | `create_figure_2_model_dynamics.py` | Model Dynamics Overview |
| 8 | `create_all_figures_colorblind.py` | Environmental Phase Space |
| 9 | `create_price_equation_validation.py` | Validation of Predictions |
| 10 | `create_figure_10_temporal_dynamics.py` | Temporal Dynamics (100 replicates) |
| 11 | `create_all_figures_colorblind.py` | Case Study Comparison |

### Master Figure Generation Script

To generate all figures at once:

```bash
python scripts/generate_all_figures.py
```

To generate specific figures:

```bash
python scripts/generate_all_figures.py --figures 3 4 5
```

To list all available figures:

```bash
python scripts/generate_all_figures.py --list
```

---

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    REPRODUCTION PIPELINE                     │
└─────────────────────────────────────────────────────────────┘

┌──────────┐     ┌─────────────┐     ┌──────────┐     ┌────────────┐
│ install  │────▶│ data-quick  │────▶│ figures  │────▶│ manuscript │
└──────────┘     └─────────────┘     └──────────┘     └────────────┘
    ~1 min          ~30 min            ~10 min           ~1 min
                       │
                       │ (optional)
                       ▼
               ┌─────────────┐
               │  data-full  │
               └─────────────┘
                  ~24-48 hrs
```

---

## Manuscript Generation

To convert the markdown manuscript to Word format:

```bash
make manuscript
```

This requires [pandoc](https://pandoc.org/installing.html) to be installed.

The manuscript source is at:
- `docs/manuscript/PAPER_DRAFT_THEORY_FIRST_EXPANDED.md`

The generated Word document will be at:
- `docs/manuscript/PAPER_DRAFT_THEORY_FIRST_EXPANDED.docx`

---

## Verifying Reproduction

After running the pipeline, verify your results:

### 1. Check Figure Count
```bash
ls -la figures/final/Figure_*.png | wc -l
# Should output: 11
```

### 2. Verify Figure Files
```bash
ls figures/final/Figure_*.png
```

Expected files:
- `Figure_1_Pacific_Overview_Map.png` - Pacific Overview Map
- `Figure_2_price_equation.png` - Price Equation for Multilevel Selection
- `Figure_3_frequency_comparison.png` - Frequency Comparison
- `Figure_4_magnitude_comparison.png` - Magnitude Comparison
- `Figure_5_shortfall_scenarios.png` - Combined Shortfall Scenarios
- `Figure_6_modified_price_equation.png` - Modified Price Equation Framework
- `Figure_7_model_dynamics.png` - Model Dynamics Overview
- `Figure_8_phase_space.png` - Environmental Phase Space
- `Figure_9_validation.png` - Validation of Predictions
- `Figure_10_temporal_dynamics.png` - Temporal Dynamics
- `Figure_11_case_study.png` - Case Study Comparison

### 3. Check Data Files
```bash
ls -la data/*.pkl
# Should show multiple .pkl files totaling ~3GB
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'costly'"

**Solution**: Install the package first:
```bash
pip install -e .
```

### "FileNotFoundError" when generating figures

**Solution**: Make sure you're running from the project root directory:
```bash
cd /path/to/costly-signaling-abm
make figures
```

### Figures look different from paper

**Possible causes**:
1. Different random seed (stochastic elements vary)
2. Different data file being used
3. Color scheme not applied

**Solution**: Use the latest data files and ensure colorblind-safe scripts are used.

### Out of memory during sensitivity analysis

**Solution**: Reduce the number of replicates or run on a machine with more RAM:
```python
# In sensitivity_analysis.py, reduce n_replicates
n_replicates = 5  # instead of 10
```

### pandoc not found

**Solution**: Install pandoc:
- macOS: `brew install pandoc`
- Ubuntu: `sudo apt install pandoc`
- Windows: Download from https://pandoc.org/installing.html

---

## Random Seeds and Reproducibility

All simulations use explicit random seeds for reproducibility:

- **Base seed**: `20260112` (date-based)
- **Validation scripts**: Seeds computed as `BASE_SEED + replicate * 1000 + condition_hash`
- **Sensitivity analysis**: Seeds vary by run number and parameter combination

Due to floating-point arithmetic differences across platforms, exact numerical results may vary slightly, but qualitative patterns (phase space structure, strategy dominance) should be identical.

---

## Contact

For questions about reproduction:
- Open an issue on GitHub
- Contact: Carl Lipo (Binghamton University)

---

## Citation

If you use this code, please cite:

```
Lipo, C.P., DiNapoli, R.J., Hunt, T.L. (2026). The Paradox of Monumental
Architecture: An Agent-Based Model of Costly Signaling Under Resource
Uncertainty. Journal of Archaeological Science (in review).
```
