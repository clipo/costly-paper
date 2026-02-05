"""
Parameter exploration for costly signaling simulation
Identifies conditions under which costly signaling dominates
"""

from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from .simulation import SpatialSimulation, Strategy


def run_single_simulation(params: dict, years: int = 100, seed: int = None) -> dict:
    """
    Run a single simulation with given parameters

    Returns summary statistics
    """
    # Separate strategy_proportions from simulation parameters
    strategy_proportions = params.get('strategy_proportions', None)
    sim_params = {k: v for k, v in params.items() if k != 'strategy_proportions'}

    sim = SpatialSimulation(**sim_params, seed=seed)
    sim.initialize_groups(strategy_proportions)
    sim.run(years)

    stats = sim.get_summary_statistics()
    stats['sim'] = sim  # Include simulation object for detailed analysis

    return stats


def explore_resource_uncertainty(
    shortfall_frequencies: List[int],
    shortfall_magnitudes: List[float],
    n_replicates: int = 5,
    years: int = 100,
    base_params: dict = None,
    seed_offset: int = 0
) -> dict:
    """
    Explore how resource uncertainty (shortfall frequency and magnitude) affects outcomes

    Parameters:
    -----------
    shortfall_frequencies: List of frequencies to test
    shortfall_magnitudes: List of magnitudes to test
    n_replicates: Number of replicate runs per parameter combination
    years: Simulation length
    base_params: Base parameters to use (others will be defaults)
    seed_offset: Offset to add to seeds for independent runs (e.g., run_idx * 100000)

    Returns:
    --------
    Dictionary of results indexed by (frequency, magnitude)
    """
    if base_params is None:
        base_params = {
            'grid_size': (40, 40),
            'n_groups': 16,
            'base_productivity': 1.0,
            'monument_cost': 0.3,
            'reproduction_bonus': 0.5,
            'conflict_mortality': 0.2,
            'carrying_capacity_per_cell': 10.0,
        }

    results = {}

    total_runs = len(shortfall_frequencies) * len(shortfall_magnitudes) * n_replicates

    print(f"Running {total_runs} simulations...")

    with tqdm(total=total_runs) as pbar:
        for freq in shortfall_frequencies:
            for mag in shortfall_magnitudes:
                key = (freq, mag)
                replicate_results = []

                for rep in range(n_replicates):
                    params = base_params.copy()
                    params['shortfall_frequency'] = freq
                    params['shortfall_magnitude'] = mag
                    params['strategy_proportions'] = {
                        Strategy.COSTLY_SIGNALING: 0.5,
                        Strategy.HIGH_REPRODUCTION: 0.5
                    }

                    stats = run_single_simulation(params, years=years, seed=seed_offset + rep)
                    replicate_results.append(stats)
                    pbar.update(1)

                # Aggregate across replicates
                results[key] = {
                    'signaling_pop_mean': np.mean([r['Monument Building_population'] for r in replicate_results]),
                    'signaling_pop_std': np.std([r['Monument Building_population'] for r in replicate_results]),
                    'reproduction_pop_mean': np.mean([r['High Reproduction_population'] for r in replicate_results]),
                    'reproduction_pop_std': np.std([r['High Reproduction_population'] for r in replicate_results]),
                    'total_pop_mean': np.mean([r['total_population'] for r in replicate_results]),
                    'total_pop_std': np.std([r['total_population'] for r in replicate_results]),
                    'conflicts_mean': np.mean([r['total_conflicts'] for r in replicate_results]),
                    'conflicts_std': np.std([r['total_conflicts'] for r in replicate_results]),
                    'signaling_groups_mean': np.mean([r['Monument Building_groups'] for r in replicate_results]),
                    'reproduction_groups_mean': np.mean([r['High Reproduction_groups'] for r in replicate_results]),
                    'replicates': replicate_results
                }

    return results


def plot_parameter_space(results: dict, metric: str = 'dominance', figsize=(12, 5)):
    """
    Plot results across parameter space

    Parameters:
    -----------
    results: Output from explore_resource_uncertainty
    metric: What to plot - 'dominance', 'total_population', 'conflicts'
    """
    # Extract parameter grid
    freqs = sorted(set(k[0] for k in results.keys()))
    mags = sorted(set(k[1] for k in results.keys()))

    # Create meshgrids
    X, Y = np.meshgrid(freqs, mags)

    if metric == 'dominance':
        # Calculate which strategy dominates (-1 = reproduction, +1 = signaling)
        Z = np.zeros_like(X, dtype=float)
        for i, mag in enumerate(mags):
            for j, freq in enumerate(freqs):
                if (freq, mag) in results:
                    sig = results[(freq, mag)]['signaling_pop_mean']
                    rep = results[(freq, mag)]['reproduction_pop_mean']
                    total = sig + rep
                    Z[i, j] = (sig - rep) / total if total > 0 else 0

        title = 'Strategy Dominance Across Resource Uncertainty'
        cmap = 'RdBu'
        cbar_label = 'Dominance\n(Blue=Signaling, Red=Reproduction)'

    elif metric == 'total_population':
        Z = np.zeros_like(X, dtype=float)
        for i, mag in enumerate(mags):
            for j, freq in enumerate(freqs):
                if (freq, mag) in results:
                    Z[i, j] = results[(freq, mag)]['total_pop_mean']

        title = 'Total Population Across Resource Uncertainty'
        cmap = 'viridis'
        cbar_label = 'Total Population'

    elif metric == 'conflicts':
        Z = np.zeros_like(X, dtype=float)
        for i, mag in enumerate(mags):
            for j, freq in enumerate(freqs):
                if (freq, mag) in results:
                    Z[i, j] = results[(freq, mag)]['conflicts_mean']

        title = 'Total Conflicts Across Resource Uncertainty'
        cmap = 'Reds'
        cbar_label = 'Number of Conflicts'

    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Heatmap
    im = ax1.contourf(X, Y, Z, levels=20, cmap=cmap)
    if metric == 'dominance':
        contours = ax1.contour(X, Y, Z, levels=[0], colors='black', linewidths=2)
        ax1.clabel(contours, inline=True, fontsize=10, fmt='Transition')

    cbar = plt.colorbar(im, ax=ax1)
    cbar.set_label(cbar_label, rotation=270, labelpad=20)

    ax1.set_xlabel('Shortfall Frequency (years)')
    ax1.set_ylabel('Shortfall Magnitude (proportion)')
    ax1.set_title(title, fontweight='bold')
    ax1.set_xticks(freqs)
    ax1.set_yticks(mags)

    # Cross-sections
    # Fix magnitude, vary frequency
    mid_mag_idx = len(mags) // 2
    mid_mag = mags[mid_mag_idx]

    sig_pops = []
    rep_pops = []
    for freq in freqs:
        if (freq, mid_mag) in results:
            sig_pops.append(results[(freq, mid_mag)]['signaling_pop_mean'])
            rep_pops.append(results[(freq, mid_mag)]['reproduction_pop_mean'])
        else:
            sig_pops.append(0)
            rep_pops.append(0)

    ax2.plot(freqs, sig_pops, 'b-o', label='Monument Building', linewidth=2)
    ax2.plot(freqs, rep_pops, 'r-o', label='High Reproduction', linewidth=2)
    ax2.set_xlabel('Shortfall Frequency (years)')
    ax2.set_ylabel('Population')
    ax2.set_title(f'Cross-section at magnitude = {mid_mag:.2f}', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def identify_critical_transitions(results: dict, threshold: float = 0.1) -> List[Tuple]:
    """
    Identify parameter combinations where strategies are roughly equal (transitions)

    Parameters:
    -----------
    results: Output from explore_resource_uncertainty
    threshold: Maximum dominance value to be considered a transition

    Returns list of (frequency, magnitude) tuples at transitions
    """
    transitions = []

    for (freq, mag), data in results.items():
        sig = data['signaling_pop_mean']
        rep = data['reproduction_pop_mean']
        total = sig + rep

        if total > 0:
            dominance = abs(sig - rep) / total
            if dominance < threshold:
                transitions.append((freq, mag, dominance))

    # Sort by dominance (closest to 0 first)
    transitions.sort(key=lambda x: x[2])

    return transitions


def compare_strategy_proportions(
    shortfall_frequency: int,
    shortfall_magnitude: float,
    proportions: List[float],
    n_replicates: int = 5,
    years: int = 100,
    base_params: dict = None
) -> dict:
    """
    Compare outcomes with different initial strategy proportions

    Parameters:
    -----------
    shortfall_frequency: Shortfall frequency to test
    shortfall_magnitude: Shortfall magnitude to test
    proportions: List of signaling proportions to test (e.g., [0, 0.25, 0.5, 0.75, 1.0])
    n_replicates: Number of replicate runs per proportion
    years: Simulation length
    base_params: Base parameters to use

    Returns:
    --------
    Dictionary of results indexed by proportion
    """
    if base_params is None:
        base_params = {
            'grid_size': (40, 40),
            'n_groups': 16,
            'base_productivity': 1.0,
            'monument_cost': 0.3,
            'reproduction_bonus': 0.5,
            'conflict_mortality': 0.2,
            'carrying_capacity_per_cell': 10.0,
        }

    results = {}

    print(f"Testing {len(proportions)} proportions with {n_replicates} replicates each...")

    for prop in tqdm(proportions):
        replicate_results = []

        for rep in range(n_replicates):
            params = base_params.copy()
            params['shortfall_frequency'] = shortfall_frequency
            params['shortfall_magnitude'] = shortfall_magnitude
            params['strategy_proportions'] = {
                Strategy.COSTLY_SIGNALING: prop,
                Strategy.HIGH_REPRODUCTION: 1 - prop
            }

            stats = run_single_simulation(params, years=years, seed=rep)
            replicate_results.append(stats)

        # Aggregate
        results[prop] = {
            'signaling_pop_mean': np.mean([r['Monument Building_population'] for r in replicate_results]),
            'signaling_pop_std': np.std([r['Monument Building_population'] for r in replicate_results]),
            'reproduction_pop_mean': np.mean([r['High Reproduction_population'] for r in replicate_results]),
            'reproduction_pop_std': np.std([r['High Reproduction_population'] for r in replicate_results]),
            'total_pop_mean': np.mean([r['total_population'] for r in replicate_results]),
            'total_pop_std': np.std([r['total_population'] for r in replicate_results]),
            'replicates': replicate_results
        }

    return results


def plot_proportion_comparison(results: dict, figsize=(10, 6)):
    """
    Plot outcomes across different initial strategy proportions
    """
    proportions = sorted(results.keys())

    sig_pops = [results[p]['signaling_pop_mean'] for p in proportions]
    sig_stds = [results[p]['signaling_pop_std'] for p in proportions]
    rep_pops = [results[p]['reproduction_pop_mean'] for p in proportions]
    rep_stds = [results[p]['reproduction_pop_std'] for p in proportions]
    total_pops = [results[p]['total_pop_mean'] for p in proportions]
    total_stds = [results[p]['total_pop_std'] for p in proportions]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    # Population by strategy
    ax1.errorbar(proportions, sig_pops, yerr=sig_stds, fmt='b-o',
                 label='Monument Building', linewidth=2, capsize=5)
    ax1.errorbar(proportions, rep_pops, yerr=rep_stds, fmt='r-o',
                 label='High Reproduction', linewidth=2, capsize=5)
    ax1.set_xlabel('Initial Proportion of Signaling Groups')
    ax1.set_ylabel('Final Population')
    ax1.set_title('Final Population by Strategy', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Total population
    ax2.errorbar(proportions, total_pops, yerr=total_stds, fmt='k-o',
                 linewidth=2, capsize=5)
    ax2.set_xlabel('Initial Proportion of Signaling Groups')
    ax2.set_ylabel('Total Population')
    ax2.set_title('Total Island Population', fontweight='bold')
    ax2.grid(True, alpha=0.3)

    # Highlight if total population is lower with signaling
    if total_pops[-1] < total_pops[0]:  # Compare all signaling vs all reproduction
        reduction = (total_pops[0] - total_pops[-1]) / total_pops[0] * 100
        ax2.text(0.5, 0.95, f'Signaling reduces total population by {reduction:.1f}%',
                transform=ax2.transAxes, ha='center', va='top',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

    plt.tight_layout()
    return fig


def analyze_population_dynamics(results: dict, proportion: float):
    """
    Detailed analysis of population dynamics for a specific proportion

    Shows time series from replicates
    """
    if proportion not in results:
        raise ValueError(f"Proportion {proportion} not in results")

    replicates = results[proportion]['replicates']

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Extract time series from replicates
    for i, rep in enumerate(replicates):
        sim = rep['sim']

        # Population over time
        ax = axes[0, 0]
        years = range(len(sim.history['total_population']))
        ax.plot(years, sim.history['total_population'], alpha=0.5, linewidth=1)

        # Population by strategy
        ax = axes[0, 1]
        for strategy in Strategy:
            pop_data = sim.history['population_by_strategy'][strategy]
            color = 'blue' if strategy == Strategy.COSTLY_SIGNALING else 'red'
            ax.plot(years, pop_data, alpha=0.5, linewidth=1, color=color)

        # Conflicts
        ax = axes[1, 0]
        ax.plot(years, np.cumsum(sim.history['conflicts_per_year']),
               alpha=0.5, linewidth=1)

        # Monument investment
        ax = axes[1, 1]
        if sim.history['avg_monument_investment']:
            ax.plot(years, sim.history['avg_monument_investment'],
                   alpha=0.5, linewidth=1)

    # Format axes
    axes[0, 0].set_xlabel('Year')
    axes[0, 0].set_ylabel('Total Population')
    axes[0, 0].set_title('Total Population Over Time (All Replicates)', fontweight='bold')
    axes[0, 0].grid(True, alpha=0.3)

    axes[0, 1].set_xlabel('Year')
    axes[0, 1].set_ylabel('Population')
    axes[0, 1].set_title('Population by Strategy', fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3)

    axes[1, 0].set_xlabel('Year')
    axes[1, 0].set_ylabel('Cumulative Conflicts')
    axes[1, 0].set_title('Cumulative Conflicts', fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3)

    axes[1, 1].set_xlabel('Year')
    axes[1, 1].set_ylabel('Investment')
    axes[1, 1].set_title('Monument Investment', fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)

    plt.suptitle(f'Population Dynamics - {proportion*100:.0f}% Signaling Groups',
                fontsize=14, fontweight='bold')
    plt.tight_layout()

    return fig
