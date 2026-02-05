"""
Create Figure 10: Temporal Dynamics by Environmental Condition
Uses the ACTUAL ABM simulation with multiple replicates to show envelopes
"""

import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import matplotlib.pyplot as plt
import numpy as np

from costly.simulation import SpatialSimulation, Strategy

print("Creating Figure 10: Temporal Dynamics (using actual ABM with replicates)...")

# Colors (colorblind-safe)
COLOR_MONUMENT = '#0072B2'  # Blue
COLOR_REPRO = '#D55E00'     # Red-orange
COLOR_SHORTFALL = '#FFCCCC'  # Light red for shortfall bands

N_REPLICATES = 100  # Number of simulation replicates for envelopes
YEARS = 200

def run_replicates(params, n_reps=N_REPLICATES, years=YEARS):
    """Run multiple simulation replicates and collect population trajectories"""
    mb_trajectories = []
    hr_trajectories = []
    conflict_trajectories = []

    for rep in range(n_reps):
        # Change seed for each replicate
        rep_params = params.copy()
        rep_params['seed'] = params.get('seed', 42) + rep * 100

        sim = SpatialSimulation(**rep_params)
        sim.initialize_groups({Strategy.COSTLY_SIGNALING: 0.5, Strategy.HIGH_REPRODUCTION: 0.5})
        sim.run(years)

        mb_pop = sim.history['population_by_strategy'][Strategy.COSTLY_SIGNALING]
        hr_pop = sim.history['population_by_strategy'][Strategy.HIGH_REPRODUCTION]
        conflicts = sim.history['conflicts_per_year']

        mb_trajectories.append(mb_pop)
        hr_trajectories.append(hr_pop)
        conflict_trajectories.append(conflicts)

        if (rep + 1) % 5 == 0:
            print(f"    Completed {rep + 1}/{n_reps} replicates...")

    return {
        'mb_trajectories': np.array(mb_trajectories),
        'hr_trajectories': np.array(hr_trajectories),
        'conflict_trajectories': np.array(conflict_trajectories),
        'shortfall_freq': params['shortfall_frequency'],
        'shortfall_mag': params['shortfall_magnitude']
    }

# Define parameters
# STRESSED (Rapa Nui-like): Frequent severe shortfalls
# - Monument builders should dominate due to conflict reduction
# - Lower overall population due to harsh conditions
stressed_params = {
    'grid_size': (40, 40),
    'n_groups': 20,
    'base_productivity': 0.7,      # Lower base productivity
    'shortfall_frequency': 6,      # Frequent shortfalls
    'shortfall_magnitude': 0.6,    # Severe
    'monument_cost': 0.35,
    'reproduction_bonus': 0.5,     # HR gets bigger bonus
    'conflict_mortality': 0.25,
    'signaling_conflict_reduction': 0.75,
    'carrying_capacity_per_cell': 8.0,
    'shortfall_conflict_multiplier': 3.0,  # More conflict during shortfalls
    'seed': 42
}

# STABLE (Rapa Iti-like): Rare mild shortfalls
# - High reproduction should dominate due to breeding advantage
# - Higher overall population due to good conditions
stable_params = {
    'grid_size': (40, 40),
    'n_groups': 20,
    'base_productivity': 1.2,      # Higher base productivity
    'shortfall_frequency': 30,     # Rare shortfalls
    'shortfall_magnitude': 0.3,    # Mild
    'monument_cost': 0.35,
    'reproduction_bonus': 0.7,     # HR gets BIGGER bonus in good times
    'conflict_mortality': 0.15,    # Lower conflict mortality (less deadly)
    'signaling_conflict_reduction': 0.5,  # Signaling less valuable in stable times
    'carrying_capacity_per_cell': 15.0,
    'shortfall_conflict_multiplier': 1.5,  # Less conflict amplification during rare shortfalls
    'seed': 42
}

# Run simulations
print(f"  Running stressed conditions ({N_REPLICATES} replicates)...")
stressed_data = run_replicates(stressed_params)

print(f"  Running stable conditions ({N_REPLICATES} replicates)...")
stable_data = run_replicates(stable_params)

# Calculate statistics
def calc_stats(trajectories):
    """Calculate mean and confidence interval"""
    mean = np.mean(trajectories, axis=0)
    std = np.std(trajectories, axis=0)
    # Use +/- 1 std for envelope
    lower = mean - std
    upper = mean + std
    return mean, lower, upper

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
years_array = np.arange(YEARS)

