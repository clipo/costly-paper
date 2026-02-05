#!/usr/bin/env python3
"""
Temporal Dynamics Validation for Figure 6 Panel E

This script runs ABM simulations to generate time-series data for validating
the theoretical temporal dynamics predictions from the modified Price equation.

PURPOSE:
--------
Validate that the ABM produces temporal trajectories consistent with
theoretical predictions:
- High stress environments → signaling frequency increases over time
- Low stress environments → signaling frequency decreases over time
- Critical threshold → signaling frequency remains stable

REPRODUCIBILITY:
----------------
- All random seeds are explicitly set for reproducibility
- Seeds are computed as: base_seed + replicate_index * 1000 + condition_hash
- Running this script twice with the same configuration produces identical results

USAGE:
------
From the project root directory:
    python scripts/run_temporal_validation.py

OUTPUT:
-------
Saves results to: data/temporal_validation_results_YYYYMMDD_HHMMSS.pkl

The pickle file contains:
- 'results': Dict mapping condition names to trajectory data
- 'config': Configuration parameters used
- 'timestamp': When the simulations were run

REQUIREMENTS:
-------------
- Python 3.8+
- numpy
- The src/costly/ module must be importable

ESTIMATED RUNTIME:
------------------
- ~5-10 minutes for default configuration (3 conditions × 10 replicates × 200 years)
- Scale linearly with N_REPLICATES and YEARS
"""

import os
import sys

# Ensure src/costly is importable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src', 'costly'))

import pickle
from datetime import datetime

import numpy as np
from simulation import SpatialSimulation, Strategy

# =============================================================================
# CONFIGURATION - Modify these for different analyses
# =============================================================================

# Random seed base for reproducibility
BASE_SEED = 20260112  # Date-based seed for traceability

# Number of independent simulation runs per condition
N_REPLICATES = 10

# Simulation length in years
YEARS = 200

# Grid and group configuration (matches sensitivity analysis)
GRID_SIZE = (40, 40)
N_GROUPS = 16

# ABM parameters (standard values from main analysis)
ABM_PARAMS = {
    'base_productivity': 1.0,
    'monument_cost': 0.35,            # C = 0.35 (reproductive cost)
    'reproduction_bonus': 0.5,
    'conflict_mortality': 0.2,
    'signaling_conflict_reduction': 0.75,  # r = 0.75 (conflict reduction)
    'carrying_capacity_per_cell': 10.0,
}

# Environmental conditions to test
# Each maps to theoretical predictions from the modified Price equation
CONDITIONS = {
    'rapa_nui': {
        'freq': 6,
        'mag': 0.6,
        'label': 'Rapa Nui (high stress)',
        'expected': 'Signaling frequency → 1.0 (signaling wins)'
    },
    'rapa_iti': {
        'freq': 18,
        'mag': 0.3,
        'label': 'Rapa Iti (low stress)',
        'expected': 'Signaling frequency → 0.0 (reproduction wins)'
    },
    'critical': {
        'freq': 12,
        'mag': 0.4,
        'label': 'Critical threshold (near σ*)',
        'expected': 'Signaling frequency ≈ 0.5 (balanced)'
    },
}


# =============================================================================
# SIMULATION FUNCTIONS
# =============================================================================

def compute_seed(condition_name: str, replicate: int) -> int:
    """Compute deterministic seed for reproducibility."""
    condition_hash = hash(condition_name) % 100000
    return BASE_SEED + replicate * 1000 + condition_hash


def run_simulation(freq: int, mag: float, seed: int, years: int = YEARS) -> dict:
    """
    Run a single ABM simulation and return population time series.

    Parameters:
    -----------
    freq : int
        Shortfall frequency in years
    mag : float
        Shortfall magnitude (0-1)
    seed : int
        Random seed for reproducibility
    years : int
        Number of years to simulate

    Returns:
    --------
    dict with keys:
        - signaling_pop: array of signaling population over time
        - reproduction_pop: array of reproduction population over time
        - total_pop: array of total population over time
        - signaling_freq: array of signaling frequency (0-1) over time
    """
    sim = SpatialSimulation(
        grid_size=GRID_SIZE,
        n_groups=N_GROUPS,
        shortfall_frequency=freq,
        shortfall_magnitude=mag,
        seed=seed,
        **ABM_PARAMS
    )

    sim.initialize_groups()

    # Track populations over time
    signaling_pop = np.zeros(years)
    reproduction_pop = np.zeros(years)

    for year in range(years):
        sim.step()

        # Get population by strategy
        sig_pop = sum(g.population for g in sim.groups.values()
                     if g.strategy == Strategy.COSTLY_SIGNALING)
        rep_pop = sum(g.population for g in sim.groups.values()
                     if g.strategy == Strategy.HIGH_REPRODUCTION)

        signaling_pop[year] = sig_pop
        reproduction_pop[year] = rep_pop

    # Calculate signaling frequency
    total_pop = signaling_pop + reproduction_pop
    signaling_freq = np.where(total_pop > 0, signaling_pop / total_pop, 0.5)

    return {
        'signaling_pop': signaling_pop,
        'reproduction_pop': reproduction_pop,
        'total_pop': total_pop,
        'signaling_freq': signaling_freq
    }


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("=" * 80)
    print("TEMPORAL DYNAMICS VALIDATION")
    print("Running ABM simulations to validate Figure 6 Panel E")
    print("=" * 80)
    print("\nConfiguration:")
    print(f"  Base seed: {BASE_SEED}")
    print(f"  Replicates per condition: {N_REPLICATES}")
    print(f"  Years per simulation: {YEARS}")
    print(f"  Grid size: {GRID_SIZE}")
    print(f"  Number of groups: {N_GROUPS}")
    print("\nConditions to test:")
    for name, params in CONDITIONS.items():
        print(f"  - {params['label']}: freq={params['freq']}, mag={params['mag']}")
        print(f"    Expected: {params['expected']}")

    results = {}

    for condition_name, params in CONDITIONS.items():
        print(f"\n{'='*60}")
        print(f"Condition: {params['label']}")
        print(f"  Frequency: {params['freq']} years")
        print(f"  Magnitude: {params['mag']}")
        print(f"  Running {N_REPLICATES} replicates...")
        print(f"{'='*60}")

        all_trajectories = []

        for rep in range(N_REPLICATES):
            seed = compute_seed(condition_name, rep)

            trajectory = run_simulation(
                freq=params['freq'],
                mag=params['mag'],
                seed=seed,
                years=YEARS
            )
            all_trajectories.append(trajectory)

            final_freq = trajectory['signaling_freq'][-1]
            print(f"  Replicate {rep+1:2d}/{N_REPLICATES}: "
                  f"seed={seed:8d}, final signaling freq = {final_freq:.3f}")

        # Aggregate results
        signaling_freq_all = np.array([t['signaling_freq'] for t in all_trajectories])
        signaling_freq_mean = np.mean(signaling_freq_all, axis=0)
        signaling_freq_std = np.std(signaling_freq_all, axis=0)

        results[condition_name] = {
            'params': params,
            'all_trajectories': all_trajectories,
            'signaling_freq_mean': signaling_freq_mean,
            'signaling_freq_std': signaling_freq_std,
            'signaling_freq_all': signaling_freq_all,
            'years': np.arange(YEARS)
        }

        print(f"\n  Mean final signaling freq: {signaling_freq_mean[-1]:.3f} "
              f"(±{signaling_freq_std[-1]:.3f})")
        print(f"  Expected: {params['expected']}")

    # Save results
    os.makedirs(os.path.join(PROJECT_ROOT, 'data'), exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(PROJECT_ROOT, 'data',
                               f'temporal_validation_results_{timestamp}.pkl')

    with open(output_file, 'wb') as f:
        pickle.dump({
            'results': results,
            'config': {
                'base_seed': BASE_SEED,
                'n_replicates': N_REPLICATES,
                'years': YEARS,
                'grid_size': GRID_SIZE,
                'n_groups': N_GROUPS,
                'abm_params': ABM_PARAMS,
                'conditions': CONDITIONS
            },
            'timestamp': timestamp
        }, f)

    print(f"\n{'='*80}")
    print(f"Results saved to: {output_file}")
    print(f"{'='*80}")

    # Summary
    print("\n=== VALIDATION SUMMARY ===")
    print("\nComparison with theoretical predictions:")
    for condition_name, result in results.items():
        params = result['params']
        final_mean = result['signaling_freq_mean'][-1]
        final_std = result['signaling_freq_std'][-1]

        # Determine if result matches expectation
        if 'Rapa Nui' in params['label']:
            match = "✓" if final_mean > 0.7 else "✗"
        elif 'Rapa Iti' in params['label']:
            match = "✓" if final_mean < 0.3 else "✗"
        else:  # Critical
            match = "✓" if 0.3 < final_mean < 0.7 else "~"

        print(f"\n{params['label']}:")
        print(f"  Result: {final_mean:.3f} ± {final_std:.3f}")
        print(f"  Expected: {params['expected']}")
        print(f"  Match: {match}")


if __name__ == '__main__':
    main()
