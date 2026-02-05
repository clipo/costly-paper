"""
Create Figure 2: Model Dynamics Overview

Illustrates the key model mechanics:
- Panel A: Annual cycle flowchart (5 phases)
- Panel B: Conflict probability matrix by strategy pairing
- Panel C: Resource allocation comparison between strategies

Output: figures/final/figure_2_model_dynamics.png
"""

import os

import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch

# Colorblind-safe colors
CB_COLORS = {
    'blue': '#0173B2',      # Monument builders
    'red': '#D55E00',       # High reproduction
    'green': '#029E73',     # Positive/resources
    'orange': '#DE8F05',    # Warnings/costs
    'purple': '#CC78BC',    # Neutral
    'yellow': '#ECE133',    # Highlights
    'gray': '#949494',      # Neutral elements
    'black': '#000000',
}

def create_annual_cycle_panel(ax):
    """Create flowchart showing the 5 phases of the annual cycle"""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('A. Annual Simulation Cycle', fontsize=12, fontweight='bold', loc='left')

    # Phase boxes - arranged in a cycle
    phases = [
        (5, 9, 'Phase 1:\nResource\nProduction', CB_COLORS['green']),
        (8.5, 6.5, 'Phase 2:\nResource\nAllocation', CB_COLORS['blue']),
        (7, 3, 'Phase 3:\nPopulation\nDynamics', CB_COLORS['purple']),
        (3, 3, 'Phase 4:\nTerritorial\nCompetition', CB_COLORS['red']),
        (1.5, 6.5, 'Phase 5:\nExtinction &\nInheritance', CB_COLORS['orange']),
    ]

    box_width = 2.2
    box_height = 1.4

    # Draw boxes
    for x, y, text, color in phases:
        box = FancyBboxPatch((x - box_width/2, y - box_height/2),
                              box_width, box_height,
                              boxstyle="round,pad=0.05,rounding_size=0.2",
                              facecolor=color, edgecolor='black', linewidth=1.5,
                              alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=8,
                fontweight='bold', color='white',
                path_effects=[pe.withStroke(linewidth=2, foreground='black')])

    # Draw arrows connecting phases (clockwise)
    arrow_style = "Simple,tail_width=0.5,head_width=4,head_length=4"
    kw = dict(arrowstyle=arrow_style, color=CB_COLORS['gray'], lw=2)

    # Phase 1 -> 2
    ax.annotate("", xy=(7.3, 7.5), xytext=(6.2, 8.5),
                arrowprops=dict(arrowstyle='->', color=CB_COLORS['gray'], lw=2))
    # Phase 2 -> 3
    ax.annotate("", xy=(7.8, 4.2), xytext=(8.2, 5.8),
                arrowprops=dict(arrowstyle='->', color=CB_COLORS['gray'], lw=2))
    # Phase 3 -> 4
    ax.annotate("", xy=(4.2, 3), xytext=(5.8, 3),
                arrowprops=dict(arrowstyle='->', color=CB_COLORS['gray'], lw=2))
    # Phase 4 -> 5
    ax.annotate("", xy=(2.2, 5.8), xytext=(2.8, 4.2),
                arrowprops=dict(arrowstyle='->', color=CB_COLORS['gray'], lw=2))
    # Phase 5 -> 1 (loop back)
    ax.annotate("", xy=(3.8, 8.5), xytext=(2.7, 7.5),
                arrowprops=dict(arrowstyle='->', color=CB_COLORS['gray'], lw=2))

    # Add "Year t" and "Year t+1" labels
    ax.text(5, 0.8, 'Repeat each simulated year', ha='center', va='center',
            fontsize=9, style='italic', color=CB_COLORS['gray'])


def create_conflict_matrix_panel(ax):
    """Create conflict probability matrix showing strategy interactions"""
    ax.set_title('B. Conflict Probability When Groups Share a Border', fontsize=12, fontweight='bold', loc='left')

    # Create matrix data
    # When two groups share a border, this is the probability that conflict occurs
    # MB-MB: 25% (mutual signaling deters conflict)
    # All others: 100% (no deterrence effect)
    conflict_probs = np.array([
        [0.25, 1.0],  # MB vs MB, MB vs HR
        [1.0, 1.0],   # HR vs MB, HR vs HR
    ])

    # Create heatmap
    im = ax.imshow(conflict_probs, cmap='RdYlGn_r', vmin=0, vmax=1, aspect='auto')

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Probability of\nConflict Occurring', fontsize=9)

    # Set ticks and labels
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['Monument\nBuilder', 'High\nReproduction'], fontsize=9)
    ax.set_yticklabels(['Monument\nBuilder', 'High\nReproduction'], fontsize=9)
    ax.set_xlabel('Neighboring Group', fontsize=10)
    ax.set_ylabel('Focal Group', fontsize=10)

    # Add text annotations with clearer labels
    for i in range(2):
        for j in range(2):
            prob = conflict_probs[i, j]
            text_color = 'white' if prob > 0.5 else 'black'
            if prob == 0.25:
                label = '25%\n(low)'
            else:
                label = '100%\n(high)'
            ax.text(j, i, label, ha='center', va='center',
                   fontsize=10, fontweight='bold', color=text_color)

    # Add explanatory text below (positioned within the panel area)
    ax.text(0.5, -0.18, 'When BOTH groups are monument builders,\nmutual signaling deters conflict (25% vs 100%)',
            transform=ax.transAxes, ha='center', va='top',
            fontsize=9, style='italic', color=CB_COLORS['blue'],
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, edgecolor=CB_COLORS['blue']))


