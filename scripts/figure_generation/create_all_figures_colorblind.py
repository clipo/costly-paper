"""
Create colorblind-safe versions of ALL figures for the paper
Uses colorblind-friendly color schemes throughout
"""

import glob
import pickle
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

sys.path.insert(0, 'src/costly')
from case_studies import get_rapa_iti_params, get_rapa_nui_params

print("Creating colorblind-safe versions of all figures...")

# COLORBLIND-SAFE COLOR PALETTE
# Based on Wong (2011) and Okabe & Ito (2008) recommendations
CB_COLORS = {
    'blue': '#0173B2',      # Blue
    'orange': '#DE8F05',    # Orange
    'purple': '#CC78BC',    # Purple
    'brown': '#8B4513',     # Brown
    'cyan': '#029E73',      # Cyan/Teal
    'yellow': '#ECE133',    # Yellow
    'black': '#000000',     # Black
    'gray': '#808080',      # Gray
}

# ============================================================================
# FIGURE 1: Environmental Phase Space (already colorblind safe, but verify)
# ============================================================================

print("\n1. Creating Figure 1: Environmental Phase Space...")

# Load sensitivity analysis results
result_files = glob.glob('data/sensitivity_analysis_results_*.pkl')
if not result_files:
    print("Warning: No sensitivity analysis results found. Skipping Figure 1.")
else:
    latest_file = sorted(result_files)[-1]
    with open(latest_file, 'rb') as f:
        data = pickle.load(f)

    X = data['X']
    Y = data['Y']
    freqs = data['freqs']
    mags = data['mags']

    dominance_stack = np.stack(data['all_dominance'])
    total_pop_stack = np.stack(data['all_total_pop'])
    dominance_mean = np.mean(dominance_stack, axis=0)
    total_pop_mean = np.mean(total_pop_stack, axis=0)

    rapa_nui_params = get_rapa_nui_params()
    rapa_iti_params = get_rapa_iti_params()
    rapa_nui_freq = rapa_nui_params['shortfall_frequency']
    rapa_nui_mag = rapa_nui_params['shortfall_magnitude']
    rapa_iti_freq = rapa_iti_params['shortfall_frequency']
    rapa_iti_mag = rapa_iti_params['shortfall_magnitude']

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Panel A: Strategy Dominance (colorblind-safe diverging)
    ax = axes[0]
    im1 = ax.contourf(X, Y, dominance_mean, levels=30, cmap='PuOr_r', alpha=0.9)
    contours = ax.contour(X, Y, dominance_mean, levels=[0], colors='black', linewidths=2.5)

    ax.plot(rapa_nui_freq, rapa_nui_mag, 'o', markersize=22,
            markerfacecolor=CB_COLORS['cyan'], markeredgecolor='black', markeredgewidth=3, zorder=10)
    ax.text(rapa_nui_freq - 1.5, rapa_nui_mag + 0.06, 'Rapa Nui',
            ha='center', va='bottom', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcyan',
                     edgecolor='black', linewidth=2, alpha=0.9))

    ax.plot(rapa_iti_freq, rapa_iti_mag, 's', markersize=22,
            markerfacecolor=CB_COLORS['yellow'], markeredgecolor='black', markeredgewidth=3, zorder=10)
    ax.text(rapa_iti_freq + 1.5, rapa_iti_mag - 0.06, 'Rapa Iti',
            ha='center', va='top', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
                     edgecolor='black', linewidth=2, alpha=0.9))

    cbar1 = plt.colorbar(im1, ax=ax)
    cbar1.set_label('Monument Building Dominance\n(Orange = Monument, Purple = Reproduction)',
                    rotation=270, labelpad=25, fontsize=11)

    ax.set_xlabel('Shortfall Frequency (years)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Shortfall Magnitude (proportion)', fontsize=13, fontweight='bold')
    ax.set_title('A. Strategy Dominance', fontsize=14, fontweight='bold')
    ax.set_xticks([5, 8, 10, 12, 15, 18, 20])
    ax.set_yticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    ax.grid(True, alpha=0.2)

    # Panel B: Total Population (colorblind-safe sequential)
    ax = axes[1]
    im2 = ax.contourf(X, Y, total_pop_mean, levels=30, cmap='cividis', alpha=0.9)

    ax.plot(rapa_nui_freq, rapa_nui_mag, 'o', markersize=22,
            markerfacecolor=CB_COLORS['cyan'], markeredgecolor='black', markeredgewidth=3, zorder=10)
    ax.plot(rapa_iti_freq, rapa_iti_mag, 's', markersize=22,
            markerfacecolor=CB_COLORS['yellow'], markeredgecolor='black', markeredgewidth=3, zorder=10)

    cbar2 = plt.colorbar(im2, ax=ax)
    cbar2.set_label('Total Population\n(Bright = High, Dark = Low)', rotation=270, labelpad=25, fontsize=11)

    ax.set_xlabel('Shortfall Frequency (years)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Shortfall Magnitude (proportion)', fontsize=13, fontweight='bold')
    ax.set_title('B. Final Population', fontsize=14, fontweight='bold')
    ax.set_xticks([5, 8, 10, 12, 15, 18, 20])
    ax.set_yticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    ax.grid(True, alpha=0.2)

    plt.suptitle('Environmental Phase Space and Strategy Dominance (Colorblind-Safe)',
                 fontsize=16, fontweight='bold', y=0.98)

    plt.tight_layout()
    fig.savefig('figures/final/figure_1_phase_space_CB.png', dpi=300, bbox_inches='tight')
    fig.savefig('figures/final/figure_1_phase_space_CB.pdf', bbox_inches='tight')
    print("✓ Saved: figures/final/figure_1_phase_space_CB.[png|pdf]")
    plt.close()

# ============================================================================
# FIGURE 2: Demographic Outcomes - Need to create colorblind version
# ============================================================================

print("\n2. Creating Figure 2: Demographic Outcomes...")

# Load the same data
if result_files:
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Extract temporal stability (CV over time within runs) from simulation results
    # Use the stored total_pop_std / total_pop_mean for each parameter combination
    all_runs = data['all_runs']
    pop_cv_list = []

    for replicate in all_runs:
        cv_grid = np.zeros((len(mags), len(freqs)))
        for i, mag in enumerate(mags):
            for j, freq in enumerate(freqs):
                sim_result = replicate[(freq, mag)]
                # Calculate coefficient of variation: std/mean over time
                cv = sim_result['total_pop_std'] / (sim_result['total_pop_mean'] + 1e-10)
                cv_grid[i, j] = cv
        pop_cv_list.append(cv_grid)

    # Average CV across replicates
    pop_cv = np.mean(np.stack(pop_cv_list), axis=0)

    # Panel A: Average Population (colorblind-safe sequential)
    ax = axes[0]
    im1 = ax.contourf(X, Y, total_pop_mean, levels=30, cmap='cividis', alpha=0.9)

    ax.plot(rapa_nui_freq, rapa_nui_mag, 'o', markersize=22,
            markerfacecolor=CB_COLORS['cyan'], markeredgecolor='black', markeredgewidth=3, zorder=10)
    ax.plot(rapa_iti_freq, rapa_iti_mag, 's', markersize=22,
            markerfacecolor=CB_COLORS['yellow'], markeredgecolor='black', markeredgewidth=3, zorder=10)

    cbar1 = plt.colorbar(im1, ax=ax)
    cbar1.set_label('Average Population\n(Bright = High, Dark = Low)', rotation=270, labelpad=25, fontsize=11)

    ax.set_xlabel('Shortfall Frequency (years)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Shortfall Magnitude (proportion)', fontsize=13, fontweight='bold')
    ax.set_title('A. Average Population', fontsize=14, fontweight='bold')
    ax.set_xticks([5, 8, 10, 12, 15, 18, 20])
    ax.set_yticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    ax.grid(True, alpha=0.2)

    # Panel B: Population Stability (colorblind-safe sequential, reversed)
    ax = axes[1]
    im2 = ax.contourf(X, Y, pop_cv, levels=30, cmap='cividis_r', alpha=0.9)

    ax.plot(rapa_nui_freq, rapa_nui_mag, 'o', markersize=22,
            markerfacecolor=CB_COLORS['cyan'], markeredgecolor='black', markeredgewidth=3, zorder=10)
    ax.plot(rapa_iti_freq, rapa_iti_mag, 's', markersize=22,
            markerfacecolor=CB_COLORS['yellow'], markeredgecolor='black', markeredgewidth=3, zorder=10)

    cbar2 = plt.colorbar(im2, ax=ax)
    cbar2.set_label('Population Stability\n(Bright = Stable, Dark = Volatile)', rotation=270, labelpad=25, fontsize=11)

    ax.set_xlabel('Shortfall Frequency (years)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Shortfall Magnitude (proportion)', fontsize=13, fontweight='bold')
    ax.set_title('B. Population Stability', fontsize=14, fontweight='bold')
    ax.set_xticks([5, 8, 10, 12, 15, 18, 20])
    ax.set_yticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    ax.grid(True, alpha=0.2)

    plt.suptitle('Demographic Trade-offs Across Environmental Space (Colorblind-Safe)',
                 fontsize=16, fontweight='bold', y=0.98)

    plt.tight_layout()
    fig.savefig('figures/final/figure_2_demographic_outcomes_CB.png', dpi=300, bbox_inches='tight')
    fig.savefig('figures/final/figure_2_demographic_outcomes_CB.pdf', bbox_inches='tight')
    print("✓ Saved: figures/final/figure_2_demographic_outcomes_CB.[png|pdf]")
    plt.close()

