#!/usr/bin/env python3
"""
Parameter Sensitivity Validation for Figure 6 Panel F

This script runs ABM simulations with different conflict reduction (r) values
to validate the theoretical predictions about how r affects strategy dominance.

PURPOSE:
--------
Validate that the ABM produces phase-space patterns consistent with theoretical
predictions when varying the conflict reduction parameter r:
- Higher r → signaling favored at lower stress levels (σ* shifts down)
- Lower r → signaling only favored at higher stress levels (σ* shifts up)

REPRODUCIBILITY:
----------------
- All random seeds are explicitly set for reproducibility
- Seeds are computed as: base_seed + replicate * 1000 + point * 100 + r_index * 10000
- Running this script twice with the same configuration produces identical results

USAGE:
------
From the project root directory:
    python scripts/run_parameter_sensitivity_validation.py

OUTPUT:
-------
Saves results to: data/parameter_sensitivity_results_YYYYMMDD_HHMMSS.pkl

The pickle file contains:
- 'results': Dict mapping r values to transect dominance data
- 'config': Configuration parameters used
- 'timestamp': When the simulations were run

REQUIREMENTS:
-------------
- Python 3.8+
- numpy
- The src/costly/ module must be importable

ESTIMATED RUNTIME:
------------------
- ~10-20 minutes for default configuration (3 r-values × 12 points × 5 replicates × 100 years)
- Scale linearly with configuration parameters
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

# Number of replicates per parameter point
N_REPLICATES = 5

# Simulation length in years
YEARS = 100

# Grid and group configuration (matches sensitivity analysis)
GRID_SIZE = (40, 40)
N_GROUPS = 16

# Conflict reduction values to test
# These correspond to the lines in Figure 6 Panel F
R_VALUES = [0.50, 0.75, 0.90]

# Base ABM parameters (r will be varied)
ABM_PARAMS_BASE = {
    'base_productivity': 1.0,
    'monument_cost': 0.35,            # C = 0.35 (reproductive cost)
    'reproduction_bonus': 0.5,
    'conflict_mortality': 0.2,
    'carrying_capacity_per_cell': 10.0,
}

# Transect configuration: diagonal from Rapa Iti to Rapa Nui
N_TRANSECT_POINTS = 12
FREQ_RANGE = np.linspace(18, 6, N_TRANSECT_POINTS)   # Rapa Iti → Rapa Nui
MAG_RANGE = np.linspace(0.3, 0.7, N_TRANSECT_POINTS)


# =============================================================================
# SIMULATION FUNCTIONS
# =============================================================================

def compute_seed(r_value: float, point_idx: int, replicate: int) -> int:
    """Compute deterministic seed for reproducibility."""
    r_idx = R_VALUES.index(r_value)
    return BASE_SEED + replicate * 1000 + point_idx * 100 + r_idx * 10000


def run_simulation(freq: int, mag: float, r_value: float, seed: int,
                   years: int = YEARS) -> dict:
    """
    Run a single ABM simulation and return final outcomes.

    Parameters:
    -----------
    freq : int
        Shortfall frequency in years
    mag : float
        Shortfall magnitude (0-1)
    r_value : float
        Conflict reduction parameter (0-1)
    seed : int
        Random seed for reproducibility
    years : int
        Number of years to simulate

    Returns:
    --------
    dict with keys:
        - signaling_pop: final signaling population
        - reproduction_pop: final reproduction population
        - total_pop: final total population
        - dominance: strategy dominance (-1 to +1)
    """
    sim = SpatialSimulation(
        grid_size=GRID_SIZE,
        n_groups=N_GROUPS,
        shortfall_frequency=int(freq),
        shortfall_magnitude=mag,
        signaling_conflict_reduction=r_value,
        seed=seed,
        **ABM_PARAMS_BASE
    )

    sim.initialize_groups()

    for year in range(years):
        sim.step()

    # Get final populations
    sig_pop = sum(g.population for g in sim.groups.values()
                 if g.strategy == Strategy.COSTLY_SIGNALING)
    rep_pop = sum(g.population for g in sim.groups.values()
                 if g.strategy == Strategy.HIGH_REPRODUCTION)

    total_pop = sig_pop + rep_pop
    dominance = (sig_pop - rep_pop) / total_pop if total_pop > 0 else 0

    return {
        'signaling_pop': sig_pop,
        'reproduction_pop': rep_pop,
        'total_pop': total_pop,
        'dominance': dominance
    }


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("=" * 80)
    print("PARAMETER SENSITIVITY VALIDATION")
    print("Running ABM simulations to validate Figure 6 Panel F")
    print("=" * 80)
    print("\nConfiguration:")
    print(f"  Base seed: {BASE_SEED}")
    print(f"  Replicates per point: {N_REPLICATES}")
    print(f"  Years per simulation: {YEARS}")
    print(f"  Transect points: {N_TRANSECT_POINTS}")
    print(f"  r values to test: {R_VALUES}")
    print("\nTheoretical prediction:")
    print("  Higher r → signaling favored at lower stress (σ* shifts down)")
    print("  Lower r → signaling only at higher stress (σ* shifts up)")

    results = {}

    for r_value in R_VALUES:
        print(f"\n{'='*60}")
        print(f"Conflict Reduction: r = {r_value}")
        print(f"Running {N_TRANSECT_POINTS} transect points × {N_REPLICATES} replicates")
        print(f"{'='*60}")

        transect_results = {
            'r_value': r_value,
            'freqs': FREQ_RANGE.copy(),
            'mags': MAG_RANGE.copy(),
            'dominance_mean': np.zeros(N_TRANSECT_POINTS),
            'dominance_std': np.zeros(N_TRANSECT_POINTS),
            'all_dominance': []
        }

        for i, (freq, mag) in enumerate(zip(FREQ_RANGE, MAG_RANGE)):
            dom_values = []

            for rep in range(N_REPLICATES):
                seed = compute_seed(r_value, i, rep)

                result = run_simulation(
                    freq=freq,
                    mag=mag,
                    r_value=r_value,
                    seed=seed,
                    years=YEARS
                )
                dom_values.append(result['dominance'])

            transect_results['dominance_mean'][i] = np.mean(dom_values)
            transect_results['dominance_std'][i] = np.std(dom_values)
            transect_results['all_dominance'].append(dom_values)

            print(f"  Point {i+1:2d}/{N_TRANSECT_POINTS}: "
                  f"freq={freq:5.1f}, mag={mag:.2f} → "
                  f"dom={transect_results['dominance_mean'][i]:+.3f} "
                  f"(±{transect_results['dominance_std'][i]:.3f})")

        results[r_value] = transect_results

        # Find crossover point (where dominance crosses zero)
        dom = transect_results['dominance_mean']
        crossover_info = find_crossover(dom, FREQ_RANGE, MAG_RANGE)
        if crossover_info:
            print(f"\n  Crossover at approx: freq={crossover_info['freq']:.1f}, "
                  f"mag={crossover_info['mag']:.2f}")
        else:
            if np.all(dom > 0):
                print("\n  No crossover: Signaling favored throughout transect")
            elif np.all(dom < 0):
                print("\n  No crossover: Reproduction favored throughout transect")
            else:
                print("\n  Crossover detection unclear")

    # Save results
    os.makedirs(os.path.join(PROJECT_ROOT, 'data'), exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(PROJECT_ROOT, 'data',
                               f'parameter_sensitivity_results_{timestamp}.pkl')

    with open(output_file, 'wb') as f:
        pickle.dump({
            'results': results,
            'config': {
                'base_seed': BASE_SEED,
                'n_replicates': N_REPLICATES,
                'years': YEARS,
                'grid_size': GRID_SIZE,
                'n_groups': N_GROUPS,
                'r_values': R_VALUES,
                'n_transect_points': N_TRANSECT_POINTS,
                'abm_params_base': ABM_PARAMS_BASE
            },
            'timestamp': timestamp
        }, f)

    print(f"\n{'='*80}")
    print(f"Results saved to: {output_file}")
    print(f"{'='*80}")

    # Summary
    print("\n=== VALIDATION SUMMARY ===")
    print("\nTheoretical prediction: Higher r → more of transect favors signaling")
    print("\nSimulation results:")
    for r_value in R_VALUES:
        dom = results[r_value]['dominance_mean']
        positive_frac = np.sum(dom > 0) / len(dom)
        print(f"  r = {r_value}: {positive_frac*100:.0f}% of transect favors signaling")

    # Check if pattern matches theory
    fracs = [np.sum(results[r]['dominance_mean'] > 0) / N_TRANSECT_POINTS
             for r in R_VALUES]
    if fracs[0] < fracs[1] < fracs[2]:
        print("\n  ✓ Pattern matches theory: Higher r → more signaling favorable")
    else:
        print("\n  ? Pattern unclear or reversed - investigate further")


def find_crossover(dom: np.ndarray, freqs: np.ndarray, mags: np.ndarray) -> dict:
    """Find approximate crossover point where dominance crosses zero."""
    for i in range(len(dom) - 1):
        if (dom[i] < 0 and dom[i+1] > 0) or (dom[i] > 0 and dom[i+1] < 0):
            # Linear interpolation
            t = -dom[i] / (dom[i+1] - dom[i])
            cross_freq = freqs[i] + t * (freqs[i+1] - freqs[i])
            cross_mag = mags[i] + t * (mags[i+1] - mags[i])
            return {'freq': cross_freq, 'mag': cross_mag, 'index': i + t}
    return None


if __name__ == '__main__':
    main()
