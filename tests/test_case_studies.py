"""
Unit tests for case study scenarios.
"""

import pytest


class TestCaseStudyParameters:
    """Test that case study parameters are correctly defined."""

    def test_rapa_nui_params(self):
        """Test Rapa Nui parameter values."""
        from costly.case_studies import get_rapa_nui_params

        params = get_rapa_nui_params()
        # Check expected parameter ranges
        assert params['shortfall_frequency'] <= 10  # Frequent shortfalls
        assert params['shortfall_magnitude'] >= 0.5  # Severe magnitude

    def test_rapa_iti_params(self):
        """Test Rapa Iti parameter values."""
        from costly.case_studies import get_rapa_iti_params

        params = get_rapa_iti_params()
        # Check expected parameter ranges
        assert params['shortfall_frequency'] >= 15  # Rare shortfalls
        assert params['shortfall_magnitude'] <= 0.4  # Mild magnitude

    def test_params_differ(self):
        """Test that Rapa Nui and Rapa Iti have different parameters."""
        from costly.case_studies import get_rapa_nui_params, get_rapa_iti_params

        rn_params = get_rapa_nui_params()
        ri_params = get_rapa_iti_params()
        assert rn_params['shortfall_frequency'] != ri_params['shortfall_frequency']
        assert rn_params['shortfall_magnitude'] != ri_params['shortfall_magnitude']


class TestCaseStudySimulations:
    """Test running case study simulations."""

    def test_run_rapa_nui(self):
        """Test that Rapa Nui simulation runs."""
        from costly.case_studies import run_rapa_nui_simulation

        sim = run_rapa_nui_simulation(years=20)
        assert sim is not None

    def test_run_rapa_iti(self):
        """Test that Rapa Iti simulation runs."""
        from costly.case_studies import run_rapa_iti_simulation

        sim = run_rapa_iti_simulation(years=20)
        assert sim is not None

    def test_comparison_runs(self):
        """Test that comparison function runs."""
        from costly.case_studies import compare_rapa_scenarios
        import matplotlib.pyplot as plt

        fig, rn_sim, ri_sim = compare_rapa_scenarios(years=20)
        assert fig is not None
        assert rn_sim is not None
        assert ri_sim is not None
        plt.close(fig)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