# ============================================================================
# Top row: Stressed conditions (Rapa Nui-like)
# ============================================================================

# Panel A: Population by strategy (stressed)
ax = axes[0, 0]

# Calculate stats
mb_mean, mb_lower, mb_upper = calc_stats(stressed_data['mb_trajectories'])
hr_mean, hr_lower, hr_upper = calc_stats(stressed_data['hr_trajectories'])

# Add shortfall bands
shortfall_years = [y for y in range(YEARS) if y > 0 and y % stressed_data['shortfall_freq'] == 0]
duration = max(1, int(1 + stressed_data['shortfall_mag'] * 2.5))
for i, year in enumerate(shortfall_years):
    label = 'Shortfall period' if i == 0 else None
    ax.axvspan(year, min(year + duration, YEARS), alpha=0.2, color=COLOR_SHORTFALL, label=label)

# Plot envelopes
ax.fill_between(years_array, mb_lower, mb_upper, color=COLOR_MONUMENT, alpha=0.3)
ax.fill_between(years_array, hr_lower, hr_upper, color=COLOR_REPRO, alpha=0.3)

# Plot means
ax.plot(years_array, mb_mean, color=COLOR_MONUMENT, linewidth=2.5, label='Monument Building')
ax.plot(years_array, hr_mean, color=COLOR_REPRO, linewidth=2.5, label='High Reproduction')

ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Population', fontsize=11)
ax.set_title('STRESSED CONDITIONS (Rapa Nui-like)', fontsize=12, fontweight='bold', color='#8B0000')
ax.text(0.02, 0.98, 'A', transform=ax.transAxes, fontsize=14, fontweight='bold', va='top')
ax.legend(loc='upper left', fontsize=9)
ax.set_xlim(0, YEARS)
ax.grid(True, alpha=0.3)