def create_resource_allocation_panel(ax):
    """Create bar chart comparing resource allocation between strategies"""
    ax.set_title('C. Resource Allocation by Strategy', fontsize=12, fontweight='bold', loc='left')

    strategies = ['Monument\nBuilders', 'High\nReproduction']
    x = np.arange(len(strategies))
    width = 0.35

    # Data
    monument_cost = [35, 0]  # % to monuments
    population_support = [65, 100]  # % to population (base)
    reproduction_bonus = [0, 40]  # Additional bonus for HR

    # Stacked bars
    bars1 = ax.bar(x, monument_cost, width, label='Monument Investment',
                   color=CB_COLORS['orange'], edgecolor='black')
    bars2 = ax.bar(x, population_support, width, bottom=monument_cost,
                   label='Population Support', color=CB_COLORS['green'], edgecolor='black')

    # Add reproduction bonus as hatched extension for HR
    ax.bar(x[1], reproduction_bonus[1], width, bottom=100,
           label='Reproduction Bonus (+40%)', color=CB_COLORS['red'],
           edgecolor='black', hatch='///', alpha=0.7)

    ax.set_ylabel('Resource Allocation (%)', fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(strategies, fontsize=10)
    ax.set_ylim(0, 160)
    ax.set_yticks([0, 25, 50, 75, 100, 140])
    ax.set_yticklabels(['0', '25', '50', '75', '100', '140'])

    # Add horizontal line at 100%
    ax.axhline(y=100, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax.text(1.5, 102, 'Base resources', fontsize=8, va='bottom', ha='right', alpha=0.7)

    # Add annotations
    ax.annotate('35% cost\n(lower births)', xy=(0, 17.5), ha='center', va='center',
                fontsize=8, color='white', fontweight='bold')
    ax.annotate('65%', xy=(0, 67.5), ha='center', va='center',
                fontsize=8, color='white', fontweight='bold')
    ax.annotate('100%', xy=(1, 50), ha='center', va='center',
                fontsize=8, color='white', fontweight='bold')
    ax.annotate('+40%\nbonus', xy=(1, 120), ha='center', va='center',
                fontsize=8, color='white', fontweight='bold')

    ax.legend(loc='upper left', fontsize=8, framealpha=0.9)
    ax.grid(axis='y', alpha=0.3)


def create_conflict_outcome_panel(ax):
    """Create diagram showing conflict outcome factors"""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('D. Conflict Outcome Determinants', fontsize=12, fontweight='bold', loc='left')

    # Central "Conflict Outcome" box
    center_box = FancyBboxPatch((3.5, 4), 3, 2,
                                 boxstyle="round,pad=0.05,rounding_size=0.3",
                                 facecolor=CB_COLORS['purple'], edgecolor='black',
                                 linewidth=2, alpha=0.9)
    ax.add_patch(center_box)
    ax.text(5, 5, 'Conflict\nOutcome', ha='center', va='center', fontsize=11,
            fontweight='bold', color='white')

    # Factor boxes
    factors = [
        (1.5, 8, 'Population\nSize', CB_COLORS['green'], 'Larger groups\nmore likely to win'),
        (8.5, 8, 'Monument\nInvestment', CB_COLORS['blue'], 'Signals commitment,\ndeters attacks'),
        (1.5, 1.5, 'Stochastic\nElement', CB_COLORS['gray'], 'Historical\ncontingency'),
        (8.5, 1.5, 'Loser\nMortality', CB_COLORS['red'], '20-25%\npopulation loss'),
    ]

    box_w, box_h = 2.4, 1.3
    for x, y, title, color, subtitle in factors:
        box = FancyBboxPatch((x - box_w/2, y - box_h/2), box_w, box_h,
                              boxstyle="round,pad=0.03,rounding_size=0.15",
                              facecolor=color, edgecolor='black', linewidth=1.5,
                              alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y + 0.15, title, ha='center', va='center', fontsize=9,
                fontweight='bold', color='white',
                path_effects=[pe.withStroke(linewidth=1.5, foreground='black')])
        ax.text(x, y - 0.35, subtitle, ha='center', va='center', fontsize=7,
                color='white', style='italic',
                path_effects=[pe.withStroke(linewidth=1, foreground='black')])

    # Draw arrows to center
    arrow_props = dict(arrowstyle='->', color=CB_COLORS['gray'], lw=2)
    # Top left
    ax.annotate("", xy=(3.8, 5.5), xytext=(2.2, 7.2), arrowprops=arrow_props)
    # Top right
    ax.annotate("", xy=(6.2, 5.5), xytext=(7.8, 7.2), arrowprops=arrow_props)
    # Bottom left
    ax.annotate("", xy=(3.8, 4.5), xytext=(2.2, 2.3), arrowprops=arrow_props)
    # Bottom right (outcome arrow)
    ax.annotate("", xy=(7.8, 2.3), xytext=(6.2, 4.5), arrowprops=arrow_props)


def main():
    print("Creating Figure 2: Model Dynamics Overview...")

    # Create figure with 2x2 grid
    fig = plt.figure(figsize=(14, 12))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Panel A: Annual cycle (top left)
    ax1 = fig.add_subplot(gs[0, 0])
    create_annual_cycle_panel(ax1)

    # Panel B: Conflict matrix (top right)
    ax2 = fig.add_subplot(gs[0, 1])
    create_conflict_matrix_panel(ax2)

    # Panel C: Resource allocation (bottom left)
    ax3 = fig.add_subplot(gs[1, 0])
    create_resource_allocation_panel(ax3)

    # Panel D: Conflict outcomes (bottom right)
    ax4 = fig.add_subplot(gs[1, 1])
    create_conflict_outcome_panel(ax4)

    plt.tight_layout()

    # Save
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'final')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, 'Figure_7_model_dynamics.png')
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")

    plt.close()


if __name__ == '__main__':
    main()
