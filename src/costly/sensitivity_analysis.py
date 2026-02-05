"""
Sensitivity Analysis for Phase Space Patterns
Runs parameter exploration multiple times to assess pattern stability
"""

import pickle
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

from .case_studies import get_rapa_iti_params, get_rapa_nui_params
from .parameter_exploration import explore_resource_uncertainty

print("=" * 80)
print("SENSITIVITY ANALYSIS: Testing Pattern Stability")
print("=" * 80)

# Configuration
N_RUNS = 5  # Number of independent runs
N_REPLICATES = 10  # Replicates per parameter combination (more robust)
YEARS = 100

shortfall_frequencies = list(range(5, 21, 1))  # 16 values
shortfall_magnitudes = [round(x, 2) for x in np.arange(0.2, 0.81, 0.05)]  # 13 values

print("\nConfiguration:")
print(f"  Independent runs: {N_RUNS}")
print(f"  Replicates per point: {N_REPLICATES} (vs 3 in original)")
print(f"  Parameter combinations: {len(shortfall_frequencies)} × {len(shortfall_magnitudes)} = {len(shortfall_frequencies) * len(shortfall_magnitudes)}")
print(f"  Total simulations per run: {len(shortfall_frequencies) * len(shortfall_magnitudes) * N_REPLICATES}")
print(f"  Grand total simulations: {len(shortfall_frequencies) * len(shortfall_magnitudes) * N_REPLICATES * N_RUNS}")

# Get island parameters for plotting
rapa_nui_params = get_rapa_nui_params()
rapa_iti_params = get_rapa_iti_params()
rapa_nui_freq = rapa_nui_params['shortfall_frequency']
rapa_nui_mag = rapa_nui_params['shortfall_magnitude']
rapa_iti_freq = rapa_iti_params['shortfall_frequency']
rapa_iti_mag = rapa_iti_params['shortfall_magnitude']

# Run multiple independent explorations
all_runs = []
all_dominance = []
all_total_pop = []

for run_idx in range(N_RUNS):
    print(f"\n{'='*80}")
    print(f"RUN {run_idx + 1}/{N_RUNS}")
    print(f"{'='*80}")

    # Use different seed offset for each run to ensure independence
    # Each run gets a unique range of seeds (run 0: 0-99999, run 1: 100000-199999, etc.)
    seed_offset = run_idx * 100000

    results = explore_resource_uncertainty(
        shortfall_frequencies=shortfall_frequencies,
        shortfall_magnitudes=shortfall_magnitudes,
        n_replicates=N_REPLICATES,
        years=YEARS,
        seed_offset=seed_offset
    )

    # Extract parameter grid
    freqs = sorted(set(k[0] for k in results.keys()))
    mags = sorted(set(k[1] for k in results.keys()))
    X, Y = np.meshgrid(freqs, mags)

    # Calculate metrics
    dominance = np.zeros_like(X, dtype=float)
    total_pop = np.zeros_like(X, dtype=float)

    for i, mag in enumerate(mags):
        for j, freq in enumerate(freqs):
            if (freq, mag) in results:
                sig = results[(freq, mag)]['signaling_pop_mean']
                rep = results[(freq, mag)]['reproduction_pop_mean']
                total = sig + rep
                dominance[i, j] = (sig - rep) / total if total > 0 else 0
                total_pop[i, j] = results[(freq, mag)]['total_pop_mean']

    all_runs.append(results)
    all_dominance.append(dominance)
    all_total_pop.append(total_pop)

    print(f"✓ Run {run_idx + 1} complete")

# Save results
import os