# Add annotations
mb_final = mb_mean[-1]
hr_final = hr_mean[-1]
total_final = mb_final + hr_final
ax.text(0.98, 0.15, f'Final: MB={mb_final:.0f}, HR={hr_final:.0f}\nMB dominance: {mb_final/total_final*100:.0f}%\nTotal pop: {total_final:.0f}',
        transform=ax.transAxes, fontsize=9, ha='right', va='bottom',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

# Panel B: Conflicts per year (stressed)
ax = axes[0, 1]

conflict_mean, conflict_lower, conflict_upper = calc_stats(stressed_data['conflict_trajectories'])

# Add shortfall bands
for year in shortfall_years:
    ax.axvspan(year, min(year + duration, YEARS), alpha=0.2, color=COLOR_SHORTFALL)

# Plot envelope and mean
ax.fill_between(years_array, conflict_lower, conflict_upper, color='gray', alpha=0.3)
ax.plot(years_array, conflict_mean, color='black', linewidth=2)

ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Conflicts per Year', fontsize=11)
ax.set_title('CONFLICT RATE (Stressed)', fontsize=12, fontweight='bold', color='#8B0000')
ax.text(0.02, 0.98, 'B', transform=ax.transAxes, fontsize=14, fontweight='bold', va='top')
ax.set_xlim(0, YEARS)
ax.grid(True, alpha=0.3, axis='y')

total_conflicts = np.sum(conflict_mean)
ax.text(0.98, 0.85, f'Total: {total_conflicts:.0f} conflicts\n(mean across {N_REPLICATES} runs)',
        transform=ax.transAxes, fontsize=9, ha='right', va='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, edgecolor='orange'))

# ============================================================================
# Bottom row: Stable conditions (Rapa Iti-like)
# ============================================================================

# Panel C: Population by strategy (stable)
ax = axes[1, 0]

mb_mean_s, mb_lower_s, mb_upper_s = calc_stats(stable_data['mb_trajectories'])
hr_mean_s, hr_lower_s, hr_upper_s = calc_stats(stable_data['hr_trajectories'])

# Add shortfall bands
shortfall_years_s = [y for y in range(YEARS) if y > 0 and y % stable_data['shortfall_freq'] == 0]
duration_s = max(1, int(1 + stable_data['shortfall_mag'] * 2.5))
for i, year in enumerate(shortfall_years_s):
    label = 'Shortfall period' if i == 0 else None
    ax.axvspan(year, min(year + duration_s, YEARS), alpha=0.2, color=COLOR_SHORTFALL, label=label)

# Plot envelopes
ax.fill_between(years_array, mb_lower_s, mb_upper_s, color=COLOR_MONUMENT, alpha=0.3)
ax.fill_between(years_array, hr_lower_s, hr_upper_s, color=COLOR_REPRO, alpha=0.3)

# Plot means
ax.plot(years_array, mb_mean_s, color=COLOR_MONUMENT, linewidth=2.5, label='Monument Building')
ax.plot(years_array, hr_mean_s, color=COLOR_REPRO, linewidth=2.5, label='High Reproduction')

ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Population', fontsize=11)
ax.set_title('STABLE CONDITIONS (Rapa Iti-like)', fontsize=12, fontweight='bold', color='#006400')
ax.text(0.02, 0.98, 'C', transform=ax.transAxes, fontsize=14, fontweight='bold', va='top')
ax.legend(loc='upper left', fontsize=9)
ax.set_xlim(0, YEARS)
ax.grid(True, alpha=0.3)

# Add annotations
mb_final_s = mb_mean_s[-1]
hr_final_s = hr_mean_s[-1]
total_final_s = mb_final_s + hr_final_s
ax.text(0.98, 0.15, f'Final: MB={mb_final_s:.0f}, HR={hr_final_s:.0f}\nHR dominance: {hr_final_s/total_final_s*100:.0f}%\nTotal pop: {total_final_s:.0f}',
        transform=ax.transAxes, fontsize=9, ha='right', va='bottom',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

# Panel D: Conflicts per year (stable)
ax = axes[1, 1]

conflict_mean_s, conflict_lower_s, conflict_upper_s = calc_stats(stable_data['conflict_trajectories'])

# Add shortfall bands
for year in shortfall_years_s:
    ax.axvspan(year, min(year + duration_s, YEARS), alpha=0.2, color=COLOR_SHORTFALL)

# Plot envelope and mean
ax.fill_between(years_array, conflict_lower_s, conflict_upper_s, color='gray', alpha=0.3)
ax.plot(years_array, conflict_mean_s, color='black', linewidth=2)

ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Conflicts per Year', fontsize=11)
ax.set_title('CONFLICT RATE (Stable)', fontsize=12, fontweight='bold', color='#006400')
ax.text(0.02, 0.98, 'D', transform=ax.transAxes, fontsize=14, fontweight='bold', va='top')
ax.set_xlim(0, YEARS)
ax.grid(True, alpha=0.3, axis='y')

total_conflicts_s = np.sum(conflict_mean_s)
ax.text(0.98, 0.85, f'Total: {total_conflicts_s:.0f} conflicts\n(mean across {N_REPLICATES} runs)',
        transform=ax.transAxes, fontsize=9, ha='right', va='top',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9, edgecolor='green'))

plt.tight_layout()

# Save
output_path = 'figures/final/Figure_10_temporal_dynamics.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"\n  Saved: {output_path}")

# Print summary
print("\n" + "="*60)
print("SIMULATION SUMMARY")
print("="*60)
print(f"\nStressed Conditions (freq={stressed_params['shortfall_frequency']}, mag={stressed_params['shortfall_magnitude']}):")
print(f"  Monument builders final: {mb_final:.0f} ± {np.std(stressed_data['mb_trajectories'][:,-1]):.0f}")
print(f"  High reproduction final: {hr_final:.0f} ± {np.std(stressed_data['hr_trajectories'][:,-1]):.0f}")
print(f"  MB dominance: {mb_final/total_final*100:.1f}%")
print(f"  Total population: {total_final:.0f}")
print(f"  Total conflicts: {total_conflicts:.0f}")

print(f"\nStable Conditions (freq={stable_params['shortfall_frequency']}, mag={stable_params['shortfall_magnitude']}):")
print(f"  Monument builders final: {mb_final_s:.0f} ± {np.std(stable_data['mb_trajectories'][:,-1]):.0f}")
print(f"  High reproduction final: {hr_final_s:.0f} ± {np.std(stable_data['hr_trajectories'][:,-1]):.0f}")
print(f"  HR dominance: {hr_final_s/total_final_s*100:.1f}%")
print(f"  Total population: {total_final_s:.0f}")
print(f"  Total conflicts: {total_conflicts_s:.0f}")

print("\nExpected patterns:")
print("  - Stressed: MB dominates, lower total population (Rapa Nui)")
print("  - Stable: HR dominates, higher total population (Rapa Iti)")

plt.close()
