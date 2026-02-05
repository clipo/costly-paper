# Supplementary Materials

## The Demographic Paradox of Monumental Architecture: An Agent-Based Model of Costly Signaling Under Resource Uncertainty

---

## S1. Modified Price Equation: Technical Derivation

### S1.1 Standard Price Equation for Multilevel Selection

The Price equation in its multilevel selection form decomposes the change in population-average trait frequency as:

$$\Delta\bar{p} = \frac{1}{\bar{w}} \text{Cov}(w_g, p_g) + \frac{1}{\bar{w}} E(w_g \Delta p_g)$$

where $\bar{p}$ is the population-average frequency of the trait (here, the signaling strategy), $w_g$ is the fitness of group $g$, $p_g$ is the frequency of signalers in group $g$, and $\bar{w}$ is mean population fitness.

The first term, $\text{Cov}(w_g, p_g)/\bar{w}$, represents between-group selection. When groups with more signalers have higher fitness, this covariance is positive, favoring the spread of signaling. The second term, $E(w_g \Delta p_g)/\bar{w}$, represents the fitness-weighted average of within-group change. Because signalers pay a reproductive cost, within-group selection typically acts against signaling, making this term negative.

### S1.2 Environmental Uncertainty Parameter

We extend this framework by making fitness components explicit functions of environmental uncertainty. We define a composite uncertainty parameter $\sigma$ that captures the combined effect of shortfall frequency, magnitude, and duration:

$$\sigma = \frac{\text{magnitude} \times \text{duration}}{\text{frequency}}$$

where frequency is measured in years between shortfall events (higher values = less frequent), magnitude is the proportional reduction in productivity (0 to 1), and duration is the number of years the shortfall persists. High $\sigma$ indicates an environment with frequent, severe, prolonged shortfalls.

In our model, duration depends on magnitude according to the formula: duration = max(1, int(1 + magnitude × 2.5)). For mild shortfalls with magnitude 0.2, this yields a duration of 1 year and σ = 0.2/frequency. For moderate shortfalls with magnitude 0.5, the duration is 2 years and σ = 1.0/frequency. For severe shortfalls with magnitude 0.8, the duration extends to 3 years and σ = 2.4/frequency.

Applying these calculations to our case studies: Rapa Nui with frequency=6, magnitude=0.6, and duration=2 yields σ = (0.6 × 2)/6 = 0.20. Rapa Iti with frequency=18, magnitude=0.3, and duration=1 yields σ = (0.3 × 1)/18 = 0.017.

### S1.3 Strategy-Specific Fitness Functions

We model fitness as depending on three components:

**Survival Component.** During resource shortfalls, groups must survive on reduced resources. We assume signalers have a survival advantage because their signals attract cooperation from other groups or because signal quality correlates with underlying resource management capacity:

$$S_{\text{signal}}(\sigma) = 1 - \alpha\sigma$$
$$S_{\text{non-signal}}(\sigma) = 1 - \beta\sigma$$

where $\alpha < \beta$, indicating that signalers experience smaller survival penalties under uncertainty. The parameter $\alpha$ represents signaler vulnerability and $\beta$ represents non-signaler vulnerability to environmental shocks.

**Conflict Component.** Groups compete for resources, with conflict more likely during shortfalls. We assume signals deter conflict, reducing mortality from intergroup competition:

$$M_{\text{signal}}(\sigma) = m_0(1 - r)$$
$$M_{\text{non-signal}}(\sigma) = m_0$$

where $m_0$ is baseline conflict mortality and $r$ is the conflict reduction factor achieved through signaling (monument-mediated deterrence). We assume $r$ is independent of $\sigma$ but note that conflict frequency may itself increase with uncertainty.

**Reproductive Cost.** Signalers divert a fraction $C$ of their resources to signal production (monument construction), reducing reproductive output:

$$R_{\text{signal}} = 1 - C$$
$$R_{\text{non-signal}} = 1$$

### S1.4 Combined Fitness Expressions

Combining these components multiplicatively, the fitness of signalers and non-signalers becomes:

$$W_{\text{signal}}(\sigma) = (1-C) \times (1 - \alpha\sigma) \times (1 - m_0(1-r))$$

$$W_{\text{non-signal}}(\sigma) = 1 \times (1 - \beta\sigma) \times (1 - m_0)$$

The selection coefficient favoring signaling is:

$$s(\sigma) = W_{\text{signal}}(\sigma) - W_{\text{non-signal}}(\sigma)$$

### S1.5 Critical Threshold Derivation

Signaling is favored when $s(\sigma) > 0$. To find the critical threshold, we set $W_{\text{signal}} = W_{\text{non-signal}}$:

$$(1-C)(1 - \alpha\sigma^*)(1 - m_0(1-r)) = (1 - \beta\sigma^*)(1 - m_0)$$

Expanding the left side:
$$(1-C)(1 - m_0 + m_0 r)(1 - \alpha\sigma^*)$$

Let $A = (1-C)(1 - m_0 + m_0 r)$ and $B = (1 - m_0)$. Then:

$$A(1 - \alpha\sigma^*) = B(1 - \beta\sigma^*)$$
$$A - A\alpha\sigma^* = B - B\beta\sigma^*$$
$$A - B = A\alpha\sigma^* - B\beta\sigma^*$$
$$A - B = \sigma^*(A\alpha - B\beta)$$

$$\sigma^* = \frac{A - B}{A\alpha - B\beta}$$

Substituting back:
$$\sigma^* = \frac{(1-C)(1 - m_0 + m_0 r) - (1 - m_0)}{(1-C)(1 - m_0 + m_0 r)\alpha - (1 - m_0)\beta}$$