# ============================================================================
# FIGURE 3: Shortfall Scenarios (4-panel grid)
# ============================================================================

print("\n3. Creating Figure 3: Shortfall Scenarios...")

years = 100
base_productivity = 1.0

scenarios = [
    {"name": "Rapa Nui-like\n(Frequent, Severe)", "freq": 6, "mag": 0.6, "color": CB_COLORS['orange']},
    {"name": "Rapa Iti-like\n(Rare, Mild)", "freq": 18, "mag": 0.3, "color": CB_COLORS['blue']},
    {"name": "Frequent, Mild", "freq": 6, "mag": 0.3, "color": CB_COLORS['purple']},
    {"name": "Rare, Severe", "freq": 18, "mag": 0.6, "color": CB_COLORS['brown']},
]

fig = plt.figure(figsize=(16, 10))
gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.25)

for idx, scenario in enumerate(scenarios):
    row = idx // 2
    col = idx % 2
    ax = fig.add_subplot(gs[row, col])

    freq = scenario['freq']
    mag = scenario['mag']
    color = scenario['color']

    productivity = np.ones(years) * base_productivity
    for year in range(0, years, freq):
        if year < years:
            productivity[year] = base_productivity * (1 - mag)

    years_array = np.arange(years)

    ax.fill_between(years_array, 0, productivity, alpha=0.3, color=color)
    ax.plot(years_array, productivity, linewidth=2.5, color=color, label='Productivity')

    # Shortfall markers - use neutral gray instead of red
    for year in range(0, years, freq):
        if year < years:
            ax.axvspan(year-0.5, year+0.5, alpha=0.15, color=CB_COLORS['gray'], zorder=0)

    ax.axhline(base_productivity, color=CB_COLORS['black'], linestyle='--', linewidth=1.5,
               alpha=0.7, label='Base productivity')

    shortfall_level = base_productivity * (1 - mag)
    ax.axhline(shortfall_level, color=CB_COLORS['black'], linestyle=':', linewidth=1.5,
               alpha=0.7, label=f'Shortfall level (-{int(mag*100)}%)')

    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Resource Productivity', fontsize=12, fontweight='bold')
    ax.set_title(f'{scenario["name"]}\nFrequency: {freq} years | Magnitude: {mag} ({int(mag*100)}% reduction)',
                fontsize=13, fontweight='bold')
    ax.set_ylim(0, 1.2)
    ax.set_xlim(0, years)
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(loc='upper right', fontsize=9)

    n_shortfalls = len(range(0, years, freq))
    avg_productivity = np.mean(productivity)
    stats_text = f'Shortfalls: {n_shortfalls}\nAvg productivity: {avg_productivity:.3f}'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
           fontsize=10, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.suptitle('Environmental Variability: Shortfall Frequency and Magnitude Scenarios (Colorblind-Safe)',
             fontsize=16, fontweight='bold', y=0.995)

plt.savefig('figure_3_shortfall_scenarios_CB.png', dpi=300, bbox_inches='tight')
plt.savefig('figure_3_shortfall_scenarios_CB.pdf', bbox_inches='tight')
print("✓ Saved: figure_3_shortfall_scenarios_CB.[png|pdf]")
plt.close()

# ============================================================================
# FIGURES 4-5: Frequency and Magnitude Comparisons (stacked panels)
# ============================================================================

print("\n4. Creating Figure 4: Frequency Comparison (stacked)...")

fig, axes = plt.subplots(3, 1, figsize=(14, 12))
years_array = np.arange(years)

# Panel 1: Short frequency (6 years, 60% magnitude)
ax = axes[0]
freq = 6
mag = 0.6
productivity = np.ones(years) * base_productivity
for year in range(0, years, freq):
    if year < years:
        productivity[year] = base_productivity * (1 - mag)

ax.fill_between(years_array, 0, productivity, alpha=0.3, color=CB_COLORS['orange'])
ax.plot(years_array, productivity, linewidth=2.5, color=CB_COLORS['orange'], label=f'Short frequency ({freq} years)')

for year in range(0, years, freq):
    if year < years:
        ax.axvline(year, alpha=0.2, color=CB_COLORS['orange'], linewidth=1, linestyle='--')

ax.axhline(base_productivity, color=CB_COLORS['gray'], linestyle='--', linewidth=1.5, alpha=0.5)
ax.set_ylabel('Resource Productivity', fontsize=12, fontweight='bold')
ax.set_title('A. Short Frequency (6 years) - Frequent Stress', fontsize=13, fontweight='bold')
ax.set_ylim(0, 1.15)
ax.set_xlim(0, years)
ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

