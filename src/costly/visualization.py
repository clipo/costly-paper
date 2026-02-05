"""
Visualization tools for costly signaling simulation
"""

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.gridspec import GridSpec

from .simulation import SpatialSimulation, Strategy


class SimulationVisualizer:
    """Create visualizations of simulation results"""

    def __init__(self, simulation: SpatialSimulation):
        self.sim = simulation

    def plot_comprehensive_results(self, figsize=(16, 12)):
        """Create comprehensive visualization of simulation results"""
        fig = plt.figure(figsize=figsize)
        gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

        # 1. Spatial map with territories and monuments
        ax_map = fig.add_subplot(gs[0:2, 0:2])
        self._plot_territory_map(ax_map)

        # 2. Population over time
        ax_pop = fig.add_subplot(gs[0, 2])
        self._plot_population_time_series(ax_pop)

        # 3. Conflicts over time
        ax_conflict = fig.add_subplot(gs[1, 2])
        self._plot_conflicts(ax_conflict)

        # 4. Population by strategy comparison
        ax_strategy = fig.add_subplot(gs[2, 0])
        self._plot_strategy_comparison(ax_strategy)

        # 5. Monument investment over time
        ax_monument = fig.add_subplot(gs[2, 1])
        self._plot_monument_investment(ax_monument)

        # 6. Summary statistics
        ax_stats = fig.add_subplot(gs[2, 2])
        self._plot_summary_stats(ax_stats)

        plt.suptitle(f'Costly Signaling Simulation - Year {self.sim.year}',
                     fontsize=16, fontweight='bold')

        return fig

    def _plot_territory_map(self, ax):
        """Plot spatial map showing territories and monument investment"""
        # Create territory map with colors by group
        territory_display = self.sim.territory_map.copy().astype(float)

        # Create custom colormap
        n_groups = len(self.sim.groups)
        colors = plt.cm.tab20(np.linspace(0, 1, max(20, n_groups)))
        cmap = ListedColormap(colors)

        im = ax.imshow(territory_display.T, cmap=cmap, interpolation='nearest', origin='lower')
        ax.set_title('Territorial Map with Monument Investment', fontweight='bold')
        ax.set_xlabel('X coordinate')
        ax.set_ylabel('Y coordinate')

        # Overlay monument investment as circles
        for group in self.sim.groups.values():
            if group.territory:
                # Calculate territory center
                x_coords = [x for x, y in group.territory]
                y_coords = [y for x, y in group.territory]
                center_x = np.mean(x_coords)
                center_y = np.mean(y_coords)

                # Monument size proportional to investment (large circles, substantial overlap)
                if group.strategy == Strategy.COSTLY_SIGNALING:
                    monument_size = min(np.sqrt(group.monument_investment) * 0.20, 8.0)
                    circle = plt.Circle((center_x, center_y), monument_size,
                                      color='black', fill=False, linewidth=2)
                    ax.add_patch(circle)

                    # Add marker at center
                    ax.plot(center_x, center_y, 'k^', markersize=8,
                           label='Monument' if group.id == 0 else '')
                else:
                    # High reproduction groups marked differently
                    ax.plot(center_x, center_y, 'ro', markersize=6,
                           label='High Reproduction' if group.id == 0 else '')

        # Legend
        legend_elements = [
            mpatches.Patch(color='none', edgecolor='black', linewidth=2,
                          label='Monument (size = investment)'),
            plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='k',
                      markersize=8, label='Signaling Group'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='r',
                      markersize=6, label='Reproduction Group')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=8)

    def _plot_population_time_series(self, ax):
        """Plot total population over time"""
        if not self.sim.history['total_population']:
            ax.text(0.5, 0.5, 'No data yet', ha='center', va='center')
            return

        years = range(len(self.sim.history['total_population']))
        ax.plot(years, self.sim.history['total_population'], 'k-', linewidth=2)
        ax.fill_between(years, 0, self.sim.history['total_population'], alpha=0.3)

        # Mark shortfall years
        shortfall_years = [y for y in years if y % self.sim.shortfall_frequency == 0]
        for sy in shortfall_years:
            if sy < len(self.sim.history['total_population']):
                ax.axvline(sy, color='red', linestyle='--', alpha=0.3)

        ax.set_xlabel('Year')
        ax.set_ylabel('Total Population')
        ax.set_title('Total Population Over Time', fontweight='bold')
        ax.grid(True, alpha=0.3)

    def _plot_conflicts(self, ax):
        """Plot conflicts over time"""
        if not self.sim.history['conflicts_per_year']:
            ax.text(0.5, 0.5, 'No data yet', ha='center', va='center')
            return

        years = range(len(self.sim.history['conflicts_per_year']))
        ax.bar(years, self.sim.history['conflicts_per_year'], color='darkred', alpha=0.7)

        # Mark shortfall years
        shortfall_years = [y for y in years if y % self.sim.shortfall_frequency == 0]
        for sy in shortfall_years:
            if sy < len(self.sim.history['conflicts_per_year']):
                ax.axvline(sy, color='red', linestyle='--', alpha=0.5, linewidth=2)

        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Conflicts')
        ax.set_title('Border Conflicts Per Year', fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

    def _plot_strategy_comparison(self, ax):
        """Plot population by strategy over time"""
        if not self.sim.history['population_by_strategy'][Strategy.COSTLY_SIGNALING]:
            ax.text(0.5, 0.5, 'No data yet', ha='center', va='center')
            return

        years = range(len(self.sim.history['population_by_strategy'][Strategy.COSTLY_SIGNALING]))

        for strategy in Strategy:
            pop_data = self.sim.history['population_by_strategy'][strategy]
            label = strategy.value
            color = 'blue' if strategy == Strategy.COSTLY_SIGNALING else 'red'
            ax.plot(years, pop_data, label=label, linewidth=2, color=color)
            ax.fill_between(years, 0, pop_data, alpha=0.2, color=color)

        ax.set_xlabel('Year')
        ax.set_ylabel('Population')
        ax.set_title('Population by Strategy', fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_monument_investment(self, ax):
        """Plot monument investment over time"""
        if not self.sim.history['avg_monument_investment']:
            ax.text(0.5, 0.5, 'No data yet', ha='center', va='center')
            return

        years = range(len(self.sim.history['avg_monument_investment']))
        ax.plot(years, self.sim.history['avg_monument_investment'],
               'b-', linewidth=2, label='Avg Monument Investment')
        ax.fill_between(years, 0, self.sim.history['avg_monument_investment'], alpha=0.3)

        ax.set_xlabel('Year')
        ax.set_ylabel('Investment')
        ax.set_title('Average Monument Investment', fontweight='bold')
        ax.grid(True, alpha=0.3)

    def _plot_summary_stats(self, ax):
        """Display summary statistics as text"""
        ax.axis('off')

        stats = self.sim.get_summary_statistics()

        text_lines = [
            f"Year: {stats['final_year']}",
            f"Total Population: {stats['total_population']:.0f}",
            f"Groups Remaining: {stats['groups_remaining']}",
            "",
            "Monument Building Groups:",
            f"  Count: {stats['Monument Building_groups']}",
            f"  Population: {stats['Monument Building_population']:.0f}",
            f"  Avg Territory: {stats['Monument Building_avg_territory']:.1f}",
            "",
            "High Reproduction Groups:",
            f"  Count: {stats['High Reproduction_groups']}",
            f"  Population: {stats['High Reproduction_population']:.0f}",
            f"  Avg Territory: {stats['High Reproduction_avg_territory']:.1f}",
            "",
            f"Total Conflicts: {stats['total_conflicts']}",
        ]

        text = '\n'.join(text_lines)
        ax.text(0.1, 0.95, text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top', fontfamily='monospace',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax.set_title('Summary Statistics', fontweight='bold')


def compare_scenarios(simulations: dict, figsize=(14, 10)):
    """
    Compare multiple simulation scenarios

    Parameters:
    -----------
    simulations: Dict mapping scenario name to SpatialSimulation instance
    """
    n_scenarios = len(simulations)
    fig, axes = plt.subplots(2, n_scenarios, figsize=figsize)

    if n_scenarios == 1:
        axes = axes.reshape(2, 1)

    for idx, (name, sim) in enumerate(simulations.items()):
        # Population comparison
        ax_pop = axes[0, idx]
        years = range(len(sim.history['population_by_strategy'][Strategy.COSTLY_SIGNALING]))

        for strategy in Strategy:
            pop_data = sim.history['population_by_strategy'][strategy]
            label = strategy.value
            color = 'blue' if strategy == Strategy.COSTLY_SIGNALING else 'red'
            ax_pop.plot(years, pop_data, label=label, linewidth=2, color=color)

        ax_pop.set_xlabel('Year')
        ax_pop.set_ylabel('Population')
        ax_pop.set_title(f'{name}\nPopulation by Strategy', fontweight='bold')
        ax_pop.legend()
        ax_pop.grid(True, alpha=0.3)

        # Conflicts
        ax_conflict = axes[1, idx]
        ax_conflict.bar(years, sim.history['conflicts_per_year'],
                       color='darkred', alpha=0.7)
        ax_conflict.set_xlabel('Year')
        ax_conflict.set_ylabel('Conflicts')
        ax_conflict.set_title('Border Conflicts', fontweight='bold')
        ax_conflict.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    return fig


def plot_phase_diagram(results: dict, figsize=(10, 8)):
    """
    Plot phase diagram showing parameter space where each strategy dominates

    Parameters:
    -----------
    results: Dict with structure {(param1_val, param2_val): {'signaling_pop': X, 'reproduction_pop': Y}}
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Extract parameter values and outcomes
    params1 = sorted(set(k[0] for k in results.keys()))
    params2 = sorted(set(k[1] for k in results.keys()))

    # Create meshgrid
    X, Y = np.meshgrid(params1, params2)
    Z = np.zeros_like(X, dtype=float)

    for i, p2 in enumerate(params2):
        for j, p1 in enumerate(params1):
            if (p1, p2) in results:
                sig_pop = results[(p1, p2)]['signaling_pop']
                rep_pop = results[(p1, p2)]['reproduction_pop']
                total = sig_pop + rep_pop
                # Z value: -1 to 1, where -1 = all reproduction, 1 = all signaling
                if total > 0:
                    Z[i, j] = (sig_pop - rep_pop) / total
                else:
                    Z[i, j] = 0

    # Plot
    im = ax.contourf(X, Y, Z, levels=20, cmap='RdBu')
    contours = ax.contour(X, Y, Z, levels=[0], colors='black', linewidths=2)
    ax.clabel(contours, inline=True, fontsize=10)

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Strategy Dominance\n(Blue=Signaling, Red=Reproduction)', rotation=270, labelpad=20)

    ax.set_xlabel('Parameter 1')
    ax.set_ylabel('Parameter 2')
    ax.set_title('Phase Diagram: Strategy Dominance', fontweight='bold', fontsize=14)

    return fig


def create_animation_frames(sim: SpatialSimulation, output_prefix='frame'):
    """
    Create animation frames from simulation

    Returns list of figure objects for each timestep
    """
    frames = []

    for year in range(len(sim.history['total_population'])):
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Territory map
        ax_map = axes[0]
        territory_display = sim.territory_map.copy().astype(float)
        n_groups = len(sim.groups)
        colors = plt.cm.tab20(np.linspace(0, 1, max(20, n_groups)))
        cmap = ListedColormap(colors)

        ax_map.imshow(territory_display.T, cmap=cmap, interpolation='nearest', origin='lower')
        ax_map.set_title(f'Year {year}')

        # Population plot
        ax_pop = axes[1]
        years = range(year + 1)
        for strategy in Strategy:
            pop_data = sim.history['population_by_strategy'][strategy][:year+1]
            label = strategy.value
            color = 'blue' if strategy == Strategy.COSTLY_SIGNALING else 'red'
            ax_pop.plot(years, pop_data, label=label, linewidth=2, color=color)

        ax_pop.set_xlabel('Year')
        ax_pop.set_ylabel('Population')
        ax_pop.set_title('Population by Strategy')
        ax_pop.legend()
        ax_pop.grid(True, alpha=0.3)

        plt.tight_layout()
        frames.append(fig)

    return frames