For small $m_0$, this simplifies. To first order in $m_0$:

$$\sigma^* \approx \frac{(1-C)(1 + m_0 r) - 1}{(1-C)(1 + m_0 r)\alpha - \beta}$$

$$\sigma^* \approx \frac{-C + (1-C)m_0 r}{(1-C)\alpha - \beta + (1-C)m_0 r \alpha}$$

For the simplest approximation (neglecting conflict terms entirely):

$$\sigma^* \approx \frac{C}{\beta - (1-C)\alpha}$$

### S1.6 Parameter Estimates and Numerical Values

Based on archaeological and ethnographic evidence, we estimate:

| Parameter | Symbol | Estimate | Source |
|-----------|--------|----------|--------|
| Reproductive cost | $C$ | 0.35 | Monument labor investment (35% of group productivity) |
| Signaler vulnerability | $\alpha$ | 0.30 | Estimated survival with cooperation networks |
| Non-signaler vulnerability | $\beta$ | 0.90 | Estimated survival without cooperation |
| Baseline conflict mortality | $m_0$ | 0.15 | Ethnographic conflict rates |
| Conflict reduction | $r$ | 0.75 | Monument deterrence effect (75% reduction) |

Using the simplified formula:

$$\sigma^* = \frac{0.35}{0.90 - (1-0.35) \times 0.30} = \frac{0.35}{0.90 - 0.195} = \frac{0.35}{0.705} \approx 0.50$$

Using the full formula with conflict terms yields a lower critical threshold σ*, as the conflict benefits provide additional selection pressure favoring signaling at lower uncertainty levels. The specific value of σ* depends on these parameter choices.

### S1.7 Relationship to Existing Theory

Our approach differs from previous extensions of the Price equation under uncertainty:

**Grafen (2000)** showed that arithmetic mean fitness is maximized under uncertainty when reproductive value is properly weighted. This resolved questions about geometric vs. arithmetic mean optimization but did not parameterize environmental conditions explicitly.

**Rice (2008)** developed a stochastic Price equation revealing "even-moment" and "odd-moment" effects. His framework shows how fitness variance and skewness affect selection. Our approach differs in that we model strategy-specific fitness responses to environmental stress rather than general moment properties of fitness distributions.

**Frank (2012)** clarified connections between the Price equation and Fisher information. While providing deep mathematical foundations, this work did not address environmental parameterization for generating predictions.

Our key innovations are: (1) the explicit $\sigma$ parameterization measurable from paleoclimate data; (2) strategy-specific fitness functions $W(\sigma)$ where environmental stress differentially affects strategies; (3) derivation of a quantitative threshold $\sigma^*$ enabling prediction; (4) the mechanism is differential survival during crises (between-group selection) rather than variance reduction (bet-hedging).

**Note on the σ threshold and ABM phase space:** The analytical threshold σ* provides an approximate indicator of when costly signaling becomes favored, but the ABM phase space boundary is not a constant-σ contour. The specific value of σ* depends on model parameters including signaling costs, vulnerability coefficients, and conflict reduction rates. The boundary in (frequency, magnitude) coordinates reflects the full nonlinear dynamics of spatial competition, stochastic shortfall timing, and parameter interactions not captured in the simplified analytical model. For empirical classification of specific cases, the ABM-derived phase space should be used directly, while the σ formula provides conceptual guidance for understanding why environmental combinations with high magnitude, long duration, and frequent occurrence favor costly signaling strategies.

---

## S2. Parameter Estimation and Calibration

This section provides detailed justification for model parameters, including archaeological and ethnographic sources.

### S2.1 Theoretical Model Parameters

**Reproductive Cost (C = 0.35)**

The reproductive cost parameter represents the fraction of group productivity diverted to monument construction. We estimate C = 0.35 (35%) based on several lines of evidence:

- **Experimental archaeology on Rapa Nui**: Moai transport experiments (Lipo et al. 2013; Hunt and Lipo 2011) demonstrate that moving a 4.4-ton moai replica required 18 people working coordinated shifts. Extrapolating to the full corpus of nearly 1,000 moai plus 300 ahu platforms suggests substantial sustained labor investment.

- **Comparative monument labor studies**: Abrams (1994) developed methods for estimating labor investment in monumental architecture. For Maya monuments, labor estimates range from 20-40% of community productive capacity during construction phases. Erasmus (1965) estimated that Mesoamerican monument construction consumed 25-35% of available labor in monument-building communities.

- **Ethnographic parallels**: Rappaport (1968) documented that Maring kaiko festivals in Papua New Guinea, which involve pig sacrifices and ceremonial displays functioning as costly signals, consume approximately 30-40% of annual household production. Sosis and Bressler (2003) found that successful religious communes imposed costs equivalent to 20-40% of members' resources.

- **Sensitivity analysis**: We tested C values from 0.20 to 0.50. The qualitative pattern (diagonal phase-space boundary) persists across this range, though the boundary position shifts. Our choice of C = 0.35 represents a mid-range estimate consistent with archaeological and ethnographic evidence.

**Signaler Vulnerability (α = 0.30) and Non-Signaler Vulnerability (β = 0.90)**

These parameters represent the proportional increase in mortality during environmental stress for signaling and non-signaling groups respectively. The ratio β/α captures the survival advantage signalers obtain through cooperation networks and resource sharing.

