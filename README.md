# The Paradox of Monumental Architecture

**An Agent-Based Model of Costly Signaling Under Resource Uncertainty**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the complete simulation framework and reproducibility package for:

> **Lipo, C.P. & Hunt, T.L. (2026).** The Paradox of Monumental Architecture: An Agent-Based Model of Costly Signaling Under Resource Uncertainty. *Proceedings of the Royal Society B* (in review).

## Quick Start

```bash
# Clone and install
git clone https://github.com/clipo/costly-paper.git
cd costly-paper
pip install -e .

# Generate all 11 publication figures
make figures
```

## Overview

This agent-based model explores how environmental uncertainty shapes costly signaling strategies (monument building) versus demographic maximization in Polynesian societies. The model uses the Price equation to formalize when costly signaling evolves at the group level despite individual-level costs.

### Key Findings

- **Phase space structure**: Clear environmental zones where different strategies dominate
- **Demographic paradox resolved**: Lower populations can be adaptive when environmental uncertainty makes conflict reduction more valuable than demographic maximization
- **Rapa Nui vs. Rapa Iti**: Environmental differences predict divergent outcomes in monument building
- **Theoretical validation**: ABM results align with Price equation predictions (r = 0.969)

## Installation

### Option 1: Direct Install

```bash
pip install -e .
```

### Option 2: Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

### Option 3: Using Make

```bash
make venv
source venv/bin/activate
```

## Reproducing Results

### Generate Figures (~10 minutes)

```bash
make figures
```

This generates all 11 publication figures in `figures/final/`.

### Generate Validation Data (~30 minutes)

```bash
make data-quick
```

### Full Sensitivity Analysis (~24-48 hours)

```bash
make data-full
```

This runs 10,400 simulations across 208 parameter combinations.

### Complete Pipeline

```bash
make all          # Install + figures
make reproduce-all  # Install + data + figures
```

## Repository Structure

```
costly-paper/
├── src/costly/              # Core simulation package
│   ├── simulation.py        # Main ABM engine
│   ├── case_studies.py      # Rapa Nui/Rapa Iti scenarios
│   ├── parameter_exploration.py
│   ├── sensitivity_analysis.py
│   └── visualization.py
├── scripts/                 # Figure generation scripts
│   ├── generate_all_figures.py
│   └── figure_generation/   # Individual figure scripts
├── figures/final/           # Publication-ready figures (11 total)
├── data/                    # Simulation output (regeneratable)
├── docs/manuscript/         # Paper and supplementary materials
└── tests/                   # Unit tests
```

## Usage Examples

### Run a Basic Simulation

```python
from costly import SpatialSimulation

# Create simulation with default parameters
sim = SpatialSimulation(
    grid_size=40,
    n_groups=16,
    shortfall_frequency=10,
    shortfall_magnitude=0.5
)

# Run for 200 years
results = sim.run(years=200)
print(f"Final population: {results['final_population']}")
```

### Compare Rapa Nui and Rapa Iti

```python
from costly.case_studies import compare_rapa_scenarios

# Run comparison with 100 replicates
fig, rn_results, ri_results = compare_rapa_scenarios(
    n_replicates=100,
    years=200
)
fig.savefig('rapa_comparison.png', dpi=300)
```

### Run Parameter Exploration

```python
from costly.parameter_exploration import run_parameter_grid

# Explore frequency-magnitude space
results = run_parameter_grid(
    frequencies=[5, 10, 15, 20],
    magnitudes=[0.2, 0.4, 0.6, 0.8],
    n_replicates=10
)
```

## Model Description

### Theoretical Framework

The model implements a multilevel selection framework using the Price equation:

**Condition for costly signaling to spread:**
> Between-group selection (conflict reduction benefits) must exceed within-group selection (reproductive costs)

### Spatial Structure

- 40×40 grid cells representing resource patches
- 16-20 territorial groups with overlapping territories
- Resource availability varies over time with periodic shortfalls

### Strategies

1. **Monument Building (Costly Signaling)**: 35% resource cost invested in monuments, 75% conflict reduction
2. **High Reproduction**: 40-50% reproduction bonus, no conflict reduction investment

### Environmental Parameters

- **Shortfall frequency**: Years between resource crashes (5-20 years)
- **Shortfall magnitude**: Proportional reduction in productivity (0.2-0.8)

### Empirical Calibration

| Parameter | Rapa Nui | Rapa Iti |
|-----------|----------|----------|
| Shortfall frequency | 6 years | 18 years |
| Shortfall magnitude | 0.6 | 0.3 |
| Duration | 2-3 years | 1 year |

## Figures

| Figure | Description |
|--------|-------------|
| 1 | Pacific Overview Map |
| 2 | Price Equation for Multilevel Selection |
| 3 | Frequency Comparison |
| 4 | Magnitude Comparison |
| 5 | Combined Shortfall Scenarios |
| 6 | Modified Price Equation Framework |
| 7 | Model Dynamics Overview |
| 8 | Environmental Phase Space |
| 9 | Validation of Predictions |
| 10 | Temporal Dynamics |
| 11 | Case Study Comparison |

## Requirements

- Python 3.8+
- NumPy >= 1.21.0
- SciPy >= 1.7.0
- Matplotlib >= 3.5.0
- tqdm >= 4.62.0

## Code Quality

Run linting:
```bash
make lint
```

Run tests:
```bash
make test
```

## Citation

```bibtex
@article{lipo2026paradox,
  title={The Paradox of Monumental Architecture: An Agent-Based Model of
         Costly Signaling Under Resource Uncertainty},
  author={Lipo, Carl P. DiNapoli, Robert J. and Hunt, Terry L.},
  journal={Proceedings of the Royal Society B},
  year={2026},
  note={in review}
}
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contact

- Carl P. Lipo - Binghamton University - clipo@binghamton.edu
- Robert J. DiNapoli - Binghamton University - dinapoli@binghamton.edu
- Terry L. Hunt - University of Arizona - tlhunt@arizona.edu

## Acknowledgments

Model development and analysis performed with assistance from Claude Code (Anthropic).
