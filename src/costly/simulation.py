"""
Spatial simulation of group-level costly signaling vs reproduction strategies
Explores conditions under which monument building leads to lower but more competitive populations
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple

import numpy as np


class Strategy(Enum):
    """Group strategy types"""
    COSTLY_SIGNALING = "Monument Building"
    HIGH_REPRODUCTION = "High Reproduction"


@dataclass
class Group:
    """Represents a social group with territory and strategy"""
    id: int
    strategy: Strategy
    territory: List[Tuple[int, int]]  # List of (x, y) coordinates
    population: float
    monument_investment: float = 0.0
    conflicts_won: int = 0
    conflicts_lost: int = 0

    def __post_init__(self):
        self.history = {
            'population': [self.population],
            'monument': [self.monument_investment],
            'conflicts': [0]
        }

    @property
    def territory_size(self) -> int:
        return len(self.territory)

    @property
    def population_density(self) -> float:
        return self.population / max(1, self.territory_size)


class SpatialSimulation:
    """
    Spatial simulation of costly signaling vs reproduction strategies
    """

    def __init__(
        self,
        grid_size: Tuple[int, int] = (50, 50),
        n_groups: int = 20,
        base_productivity: float = 1.0,
        shortfall_frequency: int = 10,
        shortfall_magnitude: float = 0.5,
        monument_cost: float = 0.3,
        reproduction_bonus: float = 0.5,
        conflict_mortality: float = 0.2,
        signaling_conflict_reduction: float = 0.7,
        carrying_capacity_per_cell: float = 10.0,
        shortfall_conflict_multiplier: float = 2.5,
        cooperation_sharing_rate: float = 0.15,
        monument_buffer_factor: float = 0.1,
        seed: Optional[int] = None
    ):
        """
        Initialize simulation

        Parameters:
        -----------
        grid_size: Territory dimensions
        n_groups: Number of groups
        base_productivity: Base resource productivity
        shortfall_frequency: Years between resource shortfalls
        shortfall_magnitude: Proportion of productivity lost during shortfall (0-1)
        monument_cost: Proportion of resources devoted to monuments (signaling groups)
        reproduction_bonus: Extra reproduction rate for high-reproduction strategy
        conflict_mortality: Deaths per conflict as proportion of population
        signaling_conflict_reduction: How much signaling reduces conflict probability
        carrying_capacity_per_cell: Maximum sustainable population per territory cell
        shortfall_conflict_multiplier: How much conflict probability increases during shortfalls
        cooperation_sharing_rate: Proportion of resources shared between signaling groups during shortfalls
        monument_buffer_factor: How much monument investment buffers against shortfall impacts
        seed: Random seed for reproducibility
        """
        self.grid_size = grid_size
        self.n_groups = n_groups
        self.base_productivity = base_productivity
        self.shortfall_frequency = shortfall_frequency
        self.shortfall_magnitude = shortfall_magnitude
        self.monument_cost = monument_cost
        self.reproduction_bonus = reproduction_bonus
        self.conflict_mortality = conflict_mortality
        self.signaling_conflict_reduction = signaling_conflict_reduction
        self.carrying_capacity_per_cell = carrying_capacity_per_cell
        self.shortfall_conflict_multiplier = shortfall_conflict_multiplier
        self.cooperation_sharing_rate = cooperation_sharing_rate
        self.monument_buffer_factor = monument_buffer_factor

        if seed is not None:
            np.random.seed(seed)

        # Initialize grid and groups
        self.territory_map = np.zeros(grid_size, dtype=int) - 1  # -1 = unoccupied
        self.productivity_map = np.ones(grid_size) * base_productivity
        self.groups: dict = {}  # Changed to dict for stable indexing
        self.year = 0
        self.is_shortfall = False  # Track current shortfall state for other methods
        self.history = {
            'total_population': [],
            'population_by_strategy': {Strategy.COSTLY_SIGNALING: [], Strategy.HIGH_REPRODUCTION: []},
            'conflicts_per_year': [],
            'avg_monument_investment': []
        }

    def initialize_groups(self, strategy_proportions: dict = None):
        """
        Initialize groups on territory

        Parameters:
        -----------
        strategy_proportions: Dict mapping Strategy to proportion (e.g., {Strategy.COSTLY_SIGNALING: 0.5})
                            If None, splits evenly
        """
        if strategy_proportions is None:
            strategy_proportions = {
                Strategy.COSTLY_SIGNALING: 0.5,
                Strategy.HIGH_REPRODUCTION: 0.5
            }

        # Create group centers using Poisson disk sampling for spatial distribution
        centers = self._generate_group_centers(self.n_groups)

        # Assign strategies
        strategies = []
        for strategy, prop in strategy_proportions.items():
            n = int(self.n_groups * prop)
            strategies.extend([strategy] * n)

        # Fill remaining if rounding leaves some out
        while len(strategies) < self.n_groups:
            strategies.append(np.random.choice(list(strategy_proportions.keys())))

        np.random.shuffle(strategies)

        # Initialize groups
        for i, (center, strategy) in enumerate(zip(centers, strategies)):
            initial_pop = np.random.uniform(50, 100)
            group = Group(
                id=i,
                strategy=strategy,
                territory=[],
                population=initial_pop
            )
            self.groups[i] = group  # Changed to dict

        # Assign territories using Voronoi-like tessellation
        self._assign_territories(centers)

        # Set initial monument investment for signaling groups
        for group in self.groups.values():  # Changed to .values()
            if group.strategy == Strategy.COSTLY_SIGNALING:
                group.monument_investment = self.monument_cost * group.population

    def _generate_group_centers(self, n: int) -> List[Tuple[int, int]]:
        """Generate spatially distributed group centers"""
        centers = []
        min_distance = min(self.grid_size) / (np.sqrt(n) * 1.5)

        attempts = 0
        max_attempts = n * 100

        while len(centers) < n and attempts < max_attempts:
            x = np.random.randint(0, self.grid_size[0])
            y = np.random.randint(0, self.grid_size[1])

            # Check distance to existing centers
            if all(np.sqrt((x - cx)**2 + (y - cy)**2) >= min_distance for cx, cy in centers):
                centers.append((x, y))

            attempts += 1

        # If we couldn't place all groups with minimum distance, fill randomly
        while len(centers) < n:
            x = np.random.randint(0, self.grid_size[0])
            y = np.random.randint(0, self.grid_size[1])
            centers.append((x, y))

        return centers

    def _assign_territories(self, centers: List[Tuple[int, int]]):
        """Assign territory cells to groups using nearest center"""
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                # Find nearest group center
                distances = [np.sqrt((x - cx)**2 + (y - cy)**2) for cx, cy in centers]
                nearest_group = np.argmin(distances)

                self.territory_map[x, y] = nearest_group
                self.groups[nearest_group].territory.append((x, y))

    def step(self):
        """Execute one time step of the simulation"""
        self.year += 1

        # Determine if this is a shortfall year (instance variable so other methods can access)
        # Duration scales with magnitude: mild (0.2) = 1 year, severe (0.8) = 3 years
        shortfall_duration = max(1, int(1 + self.shortfall_magnitude * 2.5))  # 1-3 years
        years_since_shortfall_start = self.year % self.shortfall_frequency
        self.is_shortfall = years_since_shortfall_start > 0 and years_since_shortfall_start <= shortfall_duration

        current_productivity = self.base_productivity * (
            (1 - self.shortfall_magnitude) if self.is_shortfall else 1.0
        )

        # Update productivity map
        self.productivity_map = np.ones(self.grid_size) * current_productivity

        # Phase 1: Growth and monument investment
        for group in self.groups.values():  # Changed to .values()
            self._group_growth(group, current_productivity)

        # Phase 1.5: Resource sharing among signaling groups during shortfalls
        self._resource_sharing()

        # Phase 2: Border conflicts
        conflicts_this_year = self._resolve_border_conflicts()

        # Phase 3: Remove extinct groups
        self.groups = {gid: g for gid, g in self.groups.items() if g.population > 1.0}  # Changed to dict comprehension

        # Update history
        self._update_history(conflicts_this_year)

    def _group_growth(self, group: Group, productivity: float):
        """Handle group population growth and monument investment"""
        available_resources = group.territory_size * productivity
        carrying_capacity = group.territory_size * self.carrying_capacity_per_cell

        if group.strategy == Strategy.COSTLY_SIGNALING:
            # Invest in monuments, reducing reproductive capacity
            monument_investment = available_resources * self.monument_cost
            group.monument_investment += monument_investment

            # Growth with reduced resources
            resources_for_growth = available_resources * (1 - self.monument_cost)
            base_growth_rate = 0.05  # 5% annual growth

            # MECHANISM 2A: Monument buffer during shortfalls
            # Accumulated monuments represent stored resources/organization that helps during crises
            # Scale buffer benefit by magnitude: more severe shortfall = more valuable buffer
            if self.is_shortfall:
                # Mild (0.2): buffer_scale = 0.5; Severe (0.8): buffer_scale = 2.0
                buffer_scale = 0.25 + self.shortfall_magnitude * 2.0
                buffer_bonus = min(0.4, group.monument_investment / (group.population * 100) * self.monument_buffer_factor * buffer_scale)
                resources_for_growth *= (1 + buffer_bonus)

        else:  # HIGH_REPRODUCTION
            # All resources go to reproduction
            resources_for_growth = available_resources
            base_growth_rate = 0.05 * (1 + self.reproduction_bonus)  # Enhanced reproduction

            # MECHANISM 2B: High reproduction groups hit HARDER during shortfalls
            # Larger populations are more vulnerable (more mouths to feed, no reserves)
            if self.is_shortfall:
                vulnerability_penalty = min(0.3, group.population / carrying_capacity * 0.2)
                resources_for_growth *= (1 - vulnerability_penalty)

        # Apply logistic growth with carrying capacity
        growth = base_growth_rate * group.population * (1 - group.population / carrying_capacity)

        # Scale by resource availability
        resource_factor = min(1.0, resources_for_growth / (group.population * 0.5))
        growth *= resource_factor

        group.population += growth
        group.population = min(group.population, carrying_capacity)

        # Update history
        group.history['population'].append(group.population)
        group.history['monument'].append(group.monument_investment)

    def _resource_sharing(self):
        """
        MECHANISM 3: During shortfalls, signaling groups share resources with adjacent signaling groups.
        This creates cooperation networks that buffer against resource stress.
        Monument building signals trustworthiness, enabling reciprocal sharing.
        """
        if not self.is_shortfall:
            return  # Only share during shortfalls

        # Find signaling groups
        signaling_groups = [g for g in self.groups.values() if g.strategy == Strategy.COSTLY_SIGNALING]

        if len(signaling_groups) < 2:
            return  # Need at least 2 signaling groups to share

        # Calculate surplus/deficit for each signaling group based on carrying capacity
        for group in signaling_groups:
            carrying_capacity = group.territory_size * self.carrying_capacity_per_cell
            resource_ratio = group.population / carrying_capacity if carrying_capacity > 0 else 1.0

            # Groups below 60% capacity need resources, above 70% can share
            if resource_ratio < 0.6:
                group._needs_resources = True
                group._resource_deficit = 0.6 - resource_ratio
            elif resource_ratio > 0.7:
                group._can_share = True
                group._resource_surplus = resource_ratio - 0.7
            else:
                group._needs_resources = False
                group._can_share = False

        # Share resources between adjacent signaling groups
        for group in signaling_groups:
            if not getattr(group, '_can_share', False):
                continue

            neighbors = self._get_neighboring_groups(group)
            signaling_neighbors = [
                self.groups[n] for n in neighbors
                if n in self.groups and self.groups[n].strategy == Strategy.COSTLY_SIGNALING
            ]

            # Find needy neighbors
            needy_neighbors = [n for n in signaling_neighbors if getattr(n, '_needs_resources', False)]
            if not needy_neighbors:
                continue

            # Calculate sharing amount based on surplus and sharing rate
            # Scale sharing by magnitude: more severe shortfall = more sharing needed/valuable
            # Mild (0.2): share_scale = 0.6; Severe (0.8): share_scale = 1.8
            share_scale = 0.4 + self.shortfall_magnitude * 1.75
            share_amount = group.population * self.cooperation_sharing_rate * group._resource_surplus * share_scale
            per_neighbor_share = share_amount / len(needy_neighbors)

            # Transfer resources (as population buffer - represents shared food/support)
            for neighbor in needy_neighbors:
                # Receiver gains (with efficiency loss in transfer)
                neighbor.population += per_neighbor_share * 0.5
                # Sharer pays a smaller cost (reciprocity is beneficial)
                group.population -= per_neighbor_share * 0.25

        # Clean up temporary attributes
        for group in signaling_groups:
            if hasattr(group, '_needs_resources'):
                delattr(group, '_needs_resources')
            if hasattr(group, '_can_share'):
                delattr(group, '_can_share')
            if hasattr(group, '_resource_deficit'):
                delattr(group, '_resource_deficit')
            if hasattr(group, '_resource_surplus'):
                delattr(group, '_resource_surplus')

    def _resolve_border_conflicts(self) -> int:
        """Resolve conflicts at territorial borders"""
        conflicts = 0
        conflict_pairs = set()

        # Find all border cells and potential conflicts
        for group in self.groups.values():  # Changed to .values()
            neighbors = self._get_neighboring_groups(group)

            for neighbor_id in neighbors:
                # Skip if neighbor no longer exists (extinct group)
                if neighbor_id not in self.groups:
                    continue

                # Avoid double-counting
                pair = tuple(sorted([group.id, neighbor_id]))
                if pair in conflict_pairs:
                    continue

                neighbor = self.groups[neighbor_id]

                # Determine conflict probability
                conflict_prob = self._calculate_conflict_probability(group, neighbor)

                if np.random.random() < conflict_prob:
                    conflicts += 1
                    conflict_pairs.add(pair)
                    self._resolve_conflict(group, neighbor)

        return conflicts

    def _get_neighboring_groups(self, group: Group) -> set:
        """Get IDs of groups with adjacent territories"""
        neighbors = set()

        for x, y in group.territory:
            # Check adjacent cells
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_size[0] and 0 <= ny < self.grid_size[1]:
                    neighbor_id = self.territory_map[nx, ny]
                    if neighbor_id != group.id and neighbor_id >= 0:
                        neighbors.add(neighbor_id)

        return neighbors

    def _calculate_conflict_probability(self, group1: Group, group2: Group) -> float:
        """Calculate probability of conflict between two neighboring groups"""
        # Base conflict probability depends on resource availability
        # In good times: less competition, fewer conflicts
        # In bad times: scarce resources drive conflict, SCALED BY MAGNITUDE
        if self.is_shortfall:
            # Scale conflict probability by shortfall magnitude
            # Mild shortfall (0.2): 0.05 + 0.2*0.30 = 0.11
            # Severe shortfall (0.8): 0.05 + 0.8*0.30 = 0.29
            base_conflict_prob = 0.05 + self.shortfall_magnitude * 0.30
        else:
            base_conflict_prob = 0.05  # Only 5% base chance in good times

        # Monument investment reduces conflict - MUCH stronger effect during shortfalls
        avg_monument_investment = (
            group1.monument_investment / max(1, group1.population) +
            group2.monument_investment / max(1, group2.population)
        ) / 2

        monument_factor = 1.0
        if avg_monument_investment > 0:
            # Scale deterrence by signaling_conflict_reduction (r)
            # r=0.75 is baseline; higher r = stronger deterrence
            r_scale = self.signaling_conflict_reduction / 0.75

            if self.is_shortfall:
                # Strong deterrence during shortfalls - monuments really matter
                # Scale deterrence by magnitude: more severe = monuments matter more
                # Mild (0.2): divisor = 3 + (1-0.2)*20 = 19 (weak)
                # Severe (0.8): divisor = 3 + (1-0.8)*20 = 7 (strong)
                deterrence_divisor = 3.0 + (1.0 - self.shortfall_magnitude) * 20.0
                monument_factor = 1.0 / (1.0 + (avg_monument_investment / deterrence_divisor) * r_scale)
            else:
                # Very weak deterrence in good times
                monument_factor = 1.0 / (1.0 + (avg_monument_investment / 40.0) * r_scale)

        # High reproduction groups are more aggressive during shortfalls
        # Scale aggression by magnitude: more severe = more desperate/aggressive
        aggression_factor = 1.0
        if group1.strategy == Strategy.HIGH_REPRODUCTION or group2.strategy == Strategy.HIGH_REPRODUCTION:
            if self.is_shortfall:
                # Mild (0.2): 1.0 + 0.2*1.5 = 1.3
                # Severe (0.8): 1.0 + 0.8*1.5 = 2.2
                aggression_factor = 1.0 + self.shortfall_magnitude * 1.5
            # No aggression penalty in good times - plenty for everyone

        conflict_prob = base_conflict_prob * monument_factor * aggression_factor

        return min(0.5, conflict_prob)  # Cap at 50%

    def _resolve_conflict(self, group1: Group, group2: Group):
        """Resolve conflict between two groups"""
        # Monument investment provides defensive advantage - STRONGER DURING SHORTFALLS
        # In good times, minimal defensive benefit (monuments are mostly display)
        # In bad times, monuments provide major organization, fortification, and coordination
        # Scale by signaling_conflict_reduction (r): higher r = stronger defensive bonus
        r_scale = self.signaling_conflict_reduction / 0.75

        if self.is_shortfall:
            # Strong defensive bonus from monuments during shortfalls
            monument_bonus1 = group1.monument_investment / (group1.population + 1) * r_scale
            monument_bonus2 = group2.monument_investment / (group2.population + 1) * r_scale
        else:
            # Very small defensive bonus in good times
            monument_bonus1 = group1.monument_investment / (group1.population + 1) * 0.05 * r_scale
            monument_bonus2 = group2.monument_investment / (group2.population + 1) * 0.05 * r_scale

        strength1 = group1.population * (1 + monument_bonus1)
        strength2 = group2.population * (1 + monument_bonus2)

        # Determine winner probabilistically
        win_prob = strength1 / (strength1 + strength2)

        if np.random.random() < win_prob:
            winner, loser = group1, group2
        else:
            winner, loser = group2, group1

        # Apply casualties - during shortfalls, conflicts are more devastating
        if self.is_shortfall:
            mortality_mult = 1.5  # More deadly conflicts when resources are scarce
        else:
            mortality_mult = 1.0

        winner.population *= (1 - self.conflict_mortality * 0.5 * mortality_mult)  # Winners lose less
        loser.population *= (1 - self.conflict_mortality * mortality_mult)  # Losers lose more

        winner.conflicts_won += 1
        loser.conflicts_lost += 1

        # Track conflicts
        winner.history['conflicts'][-1] += 1
        loser.history['conflicts'][-1] += 1

    def _update_history(self, conflicts: int):
        """Update simulation-level history"""
        total_pop = sum(g.population for g in self.groups.values())  # Changed to .values()
        self.history['total_population'].append(total_pop)

        for strategy in Strategy:
            pop = sum(g.population for g in self.groups.values() if g.strategy == strategy)  # Changed to .values()
            self.history['population_by_strategy'][strategy].append(pop)

        self.history['conflicts_per_year'].append(conflicts)

        signaling_groups = [g for g in self.groups.values() if g.strategy == Strategy.COSTLY_SIGNALING]  # Changed to .values()
        avg_monument = np.mean([g.monument_investment for g in signaling_groups]) if signaling_groups else 0
        self.history['avg_monument_investment'].append(avg_monument)

    def run(self, years: int):
        """Run simulation for specified number of years"""
        for _ in range(years):
            self.step()

    def get_summary_statistics(self) -> dict:
        """Get summary statistics from simulation"""
        stats = {
            'final_year': self.year,
            'total_population': self.history['total_population'][-1] if self.history['total_population'] else 0,
            'groups_remaining': len(self.groups),
            'total_conflicts': sum(self.history['conflicts_per_year']),
        }

        for strategy in Strategy:
            groups = [g for g in self.groups.values() if g.strategy == strategy]  # Changed to .values()
            stats[f'{strategy.value}_groups'] = len(groups)
            stats[f'{strategy.value}_population'] = sum(g.population for g in groups)
            stats[f'{strategy.value}_avg_territory'] = np.mean([g.territory_size for g in groups]) if groups else 0

        return stats