os.makedirs('data', exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
save_file = f'data/sensitivity_analysis_results_{timestamp}.pkl'
with open(save_file, 'wb') as f:
    pickle.dump({
        'all_runs': all_runs,
        'all_dominance': all_dominance,
        'all_total_pop': all_total_pop,
        'freqs': freqs,
        'mags': mags,
        'X': X,
        'Y': Y,
        'config': {
            'n_runs': N_RUNS,
            'n_replicates': N_REPLICATES,
            'years': YEARS
        }
    }, f)
print(f"\n✓ Results saved to: {save_file}")

# ============================================================================
# ANALYSIS: Calculate variability across runs
# ============================================================================
print("\n" + "=" * 80)
print("ANALYZING VARIABILITY")
print("=" * 80)

# Convert to numpy arrays for easier analysis
dominance_stack = np.stack(all_dominance)  # Shape: (N_RUNS, n_mags, n_freqs)
total_pop_stack = np.stack(all_total_pop)

# Calculate statistics across runs
dominance_mean = np.mean(dominance_stack, axis=0)
dominance_std = np.std(dominance_stack, axis=0)
dominance_min = np.min(dominance_stack, axis=0)
dominance_max = np.max(dominance_stack, axis=0)

total_pop_mean = np.mean(total_pop_stack, axis=0)
total_pop_std = np.std(total_pop_stack, axis=0)

# Find maximum variability
max_std_idx = np.unravel_index(np.argmax(dominance_std), dominance_std.shape)
max_std_freq = freqs[max_std_idx[1]]
max_std_mag = mags[max_std_idx[0]]
max_std_value = dominance_std[max_std_idx]

print("\nDominance Variability:")
print(f"  Mean std dev across all points: {np.mean(dominance_std):.4f}")
print(f"  Max std dev: {max_std_value:.4f} at freq={max_std_freq}, mag={max_std_mag:.2f}")
print(f"  Median std dev: {np.median(dominance_std):.4f}")

# Count how many points change strategy dominance across runs
strategy_switches = 0
for i in range(dominance_mean.shape[0]):
    for j in range(dominance_mean.shape[1]):
        run_values = dominance_stack[:, i, j]
        if (run_values > 0).any() and (run_values < 0).any():
            strategy_switches += 1

total_points = dominance_mean.shape[0] * dominance_mean.shape[1]
print("\nStrategy Switches:")
print(f"  Points that changed dominant strategy across runs: {strategy_switches}/{total_points} ({100*strategy_switches/total_points:.1f}%)")

# ============================================================================
# VISUALIZATION
# ============================================================================
print("\n" + "=" * 80)
print("CREATING VISUALIZATIONS")
print("=" * 80)

# Create comprehensive visualization
fig = plt.figure(figsize=(20, 12))
gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

# Row 1: Mean patterns (robust version)
ax1 = fig.add_subplot(gs[0, 0])
im1 = ax1.contourf(X, Y, dominance_mean, levels=30, cmap='RdBu', alpha=0.9)
contours = ax1.contour(X, Y, dominance_mean, levels=[0], colors='black', linewidths=2.5)
ax1.plot(rapa_nui_freq, rapa_nui_mag, 'o', markersize=20,
         markerfacecolor='blue', markeredgecolor='white', markeredgewidth=3, zorder=10)
ax1.plot(rapa_iti_freq, rapa_iti_mag, 's', markersize=20,
         markerfacecolor='red', markeredgecolor='white', markeredgewidth=3, zorder=10)
cbar1 = plt.colorbar(im1, ax=ax1)
cbar1.set_label('Mean Dominance', rotation=270, labelpad=20)
ax1.set_xlabel('Shortfall Frequency (years)')
ax1.set_ylabel('Shortfall Magnitude')
ax1.set_title(f'Mean Strategy Dominance\n({N_RUNS} runs, {N_REPLICATES} replicates each)', fontweight='bold')
ax1.grid(True, alpha=0.2)

ax2 = fig.add_subplot(gs[0, 1])
im2 = ax2.contourf(X, Y, total_pop_mean, levels=30, cmap='viridis', alpha=0.9)
ax2.plot(rapa_nui_freq, rapa_nui_mag, 'o', markersize=20,
         markerfacecolor='blue', markeredgecolor='white', markeredgewidth=3, zorder=10)
ax2.plot(rapa_iti_freq, rapa_iti_mag, 's', markersize=20,
         markerfacecolor='red', markeredgecolor='white', markeredgewidth=3, zorder=10)
cbar2 = plt.colorbar(im2, ax=ax2)
cbar2.set_label('Mean Total Population', rotation=270, labelpad=20)
ax2.set_xlabel('Shortfall Frequency (years)')
ax2.set_ylabel('Shortfall Magnitude')
ax2.set_title('Mean Total Population', fontweight='bold')
ax2.grid(True, alpha=0.2)

# Row 1, Col 3: Summary statistics
ax3 = fig.add_subplot(gs[0, 2])
ax3.axis('off')
summary_text = f"""SENSITIVITY ANALYSIS SUMMARY

Configuration:
  • {N_RUNS} independent runs
  • {N_REPLICATES} replicates per point
  • {total_points} parameter combinations
  • {len(shortfall_frequencies) * len(shortfall_magnitudes) * N_REPLICATES * N_RUNS:,} total simulations

Variability Results:
  • Mean std dev: {np.mean(dominance_std):.4f}
  • Median std dev: {np.median(dominance_std):.4f}
  • Max std dev: {max_std_value:.4f}

Strategy Stability:
  • Points that switched: {strategy_switches}/{total_points}
  • Stable points: {total_points - strategy_switches}/{total_points}
  • Stability: {100*(total_points-strategy_switches)/total_points:.1f}%

Interpretation:
  {"HIGH STABILITY" if strategy_switches < total_points * 0.1 else "MODERATE STABILITY" if strategy_switches < total_points * 0.3 else "LOW STABILITY"}
  General patterns are {"very" if strategy_switches < total_points * 0.1 else "moderately" if strategy_switches < total_points * 0.3 else "somewhat"} robust
"""
ax3.text(0.05, 0.95, summary_text, transform=ax3.transAxes,
         fontsize=9, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Row 2: Variability measures
ax4 = fig.add_subplot(gs[1, 0])
im4 = ax4.contourf(X, Y, dominance_std, levels=20, cmap='Reds', alpha=0.9)
ax4.plot(rapa_nui_freq, rapa_nui_mag, 'o', markersize=20,
         markerfacecolor='blue', markeredgecolor='white', markeredgewidth=3, zorder=10)
ax4.plot(rapa_iti_freq, rapa_iti_mag, 's', markersize=20,
         markerfacecolor='red', markeredgecolor='white', markeredgewidth=3, zorder=10)
cbar4 = plt.colorbar(im4, ax=ax4)
cbar4.set_label('Std Dev of Dominance', rotation=270, labelpad=20)
ax4.set_xlabel('Shortfall Frequency (years)')
ax4.set_ylabel('Shortfall Magnitude')
ax4.set_title('Variability Across Runs\n(Red = High Uncertainty)', fontweight='bold')
ax4.grid(True, alpha=0.2)

ax5 = fig.add_subplot(gs[1, 1])
dominance_range = dominance_max - dominance_min
im5 = ax5.contourf(X, Y, dominance_range, levels=20, cmap='Oranges', alpha=0.9)
ax5.plot(rapa_nui_freq, rapa_nui_mag, 'o', markersize=20,
         markerfacecolor='blue', markeredgecolor='white', markeredgewidth=3, zorder=10)
ax5.plot(rapa_iti_freq, rapa_iti_mag, 's', markersize=20,
         markerfacecolor='red', markeredgecolor='white', markeredgewidth=3, zorder=10)
cbar5 = plt.colorbar(im5, ax=ax5)
cbar5.set_label('Range (Max - Min)', rotation=270, labelpad=20)
ax5.set_xlabel('Shortfall Frequency (years)')
ax5.set_ylabel('Shortfall Magnitude')
ax5.set_title('Range of Dominance Values', fontweight='bold')
ax5.grid(True, alpha=0.2)

# Row 2, Col 3: All boundaries overlaid
ax6 = fig.add_subplot(gs[1, 2])
colors_boundaries = plt.cm.viridis(np.linspace(0, 1, N_RUNS))
for run_idx, (dominance, color) in enumerate(zip(all_dominance, colors_boundaries)):
    contours = ax6.contour(X, Y, dominance, levels=[0], colors=[color],
                          linewidths=2, alpha=0.7)
ax6.plot(rapa_nui_freq, rapa_nui_mag, 'o', markersize=20,
         markerfacecolor='blue', markeredgecolor='white', markeredgewidth=3, zorder=10)
ax6.plot(rapa_iti_freq, rapa_iti_mag, 's', markersize=20,
         markerfacecolor='red', markeredgecolor='white', markeredgewidth=3, zorder=10)
ax6.set_xlabel('Shortfall Frequency (years)')
ax6.set_ylabel('Shortfall Magnitude')
ax6.set_title(f'Boundary Shifts\n(All {N_RUNS} runs overlaid)', fontweight='bold')
ax6.grid(True, alpha=0.2)

# Row 3: Individual runs
for run_idx in range(min(3, N_RUNS)):
    ax = fig.add_subplot(gs[2, run_idx])
    im = ax.contourf(X, Y, all_dominance[run_idx], levels=30, cmap='RdBu', alpha=0.9)
    contours = ax.contour(X, Y, all_dominance[run_idx], levels=[0], colors='black', linewidths=2)
    ax.plot(rapa_nui_freq, rapa_nui_mag, 'o', markersize=15,
            markerfacecolor='blue', markeredgecolor='white', markeredgewidth=2, zorder=10)
    ax.plot(rapa_iti_freq, rapa_iti_mag, 's', markersize=15,
            markerfacecolor='red', markeredgecolor='white', markeredgewidth=2, zorder=10)
    plt.colorbar(im, ax=ax)
    ax.set_xlabel('Shortfall Frequency (years)')
    ax.set_ylabel('Shortfall Magnitude')
    ax.set_title(f'Run {run_idx + 1}', fontweight='bold')
    ax.grid(True, alpha=0.2)

plt.suptitle('Sensitivity Analysis: Pattern Stability Across Multiple Runs',
             fontsize=16, fontweight='bold', y=0.995)

plt.savefig(f'sensitivity_analysis_{timestamp}.png', dpi=300, bbox_inches='tight')
plt.savefig(f'sensitivity_analysis_{timestamp}.pdf', bbox_inches='tight')
print(f"✓ Saved: sensitivity_analysis_{timestamp}.[png|pdf]")

# ============================================================================
# Create robust version of Figure 2 using mean values
# ============================================================================
print("\nCreating robust Figure 2...")

fig2, axes = plt.subplots(1, 2, figsize=(16, 7))

# Panel 1: Mean Dominance
ax = axes[0]
im1 = ax.contourf(X, Y, dominance_mean, levels=30, cmap='RdBu', alpha=0.9)
contours = ax.contour(X, Y, dominance_mean, levels=[0], colors='black', linewidths=2.5)

ax.plot(rapa_nui_freq, rapa_nui_mag, 'o', markersize=22,
        markerfacecolor='blue', markeredgecolor='white', markeredgewidth=3, zorder=10)
ax.text(rapa_nui_freq - 1.5, rapa_nui_mag + 0.06, 'Rapa Nui',
        ha='center', va='bottom', fontsize=12, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue',
                 edgecolor='blue', linewidth=2, alpha=0.9))

ax.plot(rapa_iti_freq, rapa_iti_mag, 's', markersize=22,
        markerfacecolor='red', markeredgecolor='white', markeredgewidth=3, zorder=10)
ax.text(rapa_iti_freq + 1.5, rapa_iti_mag - 0.06, 'Rapa Iti',
        ha='center', va='top', fontsize=12, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral',
                 edgecolor='red', linewidth=2, alpha=0.9))

cbar1 = plt.colorbar(im1, ax=ax)
cbar1.set_label('Strategy Dominance\n(+1 = Signaling, -1 = Reproduction)',
                rotation=270, labelpad=25, fontsize=11)

ax.set_xlabel('Shortfall Frequency (years)', fontsize=13, fontweight='bold')
ax.set_ylabel('Shortfall Magnitude (proportion)', fontsize=13, fontweight='bold')
ax.set_title('Strategy Dominance', fontsize=14, fontweight='bold')
ax.set_xticks([5, 8, 10, 12, 15, 18, 20])
ax.set_yticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
ax.grid(True, alpha=0.2)

# Panel 2: Mean Population
ax = axes[1]
im2 = ax.contourf(X, Y, total_pop_mean, levels=30, cmap='viridis', alpha=0.9)

ax.plot(rapa_nui_freq, rapa_nui_mag, 'o', markersize=22,
        markerfacecolor='blue', markeredgecolor='white', markeredgewidth=3, zorder=10)
ax.plot(rapa_iti_freq, rapa_iti_mag, 's', markersize=22,
        markerfacecolor='red', markeredgecolor='white', markeredgewidth=3, zorder=10)

cbar2 = plt.colorbar(im2, ax=ax)
cbar2.set_label('Total Population', rotation=270, labelpad=20, fontsize=11)