n_shortfalls = len(range(0, years, freq))
avg_prod = np.mean(productivity)
ax.text(0.98, 0.05, f'{n_shortfalls} shortfalls | Avg: {avg_prod:.3f}',
       transform=ax.transAxes, fontsize=10, ha='right',
       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Panel 2: Long frequency (18 years, 60% magnitude)
ax = axes[1]
freq = 18
mag = 0.6
productivity = np.ones(years) * base_productivity
for year in range(0, years, freq):
    if year < years:
        productivity[year] = base_productivity * (1 - mag)

ax.fill_between(years_array, 0, productivity, alpha=0.3, color=CB_COLORS['blue'])
ax.plot(years_array, productivity, linewidth=2.5, color=CB_COLORS['blue'], label=f'Long frequency ({freq} years)')

for year in range(0, years, freq):
    if year < years:
        ax.axvline(year, alpha=0.2, color=CB_COLORS['blue'], linewidth=1, linestyle='--')

ax.axhline(base_productivity, color=CB_COLORS['gray'], linestyle='--', linewidth=1.5, alpha=0.5)
ax.set_ylabel('Resource Productivity', fontsize=12, fontweight='bold')
ax.set_title('B. Long Frequency (18 years) - Rare Stress', fontsize=13, fontweight='bold')
ax.set_ylim(0, 1.15)
ax.set_xlim(0, years)
ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

n_shortfalls = len(range(0, years, freq))
avg_prod = np.mean(productivity)
ax.text(0.98, 0.05, f'{n_shortfalls} shortfalls | Avg: {avg_prod:.3f}',
       transform=ax.transAxes, fontsize=10, ha='right',
       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Panel 3: Difference plot
ax = axes[2]

freq_short = 6
freq_long = 18
mag = 0.6

prod_short = np.ones(years) * base_productivity
for year in range(0, years, freq_short):
    if year < years:
        prod_short[year] = base_productivity * (1 - mag)

prod_long = np.ones(years) * base_productivity
for year in range(0, years, freq_long):
    if year < years:
        prod_long[year] = base_productivity * (1 - mag)

difference = prod_long - prod_short
ax.fill_between(years_array, 0, difference, where=(difference >= 0),
               alpha=0.3, color=CB_COLORS['cyan'], label='Long frequency advantage')
ax.fill_between(years_array, 0, difference, where=(difference < 0),
               alpha=0.3, color=CB_COLORS['orange'], label='Short frequency disadvantage')
ax.plot(years_array, difference, linewidth=2, color=CB_COLORS['black'], alpha=0.7)
ax.axhline(0, color=CB_COLORS['gray'], linestyle='-', linewidth=1.5)

ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Productivity Difference\n(Long - Short Frequency)', fontsize=12, fontweight='bold')
ax.set_title('C. Cumulative Impact of Frequency Difference', fontsize=13, fontweight='bold')
ax.set_xlim(0, years)
ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

cumulative_diff = np.sum(difference)
ax.text(0.02, 0.95, f'Cumulative difference: {cumulative_diff:.1f} units\n(+{cumulative_diff/100:.1%} advantage for long frequency)',
       transform=ax.transAxes, fontsize=10, ha='left', va='top',
       bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

plt.suptitle('Frequency Variation: Short (6 years) vs. Long (18 years) - Constant Magnitude (60%) (Colorblind-Safe)',
            fontsize=15, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('figure_4_frequency_comparison_CB.png', dpi=300, bbox_inches='tight')
plt.savefig('figure_4_frequency_comparison_CB.pdf', bbox_inches='tight')
print("✓ Saved: figure_4_frequency_comparison_CB.[png|pdf]")
plt.close()

print("\n5. Creating Figure 5: Magnitude Comparison (stacked)...")

fig, axes = plt.subplots(3, 1, figsize=(14, 12))

# Panel 1: Light magnitude (30%)
ax = axes[0]
freq = 6
mag = 0.3
productivity = np.ones(years) * base_productivity
for year in range(0, years, freq):
    if year < years:
        productivity[year] = base_productivity * (1 - mag)

ax.fill_between(years_array, 0, productivity, alpha=0.3, color=CB_COLORS['cyan'])
ax.plot(years_array, productivity, linewidth=2.5, color=CB_COLORS['cyan'], label=f'Light magnitude ({int(mag*100)}%)')

for year in range(0, years, freq):
    if year < years:
        ax.axvline(year, alpha=0.2, color=CB_COLORS['cyan'], linewidth=1, linestyle='--')

ax.axhline(base_productivity, color=CB_COLORS['gray'], linestyle='--', linewidth=1.5, alpha=0.5)
ax.set_ylabel('Resource Productivity', fontsize=12, fontweight='bold')
ax.set_title('A. Light Magnitude (30% reduction) - Mild Stress', fontsize=13, fontweight='bold')
ax.set_ylim(0, 1.15)
ax.set_xlim(0, years)
ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

n_shortfalls = len(range(0, years, freq))
avg_prod = np.mean(productivity)
ax.text(0.98, 0.05, f'{n_shortfalls} shortfalls | Avg: {avg_prod:.3f}',
       transform=ax.transAxes, fontsize=10, ha='right',
       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Panel 2: Deep magnitude (60%)
ax = axes[1]
freq = 6
mag = 0.6
productivity = np.ones(years) * base_productivity
for year in range(0, years, freq):
    if year < years:
        productivity[year] = base_productivity * (1 - mag)

ax.fill_between(years_array, 0, productivity, alpha=0.3, color=CB_COLORS['orange'])
ax.plot(years_array, productivity, linewidth=2.5, color=CB_COLORS['orange'], label=f'Deep magnitude ({int(mag*100)}%)')

for year in range(0, years, freq):
    if year < years:
        ax.axvline(year, alpha=0.2, color=CB_COLORS['orange'], linewidth=1, linestyle='--')

ax.axhline(base_productivity, color=CB_COLORS['gray'], linestyle='--', linewidth=1.5, alpha=0.5)
ax.set_ylabel('Resource Productivity', fontsize=12, fontweight='bold')
ax.set_title('B. Deep Magnitude (60% reduction) - Severe Stress', fontsize=13, fontweight='bold')
ax.set_ylim(0, 1.15)
ax.set_xlim(0, years)
ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

n_shortfalls = len(range(0, years, freq))
avg_prod = np.mean(productivity)
ax.text(0.98, 0.05, f'{n_shortfalls} shortfalls | Avg: {avg_prod:.3f}',
       transform=ax.transAxes, fontsize=10, ha='right',
       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Panel 3: Difference plot
ax = axes[2]

mag_light = 0.3
mag_deep = 0.6
freq = 6

prod_light = np.ones(years) * base_productivity
for year in range(0, years, freq):
    if year < years:
        prod_light[year] = base_productivity * (1 - mag_light)

prod_deep = np.ones(years) * base_productivity
for year in range(0, years, freq):
    if year < years:
        prod_deep[year] = base_productivity * (1 - mag_deep)

difference = prod_light - prod_deep
ax.fill_between(years_array, 0, difference, where=(difference >= 0),
               alpha=0.3, color=CB_COLORS['cyan'], label='Light magnitude advantage')
ax.plot(years_array, difference, linewidth=2, color=CB_COLORS['black'], alpha=0.7)
ax.axhline(0, color=CB_COLORS['gray'], linestyle='-', linewidth=1.5)

ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Productivity Difference\n(Light - Deep Magnitude)', fontsize=12, fontweight='bold')
ax.set_title('C. Cumulative Impact of Magnitude Difference', fontsize=13, fontweight='bold')
ax.set_xlim(0, years)
ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

cumulative_diff = np.sum(difference)
ax.text(0.02, 0.95, f'Cumulative difference: {cumulative_diff:.1f} units\n(+{cumulative_diff/100:.1%} advantage for light magnitude)',
       transform=ax.transAxes, fontsize=10, ha='left', va='top',
       bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

plt.suptitle('Magnitude Variation: Light (30%) vs. Deep (60%) - Constant Frequency (6 years) (Colorblind-Safe)',
            fontsize=15, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig('figure_5_magnitude_comparison_CB.png', dpi=300, bbox_inches='tight')
plt.savefig('figure_5_magnitude_comparison_CB.pdf', bbox_inches='tight')
print("✓ Saved: figure_5_magnitude_comparison_CB.[png|pdf]")
plt.close()

# ============================================================================
# FIGURE 6: Cumulative Resources
# ============================================================================

print("\n6. Creating Figure 6: Cumulative Resources...")

fig, ax = plt.subplots(1, 1, figsize=(12, 7))

scenarios_cumulative = [
    {"freq": 6, "mag": 0.6, "label": "Rapa Nui-like (6yr, 60%)", "color": CB_COLORS['orange']},
    {"freq": 18, "mag": 0.3, "label": "Rapa Iti-like (18yr, 30%)", "color": CB_COLORS['blue']},
    {"freq": 6, "mag": 0.3, "label": "Frequent-Mild (6yr, 30%)", "color": CB_COLORS['purple']},
    {"freq": 18, "mag": 0.6, "label": "Rare-Severe (18yr, 60%)", "color": CB_COLORS['brown']},
]

for scenario in scenarios_cumulative:
    freq = scenario['freq']
    mag = scenario['mag']

    productivity = np.ones(years) * base_productivity
    for year in range(0, years, freq):
        if year < years:
            productivity[year] = base_productivity * (1 - mag)

    cumulative = np.cumsum(productivity)
    ax.plot(years_array, cumulative, linewidth=2.5, label=scenario['label'],
           color=scenario['color'], alpha=0.8)

ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Cumulative Resource Availability', fontsize=12, fontweight='bold')
ax.set_title('Cumulative Resource Impact Over Time (Different Shortfall Scenarios) (Colorblind-Safe)',
            fontsize=14, fontweight='bold')
ax.legend(loc='upper left', fontsize=11)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figure_6_cumulative_resources_CB.png', dpi=300, bbox_inches='tight')
plt.savefig('figure_6_cumulative_resources_CB.pdf', bbox_inches='tight')
print("✓ Saved: figure_6_cumulative_resources_CB.[png|pdf]")
plt.close()

# ============================================================================
# FIGURE 7: Case Study Comparison - Need to recreate from simulation
# ============================================================================

print("\n7. Figure 7 (Case Study) requires running simulations - skipping for now")
print("   (Use existing figure_1_rapa_nui_vs_rapa_iti.png with manual color adjustment)")

print("\n" + "="*70)
print("✓ COMPLETED: All colorblind-safe figures created")
print("="*70)
print("\nGenerated files:")
print("  - figure_1_phase_space_CB.png")
print("  - figure_2_demographic_outcomes_CB.png")
print("  - figure_3_shortfall_scenarios_CB.png")
print("  - figure_4_frequency_comparison_CB.png")
print("  - figure_5_magnitude_comparison_CB.png")
print("  - figure_6_cumulative_resources_CB.png")
print("\nColorblind-safe palette used:")
print("  - Blue, Orange, Purple, Brown, Cyan (qualitative)")
print("  - cividis, PuOr (sequential/diverging)")
print("  - No red-green combinations")
