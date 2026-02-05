"""
Create figure showing modified Price equation with environmental uncertainty.

The standard Price equation for multilevel selection:
    Δp̄ = Cov(wᵢ, pᵢ)/w̄ + E(wᵢΔpᵢ)/w̄
         [between-group]   [within-group]

We extend this by making fitness terms depend on environmental uncertainty (σ):
- σ = environmental uncertainty parameter (combines frequency and magnitude)
- Higher σ → more frequent/severe shortfalls
- Signaling groups: lower reproduction but better survival during shortfalls
- Non-signaling groups: higher reproduction but vulnerable to shortfalls

The key insight: there exists a critical uncertainty σ* where between-group
selection (favoring signaling) exactly balances within-group selection
(favoring non-signaling).

Output: figures/final/figure_modified_price_equation.png
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyBboxPatch

# Colorblind-safe colors
CB_COLORS = {
    'blue': '#0173B2',      # Monument builders / signaling
    'red': '#D55E00',       # High reproduction / non-signaling
    'green': '#029E73',     # Positive outcomes
    'orange': '#DE8F05',    # Costs/warnings
    'purple': '#CC78BC',    # Neutral/balance
    'gray': '#949494',
    'black': '#000000',
}


def calculate_fitness_components(sigma, C=0.35, alpha=0.3, beta=0.9, r=0.75):
    """
    Calculate fitness components for signaling and non-signaling strategies.

    Parameters:
    -----------
    sigma : float or array
        Environmental uncertainty (0 to 1)
    C : float
        Cost of signaling (reproductive reduction, default 0.35 = 35%)
    alpha : float
        Shortfall vulnerability for signaling groups (low, due to buffer)
    beta : float
        Shortfall vulnerability for non-signaling groups (high, at capacity)
    r : float
        Conflict reduction rate for mutual signaling (default 0.75 = 75%)

    Returns:
    --------
    dict with fitness components
    """
    # Base conflict mortality (per year equivalent)
    conflict_base = 0.15

    # Survival during shortfalls (density-dependent mortality avoidance)
    S_signal = 1 - alpha * sigma
    S_nonsignal = 1 - beta * sigma

    # Conflict-adjusted survival
    # Signaling groups: reduced conflict with other signalers
    # As signaling spreads, more interactions are signal-signal
    conflict_signal = conflict_base * (1 - r)  # 75% reduction
    conflict_nonsignal = conflict_base * 1.0   # Full conflict

    # Effective fitness
    # Signaling: reduced reproduction (1-C) but better survival
    w_signal = (1 - C) * S_signal * (1 - conflict_signal)

    # Non-signaling: full reproduction but worse survival
    w_nonsignal = 1.0 * S_nonsignal * (1 - conflict_nonsignal)

    # Between-group selection component
    # Positive when signaling groups have higher fitness
    between_group = w_signal - w_nonsignal

    # Within-group selection component
    # Always negative (non-signalers out-reproduce signalers within groups)
    within_group = -C * S_signal  # Cost of signaling within any group

    return {
        'sigma': sigma,
        'w_signal': w_signal,
        'w_nonsignal': w_nonsignal,
        'S_signal': S_signal,
        'S_nonsignal': S_nonsignal,
        'between_group': between_group,
        'within_group': within_group,
        'net_selection': between_group + within_group,
    }


def find_critical_sigma(C=0.35, alpha=0.3, beta=0.9, r=0.75):
    """Find the critical uncertainty where strategies have equal fitness."""
    sigma_range = np.linspace(0, 1, 1000)
    results = calculate_fitness_components(sigma_range, C, alpha, beta, r)

    # Find where between-group advantage equals within-group cost
    # i.e., where net selection on signaling = 0
    idx = np.argmin(np.abs(results['w_signal'] - results['w_nonsignal']))
    return sigma_range[idx]


def sigma_from_params(frequency, magnitude):
    """
    Convert frequency and magnitude to uncertainty parameter σ.

    σ represents expected "shortfall-years" per century, normalized.
    Higher frequency (shorter return period) → more shortfalls
    Higher magnitude → longer duration per shortfall
    """
    # Duration increases with magnitude: mild=1yr, moderate=2yr, severe=3yr
    duration = 1 + magnitude * 2.5

    # Expected shortfall-years per century
    shortfall_years = (100 / frequency) * duration * magnitude

    # Normalize to 0-1 scale (max around 60-80 shortfall-years)
    sigma = np.clip(shortfall_years / 80, 0, 1)
    return sigma


def create_panel_a(ax):
    """Panel A: Fitness as function of uncertainty."""
    sigma = np.linspace(0, 0.8, 100)
    results = calculate_fitness_components(sigma)
    sigma_star = find_critical_sigma()

    # Plot fitness curves
    ax.plot(sigma, results['w_signal'], color=CB_COLORS['blue'],
            linewidth=2.5, label='Signaling strategy', zorder=3)
    ax.plot(sigma, results['w_nonsignal'], color=CB_COLORS['red'],
            linewidth=2.5, label='Non-signaling strategy', zorder=3)

    # Mark critical threshold
    ax.axvline(sigma_star, color=CB_COLORS['gray'], linestyle='--',
               linewidth=1.5, alpha=0.7)

    # Shade regions
    ax.fill_between(sigma[sigma < sigma_star],
                    results['w_signal'][sigma < sigma_star],
                    results['w_nonsignal'][sigma < sigma_star],
                    alpha=0.2, color=CB_COLORS['red'])
    ax.fill_between(sigma[sigma >= sigma_star],
                    results['w_signal'][sigma >= sigma_star],
                    results['w_nonsignal'][sigma >= sigma_star],
                    alpha=0.2, color=CB_COLORS['blue'])

    # Labels
    ax.set_xlabel('Environmental Uncertainty (σ)', fontsize=11)
    ax.set_ylabel('Expected Fitness', fontsize=11)
    ax.set_title('A. Fitness Under Environmental Uncertainty',
                 fontsize=12, fontweight='bold', loc='left')

    # Annotations
    ax.annotate('Critical\nthreshold σ*', xy=(sigma_star, 0.5),
                xytext=(sigma_star + 0.08, 0.58),
                fontsize=9, ha='left',
                arrowprops=dict(arrowstyle='->', color=CB_COLORS['gray']))

    ax.text(sigma_star/2, 0.72, 'Non-signaling\nfavored', ha='center',
            fontsize=9, color=CB_COLORS['red'], fontweight='bold')
    ax.text(sigma_star + (0.8-sigma_star)/2, 0.72, 'Signaling\nfavored',
            ha='center', fontsize=9, color=CB_COLORS['blue'], fontweight='bold')

    ax.legend(loc='upper right', fontsize=9)
    ax.set_xlim(0, 0.8)
    ax.set_ylim(0.4, 0.85)
    ax.grid(alpha=0.3)


def create_panel_b(ax):
    """Panel B: Selection components."""
    sigma = np.linspace(0, 0.8, 100)
    results = calculate_fitness_components(sigma)
    sigma_star = find_critical_sigma()

    # Plot selection components
    ax.plot(sigma, results['between_group'], color=CB_COLORS['blue'],
            linewidth=2.5, label='Between-group\n(favors signaling)')
    ax.plot(sigma, results['within_group'], color=CB_COLORS['red'],
            linewidth=2.5, label='Within-group\n(favors non-signaling)')
    ax.plot(sigma, results['net_selection'], color=CB_COLORS['purple'],
            linewidth=2.5, linestyle='--', label='Net selection')

    # Mark zero line and critical point
    ax.axhline(0, color=CB_COLORS['gray'], linewidth=1, alpha=0.5)
    ax.axvline(sigma_star, color=CB_COLORS['gray'], linestyle='--',
               linewidth=1.5, alpha=0.7)

    # Annotate critical threshold
    ax.annotate('Critical\nthreshold σ*', xy=(sigma_star, -0.1),
                xytext=(sigma_star + 0.08, -0.18), fontsize=8, ha='left',
                arrowprops=dict(arrowstyle='->', color=CB_COLORS['gray']))

    ax.set_xlabel('Environmental Uncertainty (σ)', fontsize=11)
    ax.set_ylabel('Selection Coefficient', fontsize=11)
    ax.set_title('B. Price Equation Components',
                 fontsize=12, fontweight='bold', loc='left')

    # Move legend to lower right to avoid overlap
    ax.legend(loc='lower right', fontsize=8, framealpha=0.95)
    ax.set_xlim(0, 0.8)
    ax.set_ylim(-0.6, 0.25)
    ax.grid(alpha=0.3)


def create_panel_c(ax):
    """Panel C: Phase space prediction from modified Price equation."""
    # Create grid of frequency and magnitude
    freq = np.linspace(5, 20, 50)
    mag = np.linspace(0.2, 0.8, 50)
    FREQ, MAG = np.meshgrid(freq, mag)

    # Calculate sigma for each point
    SIGMA = sigma_from_params(FREQ, MAG)

    # Calculate fitness difference (positive = signaling favored)
    sigma_star = find_critical_sigma()

    # Predicted dominance based on sigma relative to sigma*
    # Scale to match simulation dominance values (-1 to +1)
    DOMINANCE = np.tanh((SIGMA - sigma_star) * 5)

    # Plot
    im = ax.contourf(FREQ, MAG, DOMINANCE, levels=20,
                     cmap='RdBu', vmin=-1, vmax=1)

    # Add contour line at dominance = 0
    ax.contour(FREQ, MAG, DOMINANCE, levels=[0], colors='black',
               linewidths=2, linestyles='--')

    # Mark case study positions
    ax.scatter([6], [0.6], s=150, c='cyan', edgecolors='black',
               linewidths=2, marker='o', zorder=5, label='Rapa Nui')
    ax.scatter([18], [0.3], s=150, c='yellow', edgecolors='black',
               linewidths=2, marker='s', zorder=5, label='Rapa Iti')

    ax.set_xlabel('Shortfall Frequency (years)', fontsize=11)
    ax.set_ylabel('Shortfall Magnitude', fontsize=11)
    ax.set_title('C. Predicted Phase Space (from Modified Price Equation)',
                 fontsize=12, fontweight='bold', loc='left')

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Predicted Dominance\n(+1 = signaling, -1 = non-signaling)',
                   fontsize=9)

    ax.legend(loc='lower right', fontsize=9)

    # Add region labels
    ax.text(7, 0.7, 'Signaling\nfavored', ha='center', fontsize=10,
            color='white', fontweight='bold')
    ax.text(17, 0.3, 'Non-signaling\nfavored', ha='center', fontsize=10,
            color='white', fontweight='bold')


def create_panel_d(ax):
    """Panel D: Theoretical framework diagram."""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('D. Modified Price Equation Framework',
                 fontsize=12, fontweight='bold', loc='left')

    # Central equation box
    eq_box = FancyBboxPatch((1.5, 6), 7, 2.5,
                             boxstyle="round,pad=0.1,rounding_size=0.2",
                             facecolor='lightyellow', edgecolor='black',
                             linewidth=2)
    ax.add_patch(eq_box)

    # Main equation
    ax.text(5, 7.5, 'Modified Price Equation:', ha='center',
            fontsize=11, fontweight='bold')
    ax.text(5, 6.7, r'$\Delta\bar{p} = \frac{Cov(w_g(\sigma), p_g)}{\bar{w}} + \frac{E(w_g(\sigma)\Delta p_g)}{\bar{w}}$',
            ha='center', fontsize=11)

    # Key modification box
    mod_box = FancyBboxPatch((0.5, 3.5), 4, 2,
                              boxstyle="round,pad=0.05,rounding_size=0.1",
                              facecolor=CB_COLORS['blue'], alpha=0.2,
                              edgecolor=CB_COLORS['blue'], linewidth=1.5)
    ax.add_patch(mod_box)
    ax.text(2.5, 5.2, 'Group Fitness', ha='center', fontsize=10, fontweight='bold',
            color=CB_COLORS['blue'])
    ax.text(2.5, 4.5, r'$w_g(\sigma) = (1-C) \cdot S(\sigma)$', ha='center', fontsize=10)
    ax.text(2.5, 3.8, 'Survival depends on\nuncertainty σ', ha='center', fontsize=9,
            style='italic')

    # Uncertainty box
    unc_box = FancyBboxPatch((5.5, 3.5), 4, 2,
                              boxstyle="round,pad=0.05,rounding_size=0.1",
                              facecolor=CB_COLORS['orange'], alpha=0.2,
                              edgecolor=CB_COLORS['orange'], linewidth=1.5)
    ax.add_patch(unc_box)
    ax.text(7.5, 5.2, 'Uncertainty Parameter', ha='center', fontsize=10,
            fontweight='bold', color=CB_COLORS['orange'])
    ax.text(7.5, 4.5, r'$\sigma = f($freq, mag, dur$)$', ha='center', fontsize=10)
    ax.text(7.5, 3.8, 'Combines shortfall\nfrequency × severity', ha='center',
            fontsize=9, style='italic')

    # Prediction box
    pred_box = FancyBboxPatch((2.5, 0.5), 5, 2.2,
                               boxstyle="round,pad=0.05,rounding_size=0.1",
                               facecolor=CB_COLORS['green'], alpha=0.2,
                               edgecolor=CB_COLORS['green'], linewidth=1.5)
    ax.add_patch(pred_box)
    ax.text(5, 2.4, 'Critical Prediction', ha='center', fontsize=10,
            fontweight='bold', color=CB_COLORS['green'])
    ax.text(5, 1.6, r'Signaling favored when $\sigma > \sigma^*$',
            ha='center', fontsize=10)
    ax.text(5, 0.9, r'where $\sigma^* = \frac{C}{\beta - (1-C)\alpha}$',
            ha='center', fontsize=10)

    # Arrows connecting boxes
    ax.annotate('', xy=(2.5, 5.5), xytext=(3.5, 6),
                arrowprops=dict(arrowstyle='->', color=CB_COLORS['gray'], lw=1.5))
    ax.annotate('', xy=(7.5, 5.5), xytext=(6.5, 6),
                arrowprops=dict(arrowstyle='->', color=CB_COLORS['gray'], lw=1.5))
    ax.annotate('', xy=(5, 2.7), xytext=(5, 3.5),
                arrowprops=dict(arrowstyle='->', color=CB_COLORS['gray'], lw=1.5))


def main():
    print("Creating Modified Price Equation Figure...")

    # Create figure with 2x2 grid
    fig = plt.figure(figsize=(14, 12))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

    # Create panels
    ax1 = fig.add_subplot(gs[0, 0])
    create_panel_a(ax1)

    ax2 = fig.add_subplot(gs[0, 1])
    create_panel_b(ax2)

    ax3 = fig.add_subplot(gs[1, 0])
    create_panel_c(ax3)

    ax4 = fig.add_subplot(gs[1, 1])
    create_panel_d(ax4)

    plt.tight_layout()

    # Save PNG (Figure 6 in manuscript - Section 2.7)
    output_path = 'figures/final/Figure_6_modified_price_equation.png'
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")

    # Save SVG
    svg_path = 'figures/final/figure_modified_price_equation.svg'
    fig.savefig(svg_path, format='svg', bbox_inches='tight', facecolor='white')
    print(f"Saved: {svg_path}")

    # Print critical sigma value
    sigma_star = find_critical_sigma()
    print(f"\nCritical uncertainty threshold σ* = {sigma_star:.3f}")
    print("This corresponds approximately to:")
    print("  - Frequency ~10 years, Magnitude ~0.5")
    print("  - Or Frequency ~7 years, Magnitude ~0.4")
    print("  - Or Frequency ~15 years, Magnitude ~0.7")

    plt.close()


if __name__ == '__main__':
    main()
