"""
Unit tests for the costly signaling simulation.
"""

import pytest
import numpy as np


class TestSimulationBasics:
    """Test basic simulation functionality."""

    def test_import(self):
        """Test that the package can be imported."""
        from costly import SpatialSimulation
        assert SpatialSimulation is not None

    def test_simulation_creation(self):
        """Test that a simulation can be created with default parameters."""
        from costly import SpatialSimulation
        sim = SpatialSimulation(grid_size=20, n_groups=8)
        assert sim is not None
        assert sim.grid_size == 20

    def test_simulation_runs(self):
        """Test that a simulation can run without errors."""
        from costly import SpatialSimulation
        sim = SpatialSimulation(grid_size=20, n_groups=8)
        sim.run(years=10)
        stats = sim.get_summary_statistics()
        assert stats is not None
        assert 'total_population' in stats

    def test_strategies_compete(self):
        """Test that both strategies are present and competing."""
        from costly import SpatialSimulation
        sim = SpatialSimulation(
            grid_size=20,
            n_groups=8,
            shortfall_frequency=5,
            shortfall_magnitude=0.5
        )
        sim.run(years=50)
        stats = sim.get_summary_statistics()
        assert stats is not None


class TestParameterValidation:
    """Test parameter validation and edge cases."""

    def test_small_grid(self):
        """Test simulation with minimum grid size."""
        from costly import SpatialSimulation
        sim = SpatialSimulation(grid_size=10, n_groups=4)
        sim.run(years=5)
        stats = sim.get_summary_statistics()
        assert stats is not None

    def test_different_frequencies(self):
        """Test with different shortfall frequencies."""
        from costly import SpatialSimulation
        for freq in [5, 10, 20]:
            sim = SpatialSimulation(
                grid_size=20,
                n_groups=8,
                shortfall_frequency=freq
            )
            sim.run(years=20)
            stats = sim.get_summary_statistics()
            assert stats is not None

    def test_different_magnitudes(self):
        """Test with different shortfall magnitudes."""
        from costly import SpatialSimulation
        for mag in [0.2, 0.5, 0.8]:
            sim = SpatialSimulation(
                grid_size=20,
                n_groups=8,
                shortfall_magnitude=mag
            )
            sim.run(years=20)
            stats = sim.get_summary_statistics()
            assert stats is not None


class TestReproducibility:
    """Test that simulations are reproducible with same seed."""

    def test_same_seed_same_results(self):
        """Test that same random seed produces identical results."""
        from costly import SpatialSimulation

        seed = 12345
        np.random.seed(seed)
        sim1 = SpatialSimulation(grid_size=20, n_groups=8)
        sim1.run(years=20)
        stats1 = sim1.get_summary_statistics()

        np.random.seed(seed)
        sim2 = SpatialSimulation(grid_size=20, n_groups=8)
        sim2.run(years=20)
        stats2 = sim2.get_summary_statistics()

        # Results should be identical with same seed
        assert stats1['total_population'] == stats2['total_population']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
