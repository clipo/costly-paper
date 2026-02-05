"""
Create Price Equation Figure for Multilevel Selection

Illustrates the Price equation: Δp = Cov(wi, pi)/w̄ + E(wi Δpi)/w̄

Panel A: Visual decomposition of the Price equation with group representation
Panel B: Between-group selection - groups with more monument builders survive better
Panel C: Within-group selection - individual competition within groups
Panel D: Net selection and the conditions favoring costly signaling

Output: figures/final/figure_price_equation.png
"""

import os

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Wedge

# Colorblind-safe colors (matching project style)
CB_COLORS = {
    'blue': '#0173B2',      # Monument builders
    'red': '#D55E00',       # High reproduction
    'green': '#029E73',     # Positive/survival
    'orange': '#DE8F05',    # Costs/warnings
    'purple': '#CC78BC',    # Neutral/mixed
    'gray': '#949494',      # Neutral elements
    'black': '#000000',
}


def draw_group_pie(ax, x, y, radius, mb_fraction, label=None, fitness_label=None, highlight=False):
    """Draw a group as a pie chart showing MB vs HR proportions."""
    # Draw outer circle
    edge_width = 3 if highlight else 1.5
    circle = Circle((x, y), radius, fill=False, edgecolor=CB_COLORS['black'],
                    linewidth=edge_width)
    ax.add_patch(circle)

    # Draw as pie chart
    if mb_fraction > 0:
        mb_wedge = Wedge((x, y), radius * 0.95, 90, 90 - mb_fraction * 360,
                        facecolor=CB_COLORS['blue'], edgecolor='none', alpha=0.85)
        ax.add_patch(mb_wedge)

    if mb_fraction < 1:
        hr_wedge = Wedge((x, y), radius * 0.95, 90 - mb_fraction * 360, 90 - 360,
                        facecolor=CB_COLORS['red'], edgecolor='none', alpha=0.85)
        ax.add_patch(hr_wedge)

    if label:
        ax.text(x, y - radius - 0.25, label, ha='center', va='top', fontsize=8,
                fontweight='bold')

    if fitness_label:
        color = CB_COLORS['green'] if 'High' in fitness_label else (
            CB_COLORS['orange'] if 'Med' in fitness_label else CB_COLORS['red'])
        ax.text(x, y + radius + 0.15, fitness_label, ha='center', va='bottom',
                fontsize=7, color=color, style='italic')


def create_equation_panel(ax):
    """Panel A: Visual representation of the Price equation"""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('A. The Price Equation for Multilevel Selection', fontsize=11,
                 fontweight='bold', loc='left')

    # Main equation
    eq_text = r'$\Delta \bar{p} = \frac{Cov(w_i, p_i)}{\bar{w}} + \frac{E(w_i \Delta p_i)}{\bar{w}}$'
    ax.text(5, 9.0, eq_text, ha='center', va='center', fontsize=13)

    # Labels for equation terms with brackets
    ax.annotate('', xy=(2.7, 8.55), xytext=(4.3, 8.55),
                arrowprops=dict(arrowstyle='-', color=CB_COLORS['blue'], lw=2))
    ax.text(3.5, 8.2, 'Between-group\nselection', ha='center', va='top', fontsize=8,
            color=CB_COLORS['blue'], fontweight='bold')

    ax.annotate('', xy=(5.8, 8.55), xytext=(7.4, 8.55),
                arrowprops=dict(arrowstyle='-', color=CB_COLORS['red'], lw=2))
    ax.text(6.6, 8.2, 'Within-group\nselection', ha='center', va='top', fontsize=8,
            color=CB_COLORS['red'], fontweight='bold')

    # Draw three example groups
    draw_group_pie(ax, 2, 5.2, 0.7, 0.8, 'Group 1\n(80% MB)', 'High survival')
    draw_group_pie(ax, 5, 5.2, 0.7, 0.5, 'Group 2\n(50% MB)', 'Med. survival')
    draw_group_pie(ax, 8, 5.2, 0.7, 0.2, 'Group 3\n(20% MB)', 'Low survival')

    # Legend
    mb_circle = Circle((2.5, 2.5), 0.22, facecolor=CB_COLORS['blue'],
                       edgecolor='black', alpha=0.85)
    ax.add_patch(mb_circle)
    ax.text(2.9, 2.5, 'Monument Builders (MB)', ha='left', va='center', fontsize=8)

    hr_circle = Circle((6.2, 2.5), 0.22, facecolor=CB_COLORS['red'],
                       edgecolor='black', alpha=0.85)
    ax.add_patch(hr_circle)
    ax.text(6.6, 2.5, 'High Reproduction (HR)', ha='left', va='center', fontsize=8)

    # Explanation
    ax.text(5, 1.3, 'Each circle = a territorial group; colors = strategy proportions',
            ha='center', va='center', fontsize=8, style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                     alpha=0.8, edgecolor='gray'))


def create_between_group_panel(ax):
    """Panel B: Between-group selection illustration"""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('B. Between-Group Selection: Cov(wᵢ, pᵢ)', fontsize=11,
                 fontweight='bold', loc='left')

    # BEFORE selection - left side
    ax.text(2.2, 9.2, 'Before Shortfall', ha='center', va='center',
            fontsize=9, fontweight='bold')

    draw_group_pie(ax, 1.2, 7.5, 0.55, 0.8)
    draw_group_pie(ax, 2.2, 7.5, 0.55, 0.5)
    draw_group_pie(ax, 3.2, 7.5, 0.55, 0.2)

    # Arrow down
    ax.annotate('', xy=(2.2, 5.8), xytext=(2.2, 6.6),
                arrowprops=dict(arrowstyle='->', color=CB_COLORS['gray'], lw=2))
    ax.text(2.2, 6.2, 'Selection\nevent', ha='center', va='center', fontsize=7,
            style='italic', color=CB_COLORS['gray'])

    # AFTER selection
    ax.text(2.2, 5.3, 'After Shortfall', ha='center', va='center',
            fontsize=9, fontweight='bold')

    # High MB survives and grows
    draw_group_pie(ax, 1.2, 3.8, 0.65, 0.8, highlight=True)
    ax.text(1.2, 2.9, 'Survives', ha='center', va='top', fontsize=7,
            color=CB_COLORS['green'], fontweight='bold')

    # Medium MB reduced
    draw_group_pie(ax, 2.4, 3.8, 0.4, 0.5)
    ax.text(2.4, 3.2, 'Reduced', ha='center', va='top', fontsize=7,
            color=CB_COLORS['orange'])

    # Low MB extinct
    extinct_circle = Circle((3.4, 3.8), 0.35, fill=False, edgecolor=CB_COLORS['gray'],
                            linewidth=1, linestyle='--', alpha=0.6)
    ax.add_patch(extinct_circle)
    ax.text(3.4, 3.8, 'X', ha='center', va='center', fontsize=12,
            color=CB_COLORS['red'], fontweight='bold')
    ax.text(3.4, 3.2, 'Extinct', ha='center', va='top', fontsize=7,
            color=CB_COLORS['red'])

    # Right side: explanation box
    box = FancyBboxPatch((4.3, 1.8), 5.4, 7.0,
                          boxstyle="round,pad=0.15,rounding_size=0.2",
                          facecolor='white', edgecolor=CB_COLORS['blue'],
                          linewidth=2, alpha=0.95)
    ax.add_patch(box)

    ax.text(7.0, 8.3, 'Why high-MB groups survive:', ha='center', va='center',
            fontsize=9, fontweight='bold', color=CB_COLORS['blue'])

    benefits = [
        ('Lower conflict probability', 'Mutual signaling deters attacks'),
        ('Reciprocity networks', 'Monuments signal reliable partners'),
        ('Resource buffering', 'Cooperation during shortfalls'),
    ]

    y_pos = 7.4
    for title, desc in benefits:
        ax.text(4.7, y_pos, '•', ha='left', va='center', fontsize=10,
                color=CB_COLORS['blue'], fontweight='bold')
        ax.text(5.0, y_pos, title, ha='left', va='center', fontsize=8,
                color=CB_COLORS['blue'], fontweight='bold')
        ax.text(5.0, y_pos - 0.45, desc, ha='left', va='center', fontsize=7,
                color=CB_COLORS['gray'], style='italic')
        y_pos -= 1.3

    # Result
    result_box = FancyBboxPatch((4.6, 2.0), 4.8, 1.8,
                                 boxstyle="round,pad=0.1",
                                 facecolor='#e8f5e9', edgecolor=CB_COLORS['green'],
                                 linewidth=1.5)
    ax.add_patch(result_box)

    ax.text(7.0, 3.3, 'Result: Positive Cov(wᵢ, pᵢ)', ha='center', va='center',
            fontsize=9, fontweight='bold', color=CB_COLORS['green'])
    ax.text(7.0, 2.6, 'Groups with more MB have higher fitness', ha='center', va='center',
            fontsize=8, color=CB_COLORS['black'])