- **Ethnographic evidence for cooperation benefits**: Wiessner (1982) documented that !Kung San hxaro exchange networks reduced starvation risk by approximately 60-70% during drought years. Cashdan (1985) showed that Basarwa groups with stronger reciprocal ties experienced significantly lower mortality during resource shortfalls.

- **Archaeological mortality differentials**: Steckel and Rose (2002) found that skeletal stress markers in prehistoric North American populations varied substantially with evidence of community integration. Populations with evidence of cooperative institutions showed 40-60% lower frequencies of Harris lines and enamel hypoplasias during climatically stressful periods.

- **Theoretical grounding**: Winterhalder (1986) modeled risk-pooling among foragers, showing that groups practicing generalized reciprocity reduce variance in food intake by 50-80% compared to non-sharing groups. Our α = 0.30 and β = 0.90 imply that signalers experience only 33% of the mortality vulnerability of non-signalers (0.30/0.90), consistent with these ethnographic observations.

**Baseline Conflict Mortality (m₀ = 0.15)**

This parameter represents the annual probability of conflict-related mortality in the absence of signaling deterrence.

- **Ethnographic conflict rates**: Bowles (2009) compiled data on intergroup conflict mortality among hunter-gatherers, finding average annual mortality rates from warfare of 0.5-2% of population. Keeley (1996) documented higher rates (up to 25% of adult male deaths) in some tribal societies with active warfare.

- **Archaeological evidence**: Skeletal trauma frequencies in prehistoric populations suggest conflict mortality of 5-20% of individuals over lifetimes (Walker 2001; Lambert 2002). For annual rates, this translates to approximately 0.5-2% per year, though rates spike during resource stress.

- **Scaling considerations**: Our m₀ = 0.15 represents the cumulative mortality risk from conflict events rather than annual background rates. During simulation years with territorial competition, approximately 15% of the losing group's population dies from conflict. This is consistent with ethnographic accounts of raiding casualties (Chagnon 1988; Ember and Ember 1992).

**Conflict Reduction (r = 0.75)**

The conflict reduction parameter represents the decrease in conflict probability when both interacting groups are monument builders.

- **Costly signaling theory**: Zahavi (1975) and Grafen (1990) established that costly signals reduce conflict by providing reliable information about competitive ability. When both parties can accurately assess relative strength, costly conflicts become less likely because outcomes are predictable.

- **Archaeological correlates**: DiNapoli et al. (2019) found that Rapa Nui ahu locations correlate with freshwater sources, interpreted as territorial markers signaling resource control. The spatial regularity of ahu placement (approximately 2 km intervals along the coast) suggests successful territorial negotiation rather than constant boundary conflict.

- **Ethnographic parallels**: Wiessner (2006) documented that Enga tee exchange cycles in Papua New Guinea, which involve ceremonial pig transfers between groups, reduce intergroup raiding by approximately 60-80% compared to groups without exchange relationships. Our r = 0.75 (75% reduction) falls within this range.

- **Sensitivity analysis**: We tested r values from 0.50 to 0.90. Higher values strengthen the case for signaling but require stronger assumptions about signal effectiveness. Our choice of r = 0.75 is conservative relative to ethnographic observations of exchange-based conflict reduction.

### S2.2 Environmental Parameters: Rapa Nui

**Shortfall Magnitude (0.6)**

We estimate 60% productivity reduction during drought events based on:

- **Paleoclimate reconstruction**: Margalef et al. (2025) analyzed sediment cores from Rano Raraku and Rano Kao crater lakes, documenting 50-67% precipitation deficits during the 1550-1700 CE drought period. Their multi-proxy analysis (pollen, charcoal, geochemistry) provides direct evidence of drought severity.

- **Modern analogs**: Markovitz et al. (2025) documented the 2010-2023 megadrought on Rapa Nui, with precipitation deficits of 40-60% relative to 20th-century means. Agricultural productivity declined proportionally, with water rationing required for the modern population.

- **ENSO teleconnections**: Delcroix et al. (2022) established that Rapa Nui precipitation is strongly correlated with ENSO phases. El Niño events produce 30-50% below-normal rainfall, while La Niña events produce 20-40% above normal. Multi-year El Niño sequences (as documented for 1550-1700 CE) compound these deficits.

**Shortfall Frequency (6 years)**

We estimate major shortfall events occurring approximately every 6 years based on:

- **ENSO periodicity**: ENSO events occur every 2-7 years (NOAA 2024), with major El Niño events (producing severe Rapa Nui drought) at approximately 6-8 year intervals. The 1982-83, 1997-98, and 2015-16 super El Niño events fit this periodicity.

- **Paleoclimate evidence**: Margalef et al. (2025) identified multiple drought phases within the 1550-1700 CE period, suggesting recurring rather than continuous stress. Sediment geochemistry shows cyclical patterns consistent with 5-8 year ENSO forcing.

- **Agricultural recovery time**: Stevenson et al. (2015) modeled Rapa Nui agricultural productivity, finding that sweet potato and taro cultivation required 2-3 years to recover from major drought. A 6-year cycle allows partial recovery between events while maintaining chronic stress.

**Base Productivity (0.8)**

The base productivity value of 0.8 (relative to optimal = 1.0) reflects Rapa Nui's marginal agricultural conditions:

- **Soil limitations**: Ladefoged et al. (2010) documented that Rapa Nui soils are young volcanic substrates with limited nutrient retention. Only 20% of the island surface is suitable for intensive cultivation.

- **Rainfall limitations**: Mean annual precipitation is approximately 1,200 mm (Delcroix et al. 2022), marginal for Polynesian crops. By comparison, Hawaii receives 2,000-4,000 mm in agricultural zones; Tahiti receives 1,500-2,000 mm.

