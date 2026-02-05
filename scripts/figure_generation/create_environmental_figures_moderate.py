"""
Create all environmental variability figures with moderate parameters
- Frequency: 5 years vs 20 years
- Magnitude: 25% vs 70%
- Duration scales with magnitude (mild=1yr, severe=3yr)
- Consistent across all figures
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

print("Creating environmental variability figures with moderate parameters...")

# Simulation parameters
years = 100
base_productivity = 1.0
years_array = np.arange(years)


def calculate_shortfall_duration(magnitude):
    """Duration scales with magnitude: mild=1yr, severe=3yr

    Using a gentler multiplier so shortfalls don't overlap when frequent.
    This ensures Panel A shows distinct events rather than constant shortfall.
    """
    return max(1, int(1 + magnitude * 2.5))


def create_productivity_with_duration(years, freq, mag, base=1.0):
    """Create productivity array where shortfalls have duration based on magnitude"""
    productivity = np.ones(years) * base
    duration = calculate_shortfall_duration(mag)

    year = 0
    while year < years:
        # Apply shortfall for duration years
        for d in range(duration):
            if year + d < years:
                productivity[year + d] = base * (1 - mag)
        year += freq

    return productivity, duration

# Color scheme (colorblind-safe)
COLORS = {
    'rapa_nui': '#E69F00',  # Orange
    'rapa_iti': '#0072B2',  # Blue
    'freq_mild': '#CC79A7',  # Pink
    'rare_severe': '#999999',  # Gray
    'green': '#009E73',  # Teal-green
}

# ============================================================================
# FIGURE 5: Shortfall Scenarios (4-panel) - Combines frequency, magnitude, and duration
# ============================================================================
print("Creating Figure 5: Shortfall Scenarios...")

# Calculate durations for each magnitude
dur_severe = calculate_shortfall_duration(0.80)  # 3 years
dur_mild = calculate_shortfall_duration(0.20)    # 1 year

scenarios = [
    {"name": "Frequent + Severe", "subtitle": f"Frequent (6yr) × Severe (60%) × Long ({dur_severe}yr)",
     "freq": 6, "mag": 0.60, "color": COLORS['rapa_nui']},
    {"name": "Rare + Mild", "subtitle": f"Rare (30yr) × Mild (30%) × Brief ({dur_mild}yr)",
     "freq": 30, "mag": 0.30, "color": COLORS['rapa_iti']},
    {"name": "Frequent + Mild", "subtitle": f"Frequent (6yr) × Mild (30%) × Brief ({dur_mild}yr)",
     "freq": 6, "mag": 0.30, "color": COLORS['freq_mild']},
    {"name": "Rare + Severe", "subtitle": f"Rare (30yr) × Severe (60%) × Long ({dur_severe}yr)",
     "freq": 30, "mag": 0.60, "color": COLORS['rare_severe']},
]

fig = plt.figure(figsize=(16, 12))
gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.25)

panel_labels = ['A', 'B', 'C', 'D']

for idx, scenario in enumerate(scenarios):
    row = idx // 2
    col = idx % 2
    ax = fig.add_subplot(gs[row, col])

    freq = scenario['freq']
    mag = scenario['mag']
    color = scenario['color']

    # Use duration-aware productivity calculation
    productivity, duration = create_productivity_with_duration(years, freq, mag, base_productivity)

    ax.fill_between(years_array, 0, productivity, alpha=0.3, color=color)
    ax.plot(years_array, productivity, linewidth=2.5, color=color, label='Productivity')


    ax.axhline(base_productivity, color='gray', linestyle='--', linewidth=1.5, alpha=0.7, label='Base (100%)')
    shortfall_level = base_productivity * (1 - mag)
    ax.axhline(shortfall_level, color='darkred', linestyle=':', linewidth=1.5, alpha=0.7,
               label=f'Shortfall level ({int((1-mag)*100)}%)')

    ax.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax.set_ylabel('Resource Productivity', fontsize=11, fontweight='bold')

    # Panel label and title
    ax.text(0.02, 1.02, f'{panel_labels[idx]}. {scenario["name"]}',
            transform=ax.transAxes, fontsize=13, fontweight='bold', va='bottom')

    ax.set_ylim(0, 1.2)
    ax.set_xlim(0, years)
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(loc='upper right', fontsize=9)

    # Stats box with all three dimensions clearly shown
    n_shortfall_events = years // freq
    shortfall_years = n_shortfall_events * duration
    avg_productivity = np.mean(productivity)
    cumulative_loss = mag * duration * n_shortfall_events

    stats_text = (f'Frequency: every {freq} years ({n_shortfall_events} events/century)\n'
                  f'Magnitude: {int(mag*100)}% depth\n'
                  f'Duration: {duration} year{"s" if duration > 1 else ""} per event\n'
                  f'Total shortfall years: {shortfall_years}/century')
    ax.text(0.02, 0.97, stats_text, transform=ax.transAxes,
           fontsize=9, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor=color, linewidth=2))

# No suptitle - keep figure clean for publication
plt.savefig('figures/final/Figure_5_shortfall_scenarios.png', dpi=300, bbox_inches='tight')
print("  Saved: figures/final/Figure_5_shortfall_scenarios.png")
plt.close()

# ============================================================================
# FIGURE 3: Frequency Comparison (3-panel) - Explain frequency dimension first
# ============================================================================
print("Creating Figure 3: Frequency Comparison...")

fig, axes = plt.subplots(3, 1, figsize=(14, 12))

# Panel A: Short frequency (6 years, 60% magnitude - severe, 3yr duration)
ax = axes[0]
freq, mag = 6, 0.60
productivity, duration = create_productivity_with_duration(years, freq, mag, base_productivity)

ax.fill_between(years_array, 0, productivity, alpha=0.3, color=COLORS['rapa_nui'])
ax.plot(years_array, productivity, linewidth=2.5, color=COLORS['rapa_nui'], label=f'Frequent ({freq}yr cycle, {duration}yr duration)')
ax.axhline(base_productivity, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
ax.set_ylabel('Resource Productivity', fontsize=12, fontweight='bold')
ax.text(0.02, 0.98, 'A', transform=ax.transAxes, fontsize=14, fontweight='bold', va='top')
ax.set_ylim(0, 1.15)
ax.set_xlim(0, years)
ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.3, axis='y')
n_events = years // freq
shortfall_years = n_events * duration
avg_prod = np.mean(productivity)
ax.text(0.98, 0.05, f'{n_events} events × {duration}yr = {shortfall_years} shortfall years | Avg: {avg_prod:.3f}',
       transform=ax.transAxes, fontsize=10, ha='right',
       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Panel B: Long frequency (30 years, 60% magnitude - severe, 3yr duration)
ax = axes[1]
freq, mag = 30, 0.60
productivity, duration = create_productivity_with_duration(years, freq, mag, base_productivity)

ax.fill_between(years_array, 0, productivity, alpha=0.3, color=COLORS['rapa_iti'])
ax.plot(years_array, productivity, linewidth=2.5, color=COLORS['rapa_iti'], label=f'Rare ({freq}yr cycle, {duration}yr duration)')
ax.axhline(base_productivity, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
ax.set_ylabel('Resource Productivity', fontsize=12, fontweight='bold')
ax.text(0.02, 0.98, 'B', transform=ax.transAxes, fontsize=14, fontweight='bold', va='top')
ax.set_ylim(0, 1.15)
ax.set_xlim(0, years)
ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.3, axis='y')
n_events = years // freq
shortfall_years = n_events * duration
avg_prod = np.mean(productivity)
ax.text(0.98, 0.05, f'{n_events} events × {duration}yr = {shortfall_years} shortfall years | Avg: {avg_prod:.3f}',
       transform=ax.transAxes, fontsize=10, ha='right',
       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Panel C: Difference
ax = axes[2]
freq_short, freq_long, mag = 6, 30, 0.60

prod_short, _ = create_productivity_with_duration(years, freq_short, mag, base_productivity)
prod_long, _ = create_productivity_with_duration(years, freq_long, mag, base_productivity)

difference = prod_long - prod_short
ax.fill_between(years_array, 0, difference, where=(difference >= 0),
               alpha=0.3, color=COLORS['green'], label='Long frequency advantage')
ax.fill_between(years_array, 0, difference, where=(difference < 0),
               alpha=0.3, color='red', label='Short frequency disadvantage')
ax.plot(years_array, difference, linewidth=2, color='black', alpha=0.7)
ax.axhline(0, color='gray', linestyle='-', linewidth=1.5)
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Productivity Difference\n(Long - Short Frequency)', fontsize=12, fontweight='bold')
ax.text(0.02, 0.98, 'C', transform=ax.transAxes, fontsize=14, fontweight='bold', va='top')
ax.set_xlim(0, years)
ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

cumulative_diff = np.sum(difference)
ax.text(0.02, 0.95, f'Cumulative difference: {cumulative_diff:.1f} units\n(+{cumulative_diff/100:.1%} advantage for long frequency)',
       transform=ax.transAxes, fontsize=10, ha='left', va='top',
       bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# No suptitle - keep figure clean for publication
plt.tight_layout()
plt.savefig('figures/final/Figure_3_frequency_comparison.png', dpi=300, bbox_inches='tight')
print("  Saved: figures/final/Figure_3_frequency_comparison.png")
plt.close()

# ============================================================================
# FIGURE 4: Magnitude Comparison (2x2 panel) - Shows magnitude affects BOTH depth AND duration
# ============================================================================
print("Creating Figure 4: Magnitude Comparison...")

from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(16, 12))
gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.25)

# Panel A: Mild magnitude time series (top left)
ax = fig.add_subplot(gs[0, 0])
freq, mag = 6, 0.30
productivity, duration = create_productivity_with_duration(years, freq, mag, base_productivity)

ax.fill_between(years_array, 0, productivity, alpha=0.3, color=COLORS['green'])
ax.plot(years_array, productivity, linewidth=2.5, color=COLORS['green'])
ax.axhline(base_productivity, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
ax.set_ylabel('Resource Productivity', fontsize=12, fontweight='bold')
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.text(0.02, 0.98, 'A. Mild Shortfalls (30% magnitude)', transform=ax.transAxes,
        fontsize=12, fontweight='bold', va='top')
ax.set_ylim(0, 1.15)
ax.set_xlim(0, years)
ax.grid(True, alpha=0.3, axis='y')
n_events = years // freq
shortfall_years = n_events * duration
avg_prod = np.mean(productivity)
ax.text(0.98, 0.05, f'Depth: {int(mag*100)}% | Duration: {duration} year\n{shortfall_years} shortfall years/century',
       transform=ax.transAxes, fontsize=10, ha='right',
       bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

# Panel B: Severe magnitude time series (top right)
ax = fig.add_subplot(gs[0, 1])
freq, mag = 6, 0.60
productivity, duration = create_productivity_with_duration(years, freq, mag, base_productivity)

ax.fill_between(years_array, 0, productivity, alpha=0.3, color=COLORS['rapa_nui'])
ax.plot(years_array, productivity, linewidth=2.5, color=COLORS['rapa_nui'])
ax.axhline(base_productivity, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)
ax.set_ylabel('Resource Productivity', fontsize=12, fontweight='bold')
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.text(0.02, 0.98, 'B. Severe Shortfalls (60% magnitude)', transform=ax.transAxes,
        fontsize=12, fontweight='bold', va='top')
ax.set_ylim(0, 1.15)
ax.set_xlim(0, years)
ax.grid(True, alpha=0.3, axis='y')
n_events = years // freq
shortfall_years = n_events * duration
avg_prod = np.mean(productivity)
ax.text(0.98, 0.05, f'Depth: {int(mag*100)}% | Duration: {duration} years\n{shortfall_years} shortfall years/century',
       transform=ax.transAxes, fontsize=10, ha='right',
       bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

# Panel C: Single shortfall comparison - showing BOTH depth AND duration (bottom left)
ax = fig.add_subplot(gs[1, 0])
ax.text(0.02, 0.98, 'C. How Magnitude Affects Both Depth AND Duration', transform=ax.transAxes,
        fontsize=12, fontweight='bold', va='top')

# Show a single shortfall event at different magnitudes
event_years = np.arange(-1, 8)
magnitudes_to_show = [
    (0.30, 'Mild (30%)', COLORS['green']),
    (0.45, 'Moderate (45%)', COLORS['freq_mild']),
    (0.60, 'Severe (60%)', COLORS['rapa_nui']),
]

for mag, label, color in magnitudes_to_show:
    dur = calculate_shortfall_duration(mag)
    prod = np.ones(len(event_years)) * base_productivity
    # Apply shortfall starting at year 0
    for d in range(dur):
        idx = np.where(event_years == d)[0]
        if len(idx) > 0:
            prod[idx[0]] = base_productivity * (1 - mag)

    ax.plot(event_years, prod, linewidth=3, color=color, marker='o', markersize=8,
            label=f'{label}: {dur}yr duration')
    # Shade the shortfall area
    ax.fill_between(event_years, base_productivity, prod, alpha=0.15, color=color)

ax.axhline(base_productivity, color='gray', linestyle='--', linewidth=2, alpha=0.7)
ax.axvline(0, color='black', linestyle=':', linewidth=1.5, alpha=0.5, label='Shortfall onset')
ax.set_xlabel('Years from shortfall onset', fontsize=12, fontweight='bold')
ax.set_ylabel('Resource Productivity', fontsize=12, fontweight='bold')
ax.set_ylim(0, 1.15)
ax.set_xlim(-1, 7)
ax.legend(loc='lower right', fontsize=10)
ax.grid(True, alpha=0.3)

# Add annotations for depth and duration
ax.annotate('', xy=(-0.3, 0.2), xytext=(-0.3, 1.0),
            arrowprops=dict(arrowstyle='<->', color='black', lw=2))
ax.text(-0.7, 0.6, 'DEPTH', fontsize=10, ha='center', va='center', fontweight='bold', rotation=90)

ax.annotate('', xy=(0, 0.08), xytext=(3, 0.08),
            arrowprops=dict(arrowstyle='<->', color='black', lw=2))
ax.text(1.5, 0.02, 'DURATION', fontsize=10, ha='center', va='center', fontweight='bold')

# Panel D: Cumulative impact showing the multiplicative effect (bottom right)
ax = fig.add_subplot(gs[1, 1])
ax.text(0.02, 0.98, 'D. Cumulative Impact per Shortfall Event', transform=ax.transAxes,
        fontsize=12, fontweight='bold', va='top')

# Calculate total productivity loss for each magnitude
mag_values = [0.30, 0.40, 0.50, 0.60]
depths = []
durations = []
total_losses = []
colors_bars = []

color_map = {0.30: COLORS['green'], 0.40: COLORS['freq_mild'],
             0.50: COLORS['rapa_nui'], 0.60: COLORS['rapa_nui']}

for mag in mag_values:
    dur = calculate_shortfall_duration(mag)
    loss = mag * dur  # Total productivity lost = depth × duration
    depths.append(mag)
    durations.append(dur)
    total_losses.append(loss)
    colors_bars.append(color_map.get(mag, '#999999'))

x_pos = np.arange(len(mag_values))
width = 0.35

# Stacked bar: depth component and duration multiplier effect
bars1 = ax.bar(x_pos, depths, width, label='Depth (magnitude)', color=colors_bars, edgecolor='black', alpha=0.7)

# Show total loss as text
for i, (x, loss, dur, depth) in enumerate(zip(x_pos, total_losses, durations, depths)):
    ax.text(x, depth + 0.05, f'×{dur}yr = {loss:.1f}', ha='center', va='bottom',
            fontsize=11, fontweight='bold')

ax.set_xticks(x_pos)
ax.set_xticklabels([f'{int(m*100)}%' for m in mag_values], fontsize=11)
ax.set_xlabel('Shortfall Magnitude', fontsize=12, fontweight='bold')
ax.set_ylabel('Productivity Drop (depth)', fontsize=12, fontweight='bold')
ax.set_ylim(0, 1.1)
ax.grid(True, alpha=0.3, axis='y')

# Add explanation box
ax.text(0.5, 0.85, 'Total Impact = Depth × Duration\nSevere shortfalls are DOUBLY punishing',
       transform=ax.transAxes, fontsize=11, ha='center', va='top',
       bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, edgecolor='orange'))

plt.savefig('figures/final/Figure_4_magnitude_comparison.png', dpi=300, bbox_inches='tight')
print("  Saved: figures/final/Figure_4_magnitude_comparison.png")
plt.close()

print("\nAll environmental figures created with updated parameters:")
print("  Figure 3: Frequency Comparison (explains frequency dimension)")
print("  Figure 4: Magnitude Comparison (explains magnitude dimension)")
print("  Figure 5: Shortfall Scenarios (combines all three dimensions)")
print("  - Frequency: 6 years (frequent) vs 30 years (rare)")
print("  - Magnitude affects both DEPTH and DURATION:")
print("    - Mild (30%): 30% productivity drop, 1 year duration")
print("    - Severe (60%): 60% productivity drop, 2-3 year duration")