ax.set_xlabel('Shortfall Frequency (years)', fontsize=13, fontweight='bold')
ax.set_ylabel('Shortfall Magnitude (proportion)', fontsize=13, fontweight='bold')
ax.set_title('Total Population\n(Lower with Signaling)', fontsize=14, fontweight='bold')
ax.set_xticks([5, 8, 10, 12, 15, 18, 20])
ax.set_yticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
ax.grid(True, alpha=0.2)

plt.suptitle(f'Robust Phase Space ({N_RUNS} runs × {N_REPLICATES} replicates = {N_RUNS * N_REPLICATES}× averaging)',
             fontsize=16, fontweight='bold', y=0.98)

plt.tight_layout()
fig2.savefig('figure_2_environmental_phase_space_ROBUST.png', dpi=300, bbox_inches='tight')
fig2.savefig('figure_2_environmental_phase_space_ROBUST.pdf', bbox_inches='tight')
print("✓ Saved: figure_2_environmental_phase_space_ROBUST.[png|pdf]")

print("\n" + "=" * 80)
print("SENSITIVITY ANALYSIS COMPLETE")
print("=" * 80)
print("\nFiles created:")
print(f"  1. {save_file}")
print(f"  2. sensitivity_analysis_{timestamp}.png/pdf")
print("  3. figure_2_environmental_phase_space_ROBUST.png/pdf")
print("\nConclusion:")
if strategy_switches < total_points * 0.1:
    print("  ✓ HIGH STABILITY: Patterns are very robust across runs")
    print("    The general phase space structure is reliable for interpretation")
elif strategy_switches < total_points * 0.3:
    print("  ~ MODERATE STABILITY: Patterns are generally stable with some boundary shifts")
    print("    Core patterns are reliable, but exact boundaries may vary slightly")
else:
    print("  ! LOW STABILITY: Patterns show significant variation across runs")
    print("    Consider increasing n_replicates further for more robust results")
