"""
Case study comparisons: Rapa Nui vs Rapa Iti

Rapa Nui hypothesis:
- Lower, more uncertain productivity
- Frequent resource shortfalls
- Led to monument building strategy
- Multiple small groups cooperating internally, competing through signaling
- Lower overall population

Rapa Iti hypothesis:
- Higher, more stable productivity
- Rare resource shortfalls
- Led to high reproduction strategy
- Defensive positions to protect land
- Higher overall population with more conflict
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

from .simulation import SpatialSimulation, Strategy
from .visualization import SimulationVisualizer


def get_rapa_nui_params():
    """
    Parameters representing Rapa Nui conditions:
    - Lower productivity
    - Frequent shortfalls (every 5-7 years)
    - Moderate shortfall magnitude
    """
    return {
        'grid_size': (40, 40),
        'n_groups': 20,
        'base_productivity': 0.8,  # Lower base productivity
        'shortfall_frequency': 6,  # More frequent shortfalls
        'shortfall_magnitude': 0.6,  # Moderate-severe shortfalls
        'monument_cost': 0.35,  # Significant monument investment
        'reproduction_bonus': 0.4,
        'conflict_mortality': 0.25,
        'signaling_conflict_reduction': 0.75,  # Strong conflict deterrence from monuments
        'carrying_capacity_per_cell': 8.0,  # Lower carrying capacity
        'seed': 42
    }


def get_rapa_iti_params():
    """
    Parameters representing Rapa Iti conditions:
    - Higher productivity
    - Rare shortfalls (every 15-20 years)
    - Mild shortfall magnitude
    """
    return {
        'grid_size': (40, 40),
        'n_groups': 20,
        'base_productivity': 1.2,  # Higher base productivity
        'shortfall_frequency': 18,  # Rare shortfalls
        'shortfall_magnitude': 0.3,  # Mild shortfalls
        'monument_cost': 0.35,
        'reproduction_bonus': 0.4,
        'conflict_mortality': 0.25,
        'signaling_conflict_reduction': 0.75,
        'carrying_capacity_per_cell': 15.0,  # Higher carrying capacity
        'seed': 42
    }


def run_rapa_nui_simulation(years: int = 200, strategy_mix: str = 'signaling_dominant'):
    """
    Run Rapa Nui scenario simulation

    Parameters:
    -----------
    years: Simulation length
    strategy_mix: 'signaling_dominant', 'mixed', or 'reproduction_dominant'
    """
    params = get_rapa_nui_params()

    strategy_proportions = {
        'signaling_dominant': {Strategy.COSTLY_SIGNALING: 0.8, Strategy.HIGH_REPRODUCTION: 0.2},
        'mixed': {Strategy.COSTLY_SIGNALING: 0.5, Strategy.HIGH_REPRODUCTION: 0.5},
        'reproduction_dominant': {Strategy.COSTLY_SIGNALING: 0.2, Strategy.HIGH_REPRODUCTION: 0.8}
    }

    sim = SpatialSimulation(**params)
    sim.initialize_groups(strategy_proportions[strategy_mix])
    sim.run(years)

    return sim


def run_rapa_iti_simulation(years: int = 200, strategy_mix: str = 'reproduction_dominant'):
    """
    Run Rapa Iti scenario simulation

    Parameters:
    -----------
    years: Simulation length
    strategy_mix: 'signaling_dominant', 'mixed', or 'reproduction_dominant'
    """
    params = get_rapa_iti_params()

    strategy_proportions = {
        'signaling_dominant': {Strategy.COSTLY_SIGNALING: 0.8, Strategy.HIGH_REPRODUCTION: 0.2},
        'mixed': {Strategy.COSTLY_SIGNALING: 0.5, Strategy.HIGH_REPRODUCTION: 0.5},
        'reproduction_dominant': {Strategy.COSTLY_SIGNALING: 0.2, Strategy.HIGH_REPRODUCTION: 0.8}
    }

    sim = SpatialSimulation(**params)
    sim.initialize_groups(strategy_proportions[strategy_mix])
    sim.run(years)

    return sim


def compare_rapa_scenarios(years: int = 200, figsize=(16, 10)):
    """
    Run and compare both Rapa Nui and Rapa Iti scenarios

    This demonstrates the key hypothesis:
    - Rapa Nui (low productivity, frequent shortfalls) -> signaling dominant -> lower population
    - Rapa Iti (high productivity, rare shortfalls) -> reproduction dominant -> higher population
    """
    print("Running Rapa Nui scenario (signaling dominant)...")
    rapa_nui_sim = run_rapa_nui_simulation(years, 'signaling_dominant')

    print("Running Rapa Iti scenario (reproduction dominant)...")
    rapa_iti_sim = run_rapa_iti_simulation(years, 'reproduction_dominant')

    # Create comparison visualization
    fig = plt.figure(figsize=figsize)
    gs = GridSpec(3, 4, figure=fig, hspace=0.35, wspace=0.35)

    # Title
    fig.suptitle('Rapa Nui vs Rapa Iti: Costly Signaling Under Different Resource Conditions',
                fontsize=16, fontweight='bold')

    # RAPA NUI PLOTS
    # Territory map
    ax_rn_map = fig.add_subplot(gs[0:2, 0:2])
    visualizer_rn = SimulationVisualizer(rapa_nui_sim)
    visualizer_rn._plot_territory_map(ax_rn_map)
    ax_rn_map.set_title('Rapa Nui: Territorial Control\n(Low productivity, frequent shortfalls)',
                       fontweight='bold', fontsize=11)

    # Population time series
    ax_rn_pop = fig.add_subplot(gs[0, 2:])
    years_rn = range(len(rapa_nui_sim.history['total_population']))
    for strategy in Strategy:
        pop_data = rapa_nui_sim.history['population_by_strategy'][strategy]
        color = 'blue' if strategy == Strategy.COSTLY_SIGNALING else 'red'
        ax_rn_pop.plot(years_rn, pop_data, label=strategy.value, linewidth=2, color=color)
    ax_rn_pop.set_ylabel('Population')
    ax_rn_pop.set_title('Rapa Nui: Population by Strategy', fontweight='bold')
    ax_rn_pop.legend(fontsize=9)
    ax_rn_pop.grid(True, alpha=0.3)

    # Conflicts
    ax_rn_conflict = fig.add_subplot(gs[1, 2:])
    ax_rn_conflict.plot(years_rn, np.cumsum(rapa_nui_sim.history['conflicts_per_year']),
                       'darkred', linewidth=2)
    ax_rn_conflict.set_xlabel('Year')
    ax_rn_conflict.set_ylabel('Cumulative Conflicts')
    ax_rn_conflict.set_title('Rapa Nui: Cumulative Conflicts', fontweight='bold')
    ax_rn_conflict.grid(True, alpha=0.3)

    # RAPA ITI PLOTS
    # Territory map
    ax_ri_map = fig.add_subplot(gs[2, 0:2])
    visualizer_ri = SimulationVisualizer(rapa_iti_sim)
    visualizer_ri._plot_territory_map(ax_ri_map)
    ax_ri_map.set_title('Rapa Iti: Territorial Control\n(High productivity, rare shortfalls)',
                       fontweight='bold', fontsize=11)

    # Population time series
    ax_ri_pop = fig.add_subplot(gs[2, 2])
    years_ri = range(len(rapa_iti_sim.history['total_population']))
    for strategy in Strategy:
        pop_data = rapa_iti_sim.history['population_by_strategy'][strategy]
        color = 'blue' if strategy == Strategy.COSTLY_SIGNALING else 'red'
        ax_ri_pop.plot(years_ri, pop_data, label=strategy.value, linewidth=2, color=color)
    ax_ri_pop.set_xlabel('Year')
    ax_ri_pop.set_ylabel('Population')
    ax_ri_pop.set_title('Rapa Iti: Population by Strategy', fontweight='bold')
    ax_ri_pop.legend(fontsize=9)
    ax_ri_pop.grid(True, alpha=0.3)

    # Comparison bar chart
    ax_compare = fig.add_subplot(gs[2, 3])

    rn_stats = rapa_nui_sim.get_summary_statistics()
    ri_stats = rapa_iti_sim.get_summary_statistics()

    categories = ['Total\nPopulation', 'Conflicts', 'Signaling\nGroups']
    rn_values = [
        rn_stats['total_population'],
        rn_stats['total_conflicts'],
        rn_stats['Monument Building_groups']
    ]
    ri_values = [
        ri_stats['total_population'],
        ri_stats['total_conflicts'],
        ri_stats['Monument Building_groups']
    ]

    x = np.arange(len(categories))
    width = 0.35

    # Normalize for comparison
    max_vals = [max(rn_values[i], ri_values[i]) for i in range(len(categories))]
    rn_normalized = [rn_values[i] / max_vals[i] if max_vals[i] > 0 else 0 for i in range(len(categories))]
    ri_normalized = [ri_values[i] / max_vals[i] if max_vals[i] > 0 else 0 for i in range(len(categories))]

    bars1 = ax_compare.bar(x - width/2, rn_normalized, width, label='Rapa Nui', color='steelblue')
    bars2 = ax_compare.bar(x + width/2, ri_normalized, width, label='Rapa Iti', color='coral')

    ax_compare.set_ylabel('Relative Value (normalized)')
    ax_compare.set_title('Comparative Outcomes', fontweight='bold')
    ax_compare.set_xticks(x)
    ax_compare.set_xticklabels(categories, fontsize=9)
    ax_compare.legend(fontsize=9)
    ax_compare.grid(True, alpha=0.3, axis='y')

    # Add actual values on bars
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        height1 = bar1.get_height()
        height2 = bar2.get_height()
        ax_compare.text(bar1.get_x() + bar1.get_width()/2., height1,
                       f'{rn_values[i]:.0f}',
                       ha='center', va='bottom', fontsize=8)
        ax_compare.text(bar2.get_x() + bar2.get_width()/2., height2,
                       f'{ri_values[i]:.0f}',
                       ha='center', va='bottom', fontsize=8)

    return fig, rapa_nui_sim, rapa_iti_sim


def test_strategy_stability(island_type: str = 'rapa_nui', years: int = 200, figsize=(14, 8)):
    """
    Test what happens when different strategies are tried on each island

    This shows whether the dominant strategy is stable or if mixed strategies can coexist
    """
    if island_type == 'rapa_nui':
        params_func = get_rapa_nui_params
        title = 'Rapa Nui: Testing Strategy Stability'
    else:
        params_func = get_rapa_iti_params
        title = 'Rapa Iti: Testing Strategy Stability'

    strategy_mixes = {
        'All Signaling': {Strategy.COSTLY_SIGNALING: 1.0, Strategy.HIGH_REPRODUCTION: 0.0},
        '75% Signaling': {Strategy.COSTLY_SIGNALING: 0.75, Strategy.HIGH_REPRODUCTION: 0.25},
        '50-50 Mix': {Strategy.COSTLY_SIGNALING: 0.5, Strategy.HIGH_REPRODUCTION: 0.5},
        '25% Signaling': {Strategy.COSTLY_SIGNALING: 0.25, Strategy.HIGH_REPRODUCTION: 0.75},
        'All Reproduction': {Strategy.COSTLY_SIGNALING: 0.0, Strategy.HIGH_REPRODUCTION: 1.0},
    }

    fig, axes = plt.subplots(2, 3, figsize=figsize)
    axes = axes.flatten()

    results_summary = {}

    for idx, (mix_name, proportions) in enumerate(strategy_mixes.items()):
        if idx >= 5:  # We have 6 subplots but 5 scenarios
            break

        print(f"Running {island_type} with {mix_name}...")

        params = params_func()
        sim = SpatialSimulation(**params)
        sim.initialize_groups(proportions)
        sim.run(years)

        # Plot population time series
        ax = axes[idx]
        years_range = range(len(sim.history['total_population']))

        for strategy in Strategy:
            pop_data = sim.history['population_by_strategy'][strategy]
            color = 'blue' if strategy == Strategy.COSTLY_SIGNALING else 'red'
            ax.plot(years_range, pop_data, label=strategy.value, linewidth=2, color=color)

        ax.set_xlabel('Year')
        ax.set_ylabel('Population')
        ax.set_title(mix_name, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # Store results
        stats = sim.get_summary_statistics()
        results_summary[mix_name] = {
            'total_pop': stats['total_population'],
            'signaling_pop': stats['Monument Building_population'],
            'reproduction_pop': stats['High Reproduction_population'],
            'conflicts': stats['total_conflicts']
        }

    # Summary comparison in last subplot
    ax_summary = axes[5]
    ax_summary.axis('off')

    summary_text = f"{title}\n\nFinal Populations:\n"
    for mix_name, data in results_summary.items():
        summary_text += f"\n{mix_name}:\n"
        summary_text += f"  Total: {data['total_pop']:.0f}\n"
        summary_text += f"  Conflicts: {data['conflicts']:.0f}\n"

    ax_summary.text(0.1, 0.95, summary_text, transform=ax_summary.transAxes,
                   fontsize=9, verticalalignment='top', fontfamily='monospace',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()

    return fig, results_summary


def explore_productivity_gradient(
    productivity_range: tuple = (0.5, 1.5),
    shortfall_freq_range: tuple = (5, 20),
    n_points: int = 10,
    years: int = 150
):
    """
    Explore gradient from Rapa Nui-like to Rapa Iti-like conditions

    Shows smooth transition in strategy dominance
    """
    productivities = np.linspace(productivity_range[0], productivity_range[1], n_points)
    shortfall_freqs = np.linspace(shortfall_freq_range[0], shortfall_freq_range[1], n_points, dtype=int)

    results = {
        'productivity': [],
        'shortfall_freq': [],
        'total_pop': [],
        'signaling_pop': [],
        'reproduction_pop': [],
        'conflicts': []
    }

    print(f"Exploring productivity gradient with {n_points} points...")

    for prod in productivities:
        for freq in shortfall_freqs:
            params = {
                'grid_size': (30, 30),
                'n_groups': 16,
                'base_productivity': prod,
                'shortfall_frequency': freq,
                'shortfall_magnitude': 0.5,
                'monument_cost': 0.35,
                'reproduction_bonus': 0.4,
                'conflict_mortality': 0.25,
                'carrying_capacity_per_cell': 10.0,
                'seed': 42
            }

            sim = SpatialSimulation(**params)
            sim.initialize_groups({Strategy.COSTLY_SIGNALING: 0.5, Strategy.HIGH_REPRODUCTION: 0.5})
            sim.run(years)

            stats = sim.get_summary_statistics()

            results['productivity'].append(prod)
            results['shortfall_freq'].append(freq)
            results['total_pop'].append(stats['total_population'])
            results['signaling_pop'].append(stats['Monument Building_population'])
            results['reproduction_pop'].append(stats['High Reproduction_population'])
            results['conflicts'].append(stats['total_conflicts'])

    return results


def plot_productivity_gradient(results: dict, figsize=(14, 5)):
    """Plot results from productivity gradient exploration"""
    fig, axes = plt.subplots(1, 3, figsize=figsize)

    prod_array = np.array(results['productivity'])
    freq_array = np.array(results['shortfall_freq'])

    # Calculate strategy dominance
    sig_array = np.array(results['signaling_pop'])
    rep_array = np.array(results['reproduction_pop'])
    total_array = sig_array + rep_array
    dominance = np.zeros_like(total_array)
    mask = total_array > 0
    dominance[mask] = (sig_array[mask] - rep_array[mask]) / total_array[mask]

    # Plot 1: Dominance by productivity
    ax = axes[0]
    unique_prods = np.unique(prod_array)
    avg_dominance = [np.mean(dominance[prod_array == p]) for p in unique_prods]
    ax.plot(unique_prods, avg_dominance, 'o-', linewidth=2, markersize=8)
    ax.axhline(0, color='black', linestyle='--', alpha=0.5)
    ax.set_xlabel('Base Productivity')
    ax.set_ylabel('Strategy Dominance\n(+ = Signaling, - = Reproduction)')
    ax.set_title('Dominance vs Productivity', fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Mark Rapa Nui and Rapa Iti regions
    ax.axvspan(0.5, 0.8, alpha=0.2, color='blue', label='Rapa Nui-like')
    ax.axvspan(1.2, 1.5, alpha=0.2, color='red', label='Rapa Iti-like')
    ax.legend()

    # Plot 2: Dominance by shortfall frequency
    ax = axes[1]
    unique_freqs = np.unique(freq_array)
    avg_dominance = [np.mean(dominance[freq_array == f]) for f in unique_freqs]
    ax.plot(unique_freqs, avg_dominance, 'o-', linewidth=2, markersize=8)
    ax.axhline(0, color='black', linestyle='--', alpha=0.5)
    ax.set_xlabel('Shortfall Frequency (years)')
    ax.set_ylabel('Strategy Dominance')
    ax.set_title('Dominance vs Shortfall Frequency', fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Plot 3: Total population
    ax = axes[2]
    avg_pop = [np.mean(total_array[prod_array == p]) for p in unique_prods]
    ax.plot(unique_prods, avg_pop, 'ko-', linewidth=2, markersize=8)
    ax.set_xlabel('Base Productivity')
    ax.set_ylabel('Total Population')
    ax.set_title('Total Population vs Productivity', fontweight='bold')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig
