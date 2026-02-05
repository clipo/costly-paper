"""
Costly Signaling and Demography in Polynesian Societies

Agent-based model exploring how environmental uncertainty shapes costly
signaling strategies and demographic outcomes.
"""

__version__ = "1.0.0"

# Core simulation classes
# Case study functions
from .case_studies import (
    compare_rapa_scenarios,
    explore_productivity_gradient,
    get_rapa_iti_params,
    get_rapa_nui_params,
    plot_productivity_gradient,
    run_rapa_iti_simulation,
    run_rapa_nui_simulation,
    test_strategy_stability,
)

# Parameter exploration functions
from .parameter_exploration import (
    analyze_population_dynamics,
    compare_strategy_proportions,
    explore_resource_uncertainty,
    identify_critical_transitions,
    plot_parameter_space,
    plot_proportion_comparison,
    run_single_simulation,
)
from .simulation import Group, SpatialSimulation, Strategy

# Visualization classes and functions
from .visualization import (
    SimulationVisualizer,
    compare_scenarios,
    create_animation_frames,
    plot_phase_diagram,
)

__all__ = [
    # Version
    '__version__',
    # Simulation
    'Strategy',
    'Group',
    'SpatialSimulation',
    # Case studies
    'get_rapa_nui_params',
    'get_rapa_iti_params',
    'run_rapa_nui_simulation',
    'run_rapa_iti_simulation',
    'compare_rapa_scenarios',
    'test_strategy_stability',
    'explore_productivity_gradient',
    'plot_productivity_gradient',
    # Parameter exploration
    'run_single_simulation',
    'explore_resource_uncertainty',
    'plot_parameter_space',
    'identify_critical_transitions',
    'compare_strategy_proportions',
    'plot_proportion_comparison',
    'analyze_population_dynamics',
    # Visualization
    'SimulationVisualizer',
    'compare_scenarios',
    'plot_phase_diagram',
    'create_animation_frames',
]