def create_within_group_panel(ax):
    """Panel C: Within-group selection illustration"""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('C. Within-Group Selection: E(wᵢΔpᵢ)', fontsize=11,
                 fontweight='bold', loc='left')

    # Draw enlarged single group
    ax.text(3.2, 9.2, 'Within a Single Group', ha='center', va='center',
            fontsize=10, fontweight='bold')

    # Group boundary (dashed circle)
    group_circle = Circle((3.2, 5.5), 2.5, fill=False,
                          edgecolor=CB_COLORS['gray'], linewidth=2, linestyle='--')
    ax.add_patch(group_circle)

    # Individual MB agents (blue circles with offspring)
    mb_positions = [(2, 6.8), (2.8, 4.2), (4.5, 6.2)]
    for i, (x, y) in enumerate(mb_positions):
        c = Circle((x, y), 0.35, facecolor=CB_COLORS['blue'],
                   edgecolor='black', linewidth=1.5, alpha=0.9)
        ax.add_patch(c)
        # Show fewer offspring for MB
        if i == 0:
            for ox, oy in [(x-0.3, y-0.7), (x+0.3, y-0.7)]:
                oc = Circle((ox, oy), 0.15, facecolor=CB_COLORS['blue'],
                           edgecolor='black', linewidth=0.5, alpha=0.7)
                ax.add_patch(oc)

    # Individual HR agents (red circles with more offspring)
    hr_positions = [(3.8, 4.5), (4.2, 5.2)]
    for i, (x, y) in enumerate(hr_positions):
        c = Circle((x, y), 0.35, facecolor=CB_COLORS['red'],
                   edgecolor='black', linewidth=1.5, alpha=0.9)
        ax.add_patch(c)
        # Show more offspring for HR
        if i == 0:
            for ox, oy in [(x-0.4, y-0.65), (x, y-0.75), (x+0.4, y-0.65)]:
                oc = Circle((ox, oy), 0.15, facecolor=CB_COLORS['red'],
                           edgecolor='black', linewidth=0.5, alpha=0.7)
                ax.add_patch(oc)

    # Labels for offspring counts
    ax.text(1.7, 5.5, '2 offspring', ha='center', va='center', fontsize=8,
            color=CB_COLORS['blue'], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9))
    ax.text(4.0, 3.4, '3+ offspring', ha='center', va='center', fontsize=8,
            color=CB_COLORS['red'], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9))

    # Right side explanation
    box = FancyBboxPatch((6.0, 4.5), 3.7, 4.5,
                          boxstyle="round,pad=0.15,rounding_size=0.2",
                          facecolor='white', edgecolor=CB_COLORS['red'],
                          linewidth=2, alpha=0.95)
    ax.add_patch(box)

    ax.text(7.85, 8.5, 'Individual dynamics:', ha='center', va='center',
            fontsize=9, fontweight='bold', color=CB_COLORS['red'])

    lines = [
        ('MB cost:', '35% resources → monuments'),
        ('HR bonus:', '+40% reproduction rate'),
        ('', ''),
        ('Result:', 'HR out-reproduces MB'),
        ('', 'within each group'),
    ]

    y_pos = 7.8
    for label, text in lines:
        if label:
            ax.text(6.3, y_pos, label, ha='left', va='center', fontsize=8,
                    color=CB_COLORS['red'] if 'Result' in label else CB_COLORS['black'],
                    fontweight='bold')
            ax.text(6.3, y_pos - 0.4, text, ha='left', va='center', fontsize=7,
                    color=CB_COLORS['gray'] if 'Result' not in label else CB_COLORS['black'])
        y_pos -= 0.9

    # Result box
    result_box = FancyBboxPatch((6.2, 4.7), 3.3, 1.2,
                                 boxstyle="round,pad=0.1",
                                 facecolor='#ffebee', edgecolor=CB_COLORS['red'],
                                 linewidth=1.5)
    ax.add_patch(result_box)

    ax.text(7.85, 5.3, 'Negative E(wᵢΔpᵢ)', ha='center', va='center',
            fontsize=9, fontweight='bold', color=CB_COLORS['red'])

    # Bottom: tension statement
    tension_box = FancyBboxPatch((0.3, 0.5), 9.4, 1.6,
                                  boxstyle="round,pad=0.15,rounding_size=0.2",
                                  facecolor='lightyellow', edgecolor=CB_COLORS['orange'],
                                  linewidth=2, alpha=0.95)
    ax.add_patch(tension_box)

    ax.text(5, 1.65, 'The Multilevel Selection Tension:', ha='center', va='center',
            fontsize=9, fontweight='bold', color=CB_COLORS['orange'])
    ax.text(5, 1.0, 'What is costly for individuals may be beneficial for the group',
            ha='center', va='center', fontsize=9, style='italic')