- **Carrying capacity estimates**: Puleston et al. (2017) modeled Rapa Nui carrying capacity at 4,000-7,500 individuals under optimal conditions. The archaeological population estimate of approximately 3,000 (Boersema and Huele 2019; Lipo et al. 2022) suggests populations remained well below theoretical maximum, consistent with productivity limitations.

### S2.3 Environmental Parameters: Rapa Iti

**Shortfall Magnitude (0.3)**

We estimate 30% productivity reduction during stress events, based primarily on modern climate analogy:

- **Modern precipitation**: Rapa Iti receives approximately 2,500 mm annual rainfall (Climate Data 2024), more than double Rapa Nui's 1,200 mm. This abundant rainfall buffers agricultural productivity against drought.

- **Geographic position**: Located at 27°S latitude (compared to Rapa Nui's 27°S but further from ENSO centers), Rapa Iti experiences attenuated ENSO effects. Drought magnitude is typically 40-60% less severe than at Rapa Nui.

- **Paleoclimate gap**: No paleoclimate reconstructions exist for Rapa Iti. Our estimate relies on modern climate interpolation and should be treated as provisional pending sediment core analysis from the Austral Islands.

**Shortfall Frequency (18 years)**

We estimate major shortfall events approximately every 18 years:

- **ENSO attenuation**: While ENSO affects the entire Pacific, teleconnection strength decreases with distance from the equatorial Pacific. Rapa Iti's position south of the main ENSO corridor reduces drought frequency.

- **Modern observations**: Climate records for the Austral Islands show significant precipitation deficits occurring approximately once per decade, with major droughts (>30% reduction) at approximately 15-20 year intervals.

- **Archaeological inference**: The absence of monuments on Rapa Iti (despite cultural capacity inherited from shared Polynesian ancestry) suggests environmental conditions did not favor signaling strategies. Our frequency estimate is calibrated to produce model outcomes consistent with this archaeological pattern.

**Base Productivity (1.2)**

The base productivity value of 1.2 reflects Rapa Iti's favorable agricultural conditions:

- **Rainfall abundance**: At 2,500 mm annually, Rapa Iti receives sufficient rainfall for intensive Polynesian horticulture without irrigation.

- **Soil fertility**: Like Rapa Nui, Rapa Iti has volcanic soils, but higher rainfall promotes weathering and nutrient cycling, enhancing agricultural potential.

- **Population density**: At European contact, Rapa Iti supported 1,500-2,000 people on approximately 40 km² (Anderson and Kennett 2012), yielding population densities of 37-50 people/km². This is 2-3 times Rapa Nui's density (approximately 18 people/km²), consistent with higher productivity.

### S2.4 Parameter Uncertainty and Sensitivity

All parameter estimates carry uncertainty. We address this through:

- **Sensitivity analysis**: Section S3 documents robustness across 10,400 simulations with varying parameters.

- **Conservative choices**: Where evidence is ambiguous, we select parameter values that weaken rather than strengthen our conclusions. For example, our C = 0.35 is at the lower end of ethnographic estimates for ceremonial investment.

- **Qualitative predictions**: The key finding (diagonal phase-space boundary) is robust to parameter variation. The specific value of σ* depends on parameter choices, but the qualitative pattern persists.

- **Future calibration**: Approximate Bayesian Computation methods could formally estimate parameters from archaeological data, reducing reliance on ethnographic analogy.

---

## S3. Agent-Based Model Technical Details

### S3.1 Spatial Structure

The landscape consists of a 40×40 grid containing 1600 cells, initially divided among 16-20 groups. Each cell is characterized by:
- **Ownership**: Which group controls the cell
- **Productivity**: Base values ranging from 0.8 to 1.2, subject to stochastic shortfalls
- **Carrying capacity**: Maximum population density at 8-15 individuals per cell
- **Monument investment**: Cumulative costly signaling by controlling group

Groups occupy contiguous territories. Territory size, productivity, and carrying capacity together determine demographic potential.

### S3.2 Strategic Variation

**Monument building (costly signaling)**:
- Invests 35% of annual productivity in monument construction
- Monuments provide no direct subsistence benefit (pure cost)
- Yields 75% conflict reduction when interacting with other monument builders
- Signals surplus capacity and coordination ability

**High reproduction**:
- Redirects would-be monument resources to reproduction
- Applies 40-50% bonus to population growth
- Maximizes demographic expansion during productive periods
- Tolerates higher conflict rates (no signaling deterrence)

### S3.3 Annual Simulation Cycle

**Phase 1: Resource Production**
- Each cell generates resources according to base productivity (0.8-1.2)
- Stochastic shortfalls occur at intervals set by frequency parameter (5-20 years)
- Magnitude (0.2-0.8) affects both depth of reduction and duration
- Duration formula: max(1, int(1 + magnitude × 2.5))
- Total group production = sum across controlled cells

**Phase 2: Resource Allocation**
- Monument builders: 35% to monuments, 65% to population support
- High reproduction: 100% to population support + 40-50% bonus

**Phase 3: Population Dynamics**
- Deaths: natural mortality + conflict casualties + starvation (when resources < population needs)
- Births: proportional to available resources after costs
- Population cannot exceed carrying capacity (sum of cell capacities)

**Phase 4: Territorial Competition**
- Groups attempt expansion into neighboring cells along contested borders
- Conflict probability depends on strategy pairing:
  - Both monument builders: 25% of baseline (75% reduction)
  - Mixed or both high-reproduction: 100% baseline
- Conflict outcomes depend on:
  - Population size (larger groups more likely to win)
  - Monument investment (signals commitment)
  - Stochastic element (historical contingency)
- Losers suffer 20-25% population mortality

**Phase 5: Extinction and Inheritance**
- Groups with population < 1 go extinct
- Territory absorbed by neighbors proportional to shared border length

### S3.4 Environmental Parameter Calibration

**Rapa Nui:**
- Magnitude: 0.6 (60% reduction based on Margalef et al. 2025 sediment cores showing 50-67% deficits)
- Frequency: 6 years (ENSO-driven drought clustering)
- Duration: 2-3 years (derived from magnitude)
- Base productivity: 0.8 (marginal conditions)
- Carrying capacity: 8 per cell (supports ~3000 population estimate)

**Rapa Iti:**
- Magnitude: 0.3 (30% reduction, modern climate analogy)
- Frequency: 18 years (rare shortfalls)
- Duration: 1 year (mild shortfalls)
- Base productivity: 1.2 (abundant rainfall: 2500mm/year)
- Carrying capacity: 15 per cell (higher density sustainable)

---

## S4. Sensitivity Analysis and Robustness

To assess whether the patterns reported in the main text reflect robust dynamics or stochastic artifacts, we conducted 5 independent phase-space explorations totaling 10,400 simulations.

### S4.1 Methodology

Each phase-space exploration consisted of 208 parameter combinations (16 frequency values × 13 magnitude values) with 10 replicate simulations per combination, yielding 2,080 simulations per run. The 5 independent runs used different random seeds to assess variability in outcomes.

![Figure S1](../../figures/final/supplementary/Figure_S1_sensitivity_analysis.png)

**Figure S1. Sensitivity Analysis Across 10,400 Simulations.** *Results from 5 complete phase-space explorations with different random seeds. The phase-space structure is robust across all runs, with the diagonal boundary consistently separating signaling-favorable from reproduction-favorable regions. Variability is concentrated near the transition boundary, where stochastic factors can tip outcomes, while interior regions show consistent strategy dominance.*

### S4.2 Stability Metrics

The sensitivity analysis reveals meaningful variation across runs, reflecting the stochastic nature of the underlying dynamics while maintaining robust core patterns.

**Strategy switches**: Approximately 34% of parameter space points (71 out of 208) showed different dominant strategies across some runs. This variability concentrates near the transition boundary where strategies have similar fitness. Points far from the boundary show consistent outcomes across all runs.

**Mean standard deviation**: The average standard deviation in dominance values across the 5 runs was 0.10. This indicates moderate but meaningful variation, particularly near the competitive equilibrium.

**Regional stability**:
- Upper-left region (frequent severe shortfalls): Consistently shows positive dominance (monument building favored) across all runs
- Lower-right region (rare mild shortfalls): Consistently shows negative dominance (high reproduction favored) across all runs
- Transition zone: Shows greatest variability, with some points switching dominant strategy between runs

### S4.3 Boundary Variability

Panel F of Figure S1 overlays the dominance=0 contour line from all 5 runs. The lines show some spread, indicating that the exact position of the transition boundary varies with stochastic factors. However, several features are robust:

1. **Orientation**: The boundary runs diagonally from upper-left to lower-right in all runs
2. **Slope**: The relationship between frequency and magnitude is consistent
3. **Location**: The boundary passes through approximately the same region of parameter space (frequency 8-12, magnitude 0.3-0.6)

### S4.4 Uncertainty Envelopes

Panels D and E show slices through parameter space with shaded uncertainty envelopes (mean ± 1 standard deviation).

**Frequency slice** (Panel D): At high magnitude (0.7), varying frequency from 5 to 20 years shows:
- Clear positive dominance at low frequency (5-8 years)
- Transition to negative dominance at high frequency (15-20 years)
- Uncertainty envelope widens near the transition point

**Magnitude slice** (Panel E): At frequent shortfalls (7 years), varying magnitude from 0.2 to 0.8 shows:
- Clear negative dominance at low magnitude (0.2-0.3)
- Transition to positive dominance at high magnitude (0.6-0.8)
- Narrower uncertainty envelope compared to frequency slice

### S4.5 Robustness Implications

The stability analysis yields several important methodological findings:

1. **Core patterns are deterministic**: Despite stochastic variation in individual simulations, the phase-space structure is reproducible. The fundamental finding—that frequent severe shortfalls favor monument building while stable environments favor high reproduction—emerges consistently.

2. **Boundary uncertainty is real**: Near competitive equilibrium, outcomes genuinely depend on historical contingency. This is theoretically appropriate: when strategies have similar fitness, small differences in initial conditions or event timing can determine outcomes.

3. **Magnitude affects both depth and duration**: The more complex dynamics introduced by duration-dependent shortfalls create additional stochasticity. Severe shortfalls lasting 3 years create more opportunities for demographic events to compound.

4. **Predictions remain useful**: For most of the parameter space (66% of points), outcomes are consistent across runs. Archaeological predictions based on environmental parameters are reliable except near the transition boundary.

---

## S5. Demographic Paradox: Detailed Results

This section provides the detailed quantitative results supporting the demographic paradox findings reported in the main text.

### S5.1 Controlled Comparison Under Moderate-High Stress

Controlled comparison of homogeneous populations using all monument-building versus all high-reproduction strategies under identical environmental conditions (frequency=8 years, magnitude=0.6):

**Table S1. Strategy Comparison Under Uniform Conditions**

| Metric | All Monument | All Reproduction | Difference |
|--------|--------------|------------------|------------|
| Final Population | 1,189 ± 67 | 1,532 ± 134 | -343 (-22%) |
| Cumulative Conflicts | 128 ± 23 | 1,247 ± 187 | -1,119 (-90%) |
| Conflict Deaths | 32 ± 6 | 312 ± 47 | -280 (-90%) |
| Shortfall Deaths | 45 ± 12 | 187 ± 43 | -142 (-76%) |
| Total Deaths | 892 ± 34 | 1,456 ± 89 | -564 (-39%) |

Monument construction reduces final population by 22% but reduces total mortality by 39%. The "missing" population never existed because monument builders have lower birth rates due to resource diversion. The per capita survival rate is higher among monument builders: 892 deaths across 1,189 population (0.75 deaths/capita), compared with 1,456 deaths across 1,532 population (0.95 deaths/capita) for high-reproduction groups.

### S5.2 Mixed Strategy Competition

When both strategies coexist and compete in the same environment:

**Table S2. Competitive Outcomes Under Mixed Strategies**

| Metric | Monument Builders | High Reproduction | Ratio |
|--------|-------------------|-------------------|-------|
| Final Population | 1,104 | 143 | 7.7:1 |
| Total Deaths | 187 | 934 | 0.2:1 |
| Deaths per Capita | 0.17 | 6.53 | 0.03:1 |

High-reproduction groups suffer 38 times higher per-capita mortality when competing against monument builders in stressful environments. The demographic trap mechanism operates through density-dependent mortality: high-reproduction groups boost population, exceed carrying capacity during shortfalls, experience catastrophic mortality, engage in desperate territorial conflicts, and approach extinction.

---

## S6. Model Limitations and Archaeological Visibility

### S6.1 Archaeological Visibility and Testability

A critical consideration for archaeological application is how the predicted patterns would manifest in the material record. The model generates predictions at multiple scales, each with different archaeological visibility.

**Monument-building signatures**: Monument-building strategies produce obvious archaeological signatures—the monuments themselves. Ahu platforms, moai statues, earthworks, and megalithic structures are durable and visible. Investment intensity can be quantified through monument counts, sizes, construction phases, and labor estimates.

**High-reproduction signatures**: Distinguishing high-reproduction strategies requires attention to multiple lines of evidence:

- **Settlement patterns**: High-reproduction strategies should produce more nucleated settlements reflecting population pressure, more frequent settlement relocations indicating territorial instability, and evidence of defensive architecture such as fortifications, ditches, and palisades.

- **Demographic profiles**: High-reproduction populations should show higher proportions of subadults in skeletal assemblages, reflecting higher fertility, though potentially with greater mortality variability.

- **Conflict evidence**: High-conflict environments should show elevated frequencies of skeletal trauma, particularly perimortem injuries consistent with interpersonal violence.

- **Alternative investments**: High-reproduction strategies under environmental stress might invest in storage facilities and agricultural intensification rather than monuments. The presence of substantial storage infrastructure without corresponding monument investment would suggest reproduction-favoring environmental conditions.

The contrast between Rapa Nui's dispersed coastal settlements, organized around *ahu* platforms, and Rapa Iti's fortified *pare* settlements illustrates this predicted difference.

### S6.2 Temporal Resolution

Our model operates at annual timesteps, but archaeological chronologies rarely achieve such precision. Patterns predicted at annual scales—boom-bust cycles, conflict spikes during shortfalls—would appear smoothed at the typical archaeological resolution of 50-100 year bins.

However, the long-term outcomes should remain detectable:
- Strategy dominance (which strategy comprises the majority of final population)
- Equilibrium population (total population at simulation end)
- Cumulative monument investment (total resources invested in monuments)
- Conflict frequency (total conflicts over simulation period)

Bayesian chronological modeling, as employed by Mulrooney et al. (2010) for Rapa Nui, offers the precision needed to correlate monument construction phases with paleoclimate reconstructions.

### S6.3 Model Simplifications

Several simplifying assumptions merit detailed acknowledgment:

**Binary strategies**: Our model employs two discrete strategies (monument building vs. high reproduction), whereas real societies likely exhibit a continuum of monument investment from minimal to extensive. Future models should implement:
- Graded investment levels (0-100% of resources to monuments)
- Strategy evolution through learning or cultural transmission
- Mixed strategies within populations

**Conflict resolution**: Our conflict mechanism uses simplified resolution based on population size, monument investment, and stochasticity. Real conflict involves:
- Coalition formation and alliance networks
- Technology and weapon asymmetries
- Terrain and defensive advantages
- Tactical and strategic choices
- Negotiation and conflict avoidance

More sophisticated conflict models could test whether our results remain robust to alternative combat dynamics.

**Single resource type**: We model a single generic "productivity" resource without distinguishing:
- Marine versus terrestrial resources
- Wild versus cultivated resources
- Storable versus perishable resources

Different resource types exhibit different buffering properties. Storable grains buffer shortfalls more effectively than fresh fish. Models incorporating resource portfolios could reveal additional dynamics.

**Fixed strategies**: Strategies are treated as fixed group traits, though real monument-building traditions spread through imitation, migration, and cultural learning. Agent-based models with explicit cultural transmission mechanisms (Boyd and Richerson 1985) could test whether signaling strategies spread as predicted by cultural evolutionary theory.

**Stationary environments**: We model stationary environments with constant shortfall frequency and magnitude, whereas real climates shift over centuries. The Rapa Nui drought ended around 1720 CE, and monument construction ceased shortly thereafter. Future models should implement non-stationary environments to test adaptation to changing conditions.

**Signaling mechanism**: We assume monument building signals pre-existing group capacity rather than solving coordination problems. Models incorporating explicit cooperation dilemmas (public goods games, collective action problems) could test whether monuments function to maintain cooperation under stress.

---

## S7. Empirical Gaps and Validation

### S7.1 Paleoclimate Data

**Rapa Nui**: Our environmental parameters are grounded in empirical paleoclimate reconstructions:
- Margalef et al. (2025) documented 50-67% precipitation deficits from sediment cores
- The 1550-1700 CE drought provides the primary calibration
- The 2010-2023 megadrought (Markovitz et al. 2025) offers modern validation

**Rapa Iti**: Parameters rely on modern climate analogy rather than paleoclimate reconstructions. Sediment cores from the Austral Islands would enable proper empirical calibration. Key uncertainties include:
- Historical drought frequency prior to European contact
- ENSO teleconnection patterns in the Austral Islands
- Seasonal precipitation variability

### S7.2 Archaeological Measures

Several archaeological measures could test model predictions:

**Conflict frequency**: We lack direct archaeological measures of pre-contact conflict rates. Systematic analysis could provide empirical benchmarks:
- Skeletal trauma frequencies and patterns
- Fortification construction chronologies
- Weapon densities in archaeological deposits
- Settlement pattern changes indicating defensive concerns

**Monument timing**: While DiNapoli et al. (2019) demonstrated spatial correlations between monuments and freshwater, high-resolution chronologies correlating specific monument construction episodes with paleoclimate proxies would strengthen causal claims. Required data include:
- Bayesian chronological models for monument construction phases
- Multi-proxy paleoenvironmental reconstructions at matching resolution
- Statistical tests of construction-climate correlations

**Population estimates**: Archaeological population estimates for pre-contact Polynesia rely on multiple methods:
- Skeletal age-at-death distributions (Boersema and Huele 2019)
- Genetic effective population size estimates (Ioannidis et al. 2021)
- Settlement pattern analysis (Lipo et al. 2022)
- Carrying capacity models based on agricultural productivity

Cross-validation of these methods would strengthen population estimates used to test model predictions.

### S7.3 Monument Labor Costs

We assume 35% productivity diversion to monuments, but this requires empirical validation. Quantification approaches include:

**Experimental archaeology**: Reconstruction projects (e.g., moai transport experiments) provide labor estimates for specific construction tasks.

**Energetics studies**: Caloric requirements for quarrying, transport, and construction can be estimated from physiological models and compared to population food production.

**Ethnoarchaeological analogs**: Observations of traditional construction in societies with similar technologies provide comparative labor data.

**Archaeological residues**: Tool wear patterns, quarry debris volumes, and construction waste can indicate labor intensity.

---

## S8. Future Directions

### S8.1 Cross-Cultural Comparison

Systematic comparison of monument-building versus non-monument-building societies across environmental gradients could test whether phase-space predictions generalize:

**Pacific Islands**: Compare monument traditions across:
- Hawaii (variable by island, with heiau construction intensifying during political competition)
- Marquesas (monumental architecture present in variable environment)
- Tonga and Samoa (varying monument traditions with different environmental contexts)
- New Zealand (pa fortifications rather than ceremonial monuments)

**North American Southwest**: Compare:
- Chaco Canyon great houses (drought-prone environment)
- Hohokam ball courts (variable desert environment)
- Ancestral Pueblo cliff dwellings (defensive architecture in competitive contexts)

**Neolithic Europe**: Compare:
- Atlantic megalithic monuments (marginal coastal environments)
- Central European longhouses (productive loess soils)
- Mediterranean temple complexes (island environments)

### S8.2 Multi-Millennial Simulations

Extending simulations to multi-millennial timescales would test whether monument-building traditions emerge and disappear as predicted by environmental forcing:

**Climate transitions**:
- Medieval Warm Period to Little Ice Age
- Younger Dryas to Holocene
- Bond events and their archaeological correlates

**Cultural evolution**:
- Emergence of monument-building traditions
- Abandonment patterns
- Strategy transitions during environmental change

### S8.3 Methodological Extensions

**Multi-strategy models**: Allowing continuous variation in monument investment, intermediate strategies, and strategy switching would test evolutionary stability under more realistic conditions.

**Parameter estimation**: Approximate Bayesian Computation or similar methods could estimate model parameters directly from archaeological data, testing whether empirically fitted models reproduce observed patterns without requiring subjective parameter selection.

**Spatial heterogeneity**: Incorporating landscape variation (coastal vs. interior, fertile valleys vs. marginal uplands) could reveal landscape-specific patterns in monument investment.

**Cultural transmission**: Explicit models of how monument-building traditions spread through imitation, teaching, and migration could test whether signaling strategies propagate as predicted by cultural evolutionary theory.

### S8.4 Generalization to Other Costly Signals

Testing whether other costly behaviors show similar environmental contingency would determine whether the phase-space structure generalizes:

**Ritual elaboration**: Do complex ritual traditions emerge under the same conditions as monument building?

**Warfare intensity**: Does conflict frequency correlate with environmental uncertainty as predicted?

**Feasting and exchange**: Do prestige economies track environmental parameters?

**Body modification**: Do costly signals like tattooing, scarification, and cranial modification follow similar patterns?

If multiple costly signaling systems show parallel environmental contingency, this would suggest a general principle of cultural evolution under uncertainty.

---

## S9. Supplementary References

Abrams, E.M., 1994. How the Maya Built Their World: Energetics and Ancient Architecture. University of Texas Press.

Anderson, A., Kennett, D.J. (Eds.), 2012. Taking the High Ground: The Archaeology of Rapa, a Fortified Island in Remote East Polynesia (Terra Australis 37). ANU E Press, Canberra.

Bowles, S., 2009. Did warfare among ancestral hunter-gatherers affect the evolution of human social behaviors? Science 324, 1293-1298.

Boyd, R., Richerson, P.J., 1985. Culture and the Evolutionary Process. University of Chicago Press.

Cashdan, E., 1985. Coping with risk: Reciprocity among the Basarwa of northern Botswana. Man 20, 454-474.

Chagnon, N.A., 1988. Life histories, blood revenge, and warfare in a tribal population. Science 239, 985-992.

Climate Data, 2024. Rapa Iti climate data. Available at: https://www.climate-data.org/

Delcroix, T., et al., 2022. Clarifying the role of ENSO on Easter Island precipitation changes. Paleoceanography and Paleoclimatology 37, e2022PA004514.

Ember, C.R., Ember, M., 1992. Resource unpredictability, mistrust, and war: A cross-cultural study. Journal of Conflict Resolution 36, 242-262.

Erasmus, C.J., 1965. Monument building: Some field experiments. Southwestern Journal of Anthropology 21, 277-301.

Frank, S.A., 2012. Natural selection. IV. The Price equation. Journal of Evolutionary Biology 25, 1002-1019.

Grafen, A., 1990. Biological signals as handicaps. Journal of Theoretical Biology 144, 517-546.

Grafen, A., 2000. Developments of the Price equation and natural selection under uncertainty. Proceedings of the Royal Society B 267, 1223-1227.

Hunt, T.L., Lipo, C.P., 2011. The Statues that Walked: Unraveling the Mystery of Easter Island. Free Press.

Keeley, L.H., 1996. War Before Civilization: The Myth of the Peaceful Savage. Oxford University Press.

Ladefoged, T.N., et al., 2010. Soil nutrient analysis of Rapa Nui gardening. Archaeology in Oceania 45, 80-85.

Lambert, P.M., 2002. The archaeology of war: A North American perspective. Journal of Archaeological Research 10, 207-241.

Lipo, C.P., Hunt, T.L., Haoa, S.R., 2013. The 'walking' megalithic statues (moai) of Easter Island. Journal of Archaeological Science 40, 2859-2866.

NOAA, 2024. What are El Niño and La Niña? National Ocean Service.

Puleston, C.O., et al., 2017. Rain, sun, soil, and sweat: A consideration of population limits on Rapa Nui. Frontiers in Ecology and Evolution 5, 69.

Rappaport, R.A., 1968. Pigs for the Ancestors: Ritual in the Ecology of a New Guinea People. Yale University Press.

Rice, S.H., 2008. A stochastic version of the Price equation reveals the interplay of deterministic and stochastic processes in evolution. BMC Evolutionary Biology 8, 262.

Sosis, R., Bressler, E.R., 2003. Cooperation and commune longevity: A test of the costly signaling theory of religion. Cross-Cultural Research 37, 211-239.

Steckel, R.H., Rose, J.C. (Eds.), 2002. The Backbone of History: Health and Nutrition in the Western Hemisphere. Cambridge University Press.

Stevenson, C.M., et al., 2015. Variation in Rapa Nui (Easter Island) land use indicates production and population peaks prior to European contact. PNAS 112, 1025-1030.

Walker, P.L., 2001. A bioarchaeological perspective on the history of violence. Annual Review of Anthropology 30, 573-596.

Wiessner, P., 1982. Risk, reciprocity and social influences on !Kung San economics. In: Leacock, E., Lee, R. (Eds.), Politics and History in Band Societies. Cambridge University Press, pp. 61-84.

Wiessner, P., 2006. From spears to M-16s: Testing the imbalance of power hypothesis among the Enga. Journal of Anthropological Research 62, 165-191.

Winterhalder, B., 1986. Diet choice, risk, and food sharing in a stochastic environment. Journal of Anthropological Archaeology 5, 369-392.

Zahavi, A., 1975. Mate selection: A selection for a handicap. Journal of Theoretical Biology 53, 205-214.

Boersema, J.J., Huele, R., 2019. Pondering the population numbers of Easter Island's past. In: Vogt, B., Kühlem, A., Mieth, A., Bork, H.-R. (Eds.), Easter Island and the Pacific. Rapa Nui Press, pp. 83-92.

DiNapoli, R.J., Lipo, C.P., Brosnan, T., Hunt, T.L., Hixon, S., Morrison, A.E., Becker, M., 2019. Rapa Nui (Easter Island) monument (ahu) locations explained by freshwater sources. PLoS ONE 14(1), e0210409.

Ioannidis, A.G., et al., 2021. Paths and timings of the peopling of Polynesia inferred from genomic networks. Nature 597, 522-526.

Lipo, C.P., DiNapoli, R.J., Hunt, T.L., 2022. Claims and evidence in the population history of Rapa Nui. In: Vogt, B., et al. (Eds.), The Prehistory of Rapa Nui. Springer, pp. 511-540.

Margalef, O., et al., 2025. Prolonged drought on Rapa Nui during the decline of the monument-building culture. Communications Earth & Environment 6, 1-10.

Markovitz, Y., et al., 2025. Contemporary megadrought on Easter Island (Rapa Nui) since 2010. Geophysical Research Letters 52, e2025GL115880.

Mulrooney, M.A., et al., 2010. A Bayesian approach to determining radiocarbon age from multiple samples. Journal of Archaeological Science 37, 2759-2771.