def create_net_selection_panel(ax):
    """Panel D: Necessary conditions for costly signaling to persist"""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('D. Necessary Condition for Group-Level Traits', fontsize=11,
                 fontweight='bold', loc='left')

    # Condition for evolution
    ax.text(5, 9.3, r'For costly signaling to persist:', ha='center', va='center',
            fontsize=10, fontweight='bold')
    ax.text(5, 8.6, r'Between-group benefit  >  Within-group cost', ha='center', va='center',
            fontsize=10)

    # Color the terms
    ax.text(3.05, 8.6, 'Between-group benefit', ha='center', va='center',
            fontsize=10, color=CB_COLORS['blue'], fontweight='bold', alpha=0)  # invisible placeholder
    ax.text(6.85, 8.6, 'Within-group cost', ha='center', va='center',
            fontsize=10, color=CB_COLORS['red'], fontweight='bold', alpha=0)  # invisible placeholder

    # Visual balance scale
    # Fulcrum (triangle)
    fulcrum = Polygon([(5, 5.8), (4.7, 5.2), (5.3, 5.2)],
                      facecolor=CB_COLORS['gray'], edgecolor='black', linewidth=1.5)
    ax.add_patch(fulcrum)

    # Balance beam (tilted - between-group heavier)
    ax.plot([1.8, 8.2], [6.8, 6.0], color='black', lw=4, solid_capstyle='round')

    # Left pan - Between-group (heavier, lower position but beam tilts that way)
    between_box = FancyBboxPatch((1.0, 7.0), 2.0, 1.2,
                                  boxstyle="round,pad=0.05,rounding_size=0.1",
                                  facecolor=CB_COLORS['blue'], edgecolor='black',
                                  linewidth=2)
    ax.add_patch(between_box)
    ax.text(2.0, 7.6, 'Between\n(+)', ha='center', va='center',
            fontsize=9, fontweight='bold', color='white')

    # Right pan - Within-group (lighter)
    within_box = FancyBboxPatch((7.0, 6.2), 1.7, 1.0,
                                 boxstyle="round,pad=0.05,rounding_size=0.1",
                                 facecolor=CB_COLORS['red'], edgecolor='black',
                                 linewidth=2)
    ax.add_patch(within_box)
    ax.text(7.85, 6.7, 'Within\n(-)', ha='center', va='center',
            fontsize=9, fontweight='bold', color='white')

    # Left column: Model explores these conditions
    ax.text(0.5, 4.6, 'Model explores when\nthis condition is met:', ha='left', va='center',
            fontsize=9, fontweight='bold', color=CB_COLORS['green'])

    conditions = [
        'Shortfall frequency?',
        'Shortfall severity?',
        'Group competition?',
        'Territorial structure?',
    ]

    y_pos = 3.6
    for cond in conditions:
        ax.text(0.7, y_pos, '•  ' + cond, ha='left', va='center', fontsize=8,
                color=CB_COLORS['black'])
        y_pos -= 0.6

    # Right column: Key question
    rapa_box = FancyBboxPatch((4.8, 0.5), 5.0, 4.3,
                               boxstyle="round,pad=0.15,rounding_size=0.2",
                               facecolor='white', edgecolor=CB_COLORS['orange'],
                               linewidth=2)
    ax.add_patch(rapa_box)

    ax.text(7.3, 4.4, 'Key Question:', ha='center', va='center',
            fontsize=9, fontweight='bold', color=CB_COLORS['orange'])

    question_lines = [
        'Under what environmental',
        'conditions is between-group',
        'selection strong enough to',
        'overcome within-group costs?',
    ]

    y_pos = 3.7
    for line in question_lines:
        ax.text(7.3, y_pos, line, ha='center', va='center', fontsize=8)
        y_pos -= 0.5

    # Conclusion arrow
    ax.text(7.3, 1.5, '→ This paper uses an ABM', ha='center', va='center',
            fontsize=9, fontweight='bold', color=CB_COLORS['green'])
    ax.text(7.3, 0.95, '   to identify this parameter space', ha='center', va='center',
            fontsize=9, fontweight='bold', color=CB_COLORS['green'])


def main():
    print("Creating Price Equation Figure...")

    # Create figure with 2x2 grid
    fig = plt.figure(figsize=(12, 12))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.25,
                  left=0.05, right=0.95, top=0.95, bottom=0.05)

    # Panel A: Equation overview
    ax1 = fig.add_subplot(gs[0, 0])
    create_equation_panel(ax1)

    # Panel B: Between-group selection
    ax2 = fig.add_subplot(gs[0, 1])
    create_between_group_panel(ax2)

    # Panel C: Within-group selection
    ax3 = fig.add_subplot(gs[1, 0])
    create_within_group_panel(ax3)

    # Panel D: Net selection
    ax4 = fig.add_subplot(gs[1, 1])
    create_net_selection_panel(ax4)

    # Save
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'figures', 'final')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, 'figure_price_equation.png')
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {output_path}")

    # Also save PDF version
    pdf_path = os.path.join(output_dir, 'figure_price_equation.pdf')
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight', facecolor='white')
    print(f"Saved: {pdf_path}")

    plt.close()
    print("Done!")


if __name__ == '__main__':
    main()
