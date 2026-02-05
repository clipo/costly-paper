# The Paradox of Monumental Architecture: An Agent-Based Model of Costly Signalling Under Resource Uncertainty

*Running title: Costly Signalling and Monumental Architecture*

---

## Abstract

Monumental architecture presents a demographic paradox: why invest resources in non-utilitarian construction when those resources could support larger populations? We extend the Price equation for multilevel selection to incorporate environmental uncertainty, deriving a critical threshold above which between-group selection sustains costly signalling despite within-group reproductive costs. Agent-based simulations validate this prediction, revealing a phase-space boundary that separates signalling-favourable from reproduction-favourable environmental regimes. Applied to Polynesian case studies, the framework correctly predicts that Rapa Nui's monument tradition emerges under frequent droughts, whereas Rapa Iti invests in fortifications under stable conditions. The paradox resolves when we recognise that a smaller population is not a cost but the mechanism enabling competitive advantage by reducing conflict under environmental uncertainty.

**Keywords:** Price equation, costly signalling theory, monumental architecture, agent-based modelling, Rapa Nui, environmental uncertainty, multilevel selection, cultural evolution

## 1. Introduction

### 1.1 The puzzle of monumental architecture

Monumental architecture represents one of the most conspicuous and enduring puzzles in the archaeological record. Across all inhabited continents and throughout human history, societies have invested extraordinary labour in structures whose primary function appears symbolic rather than utilitarian [1,2]. The geographic and temporal scope of this phenomenon is remarkable. Gobekli Tepe's megalithic enclosures in southeastern Turkey (ca. 9500 BCE) were constructed by mobile hunter-gatherers who lacked agriculture, permanent settlements, or any apparent economic surplus [3,4]. Stonehenge in southern England underwent multiple phases of construction spanning over a millennium (ca. 3000-1500 BCE), mobilising communities across vast distances to transport and erect massive stones in a landscape already marked by earlier earthwork monuments [5]. The Middle Woodland Hopewell earthworks of the Ohio Valley (ca. 100 BCE - 500 CE) comprise some of the largest geometric enclosures ever constructed, including the Newark Earthworks' Great Circle and Octagon covering over 12 hectares, yet were built by dispersed populations without centralised political authority [6,7]. Poverty Point in Louisiana (ca. 1700-1100 BCE) required an estimated 238,000 cubic metres of earth moved by pre-agricultural hunter-gatherer-fishers to construct its massive mound and concentric ridges [8]. The Maltese temple complexes (ca. 3600-2500 BCE) represent the earliest free-standing stone structures in the world, constructed on small, resource-limited islands [9]. Perhaps the most famous example is Rapa Nui, where nearly 1,000 moai statues and approximately 300 ahu platforms were carved and transported beginning around 1100 CE across a remote, environmentally marginal island whose population never exceeded a few thousand individuals [10-12].

This global pattern presents a fundamental puzzle: why divert scarce resources from food production, population growth, or defensive infrastructure into "wasteful" displays? The demographic costs appear prohibitive. Communities investing heavily in monument construction channel resources away from activities that could support larger populations, whether through intensified food production, expanded territorial control, or life history strategies favouring higher fertility. The tradeoff is not simply between "building monuments" and "having children," but reflects deeper demographic strategies. Under unpredictable environmental conditions, monument-building communities may adopt more conservative reproductive strategies, investing more heavily in fewer offspring to buffer against resource shortfalls. This pattern is consistent with K-selected life histories, where parental investment per child increases at the expense of total fertility, enhancing offspring survival during periods of scarcity. The cumulative investment is staggering: conservative estimates suggest Stonehenge's sarsen circle alone required over 20 million person-hours of labour [13], while Rapa Nui's moai transport demanded coordinated efforts from communities whose total labour pool numbered only a few hundred adults.

### 1.2 Traditional explanations and their limitations

Several influential frameworks have been proposed to explain monumental construction, yet each struggles to account for critical patterns in the archaeological record.

The surplus accumulation model, most closely associated with Childe's [14] concept of the "Urban Revolution," posited that monumental construction became possible only after agricultural intensification produced economic surplus beyond subsistence needs. Monuments, in this view, represent the materialisation of accumulated wealth. Yet this model fails spectacularly for the earliest monuments. Gobekli Tepe predates the domestication of plants and animals in Southwest Asia by at least a millennium [15]. Poverty Point's massive earthworks were constructed by hunter-gatherer-fishers without agriculture. Even where agriculture is present, investment in monuments often intensifies during periods of resource stress rather than abundance [16]. Rapa Nui ahu construction increased during drought periods, precisely when surplus would be least available.

The aggrandiser or competitive feasting model [17,18] proposes that ambitious individuals ("aggrandisers") mobilised labour for monumental projects to establish and maintain social dominance through competitive display. While this framework helpfully centres human agency, it struggles to explain monuments that precede evidence for social hierarchy. The earliest phases of Stonehenge and Gobekli Tepe provide no clear evidence of ranked societies or hereditary leadership [3]. The Hopewell earthworks were constructed by societies whose mortuary evidence suggests relatively egalitarian social organisation [19]. If aggrandisers require followers, what motivated participation before hierarchical institutions existed to compel it?

The population pressure model suggests that monument construction emerges in response to demographic stress, either as territorial markers in resource competition or as integrative institutions that bind growing populations [20]. Yet monument builders frequently sustained smaller populations than non-monument-building neighbours in ecologically similar environments. The Hopewell heartland supported lower population densities than contemporaneous Fort Ancient societies, which built far fewer monumental structures [21]. Rapa Nui's population of approximately 3,000 individuals [22,23] is modest for a 164 km² subtropical island, whereas the similarly situated island of Rapa Iti supported a dense population of 1,500-2,000 in only 40 km² without comparable investment in monuments.

The state formation and ideological control model [2,24] proposes that elites constructed monuments to materialise ideology, naturalise inequality, and legitimate political authority. This model fits later monuments (e.g., Egyptian pyramids, Maya temples, Khmer complexes) but cannot explain the origins of monumentality in pre-state societies. Gobekli Tepe, Stonehenge's earliest phases, Poverty Point, and the Maltese temples all precede state formation by millennia in their respective regions.

### 1.3 The timing and location problem

Perhaps the most damaging evidence against traditional explanations is the systematic pattern in the timing and location of societies' investments in monuments. If surplus accumulation drove monumentality, we would expect monuments to cluster in the most productive environments. If population pressure drove monumentality, we would expect monuments to be concentrated in the most densely populated regions. If state power drove monumentality, we would expect monuments to follow political centralisation.

Instead, the archaeological record reveals a striking counter-pattern. Monumental construction often appears earliest and most intensively in marginal environments, among dispersed populations, and prior to social complexity. Rapa Nui is among the most remote and resource-limited islands in Polynesia, yet it produced among the most intensive monument traditions. Gobekli Tepe sits on an upland plateau without permanent water sources, an unlikely location for surplus accumulation. The Ohio Hopewell earthworks were constructed by dispersed communities practising low-intensity horticulture, not by centralised polities with agricultural intensification. Malta's temples were built on small islands with limited agricultural potential.

The timing is equally puzzling. Monuments frequently appear at the onset of environmental deterioration rather than during optimal conditions. DiNapoli et al. [16] demonstrated that Rapa Nui ahu construction accelerated during documented drought periods [25]. Banning [26] argued that Gobekli Tepe's construction coincided with Late Pleistocene climate instability. The Middle Woodland florescence of Hopewell earthwork construction occurred during a period of increasingly variable climate [7]. This pattern of investment intensifying precisely when resources are scarce directly contradicts surplus-based explanations.

### 1.4 The comparative problem

Perhaps most telling is what contemporaneous populations in nearby regions were doing instead of building monuments. Monument construction was never universal; it represented one strategic choice among alternatives. Critically, populations sharing recent common ancestry, similar technologies, and overlapping cultural traditions consistently diverged in their investment strategies when occupying different environmental contexts.

The pattern is consistent across world regions. While Gobekli Tepe's builders invested in megalithic construction, their cultural relatives in the Jordan Valley invested in plant cultivation, storage, and village infrastructure, occupying predictable riparian environments that supported larger populations [27,28]. Stonehenge represents an extraordinary achievement of inter-community cooperation: populations from across Britain coordinated to transport bluestones over 200 kilometres from Wales, quarry and move sarsen stones weighing up to 25 tons, and sustain construction efforts spanning generations [13]. Yet their relatives elsewhere lived very differently. Across much of the North European Plain and into Central Europe, contemporaneous populations with shared ancestry lived in small, autonomous farming households and villages, with no comparable large-scale cooperation [29,30]. Even within Britain, monument building concentrated in upland and marginal zones with unpredictable resources, while lowland communities with reliable agricultural soils remained dispersed in small settlements [31].

This comparative pattern sets up the central comparison of this study. Rapa Nui and Rapa Iti represent an ideal test case: they share immediate Polynesian ancestry, similar colonisation timing, and comparable cultural toolkits, yet their archaeological records diverge dramatically [32]. Rapa Nui, with its frequent droughts, produced nearly 1,000 moai and 300 ahu platforms yet sustained only about 3,000 persons over its 164 km². Rapa Iti, though much smaller at 40 km², supported population densities two to three times higher (37-50 versus 18 people per km²). Fortified refuge sites on Rapa Iti appeared only during later periods of inter-group competition [33]. These are not random cultural differences but predictable strategic divergences in response to different environmental selection pressures.

### 1.5 Evolutionary approaches and costly signalling

Evolutionary approaches to monument construction have developed along three distinct but related theoretical traditions. Evolutionary waste theory [34] proposed that energy expenditure that does not directly enhance reproduction could be maintained by selection when it represents excess capacity that buffers populations against environmental unpredictability. Costly signalling theory [35,36] proposes that expensive displays can be adaptive when they credibly signal qualities that observers value, with the costs preventing dishonest signalling. Bet-hedging theory [37] frames costly behaviours as insurance against environmental uncertainty, sacrificing mean reproductive output to reduce variance.

Archaeological applications of costly signalling theory have proliferated over the past two decades [1]. Glatz and Plourde [38] demonstrated that Hittite landscape monuments cluster in contested borderlands, consistent with predictions that signalling investment should increase in frontier zones. Kolb [39] interpreted Hawaiian heiau temple construction as costly signals of chiefly authority, with larger monuments correlating with political centralisation. DiNapoli et al. [16] used spatially explicit point-process modelling to show that Rapa Nui ahu locations correlate with critical freshwater sources, interpreted as conspicuous displays marking community resource control. Crucially, DiNapoli's analysis found that investment in monuments increased during drought periods, suggesting that environmental stress intensified signalling competition.

Ethnographic studies of costly signalling reinforce these patterns. Bliege Bird et al. [40] documented how Martu Aboriginal women's cooperative hunting functions as costly signalling that establishes social hierarchies and cooperative relationships. Sosis and Bressler [41] found that religious communes in 19th-century America that imposed more costly requirements survived longer than secular communes, despite presumably lower fertility.

These frameworks may not be mutually exclusive alternatives so much as complementary perspectives on the same underlying dynamics. A society that invests in monument construction simultaneously demonstrates excess capacity (waste), signals commitment to potential competitors (costly signalling), and maintains population below carrying capacity to buffer against shortfalls (bet-hedging). The question is not which mechanism is "correct" but rather under what conditions each mechanism contributes to adaptive outcomes.

### 1.6 Demographic tradeoffs and the Price equation

Most costly signalling models assume a constant population size or rely on fitness proxies rather than explicitly modelling demographic dynamics. This obscures a critical question: can costly signalling be adaptive even when it produces smaller populations? Empirically, this pattern appears common. Rapa Nui invested heavily in monument construction yet sustained a population of approximately 3,000 individuals [22,23,42], which is low for an island of 164 km² compared with tropical Polynesian islands of similar size. Gobekli Tepe mobilised hunter-gatherers for monumental construction without an agricultural surplus, suggesting resource diversion from immediate subsistence [3].

The relationship between environmental uncertainty and reproductive strategies has received extensive treatment in behavioural ecology. Winterhalder et al. [37] developed risk-sensitive adaptive tactics models showing that organisms facing environmental unpredictability should adopt variance-minimising strategies even at the cost of lower mean returns. Halstead and O'Shea [43] documented diverse cultural buffering mechanisms against "bad years," including storage, exchange networks, and mobility, but did not consider costly signalling as a buffering strategy.

The Price equation for multilevel selection [44,45] provides the mathematical framework for analysing when group-level traits can persist despite individual-level costs. The equation partitions evolutionary change into between-group selection (covariance between group fitness and trait frequency) and within-group selection (expected change within groups). For costly signalling to persist, between-group benefits must exceed within-group costs:

$$\text{Cov}(w_g, p_g) > -E(w_g \Delta p_g)$$

That is, the covariance between group fitness and signaller frequency (the between-group selection term) must exceed the expected within-group decline in signaller frequency weighted by group fitness. Within-group selection typically opposes costly signalling because signallers divert resources from reproduction. For signalling to spread, between-group selection must be sufficiently strong, operating through differential survival of groups containing signallers.

The critical question is: under what conditions does between-group selection become strong enough? The standard Price equation treats environmental conditions as an implicit background, offering limited predictive power. Here, we address this limitation by extending the Price equation to incorporate environmental uncertainty as an explicit parameter, enabling quantitative predictions about when monument building should evolve.

### 1.7 Research questions

We address these gaps using an agent-based model that integrates spatially-explicit group territories with competitive border conflicts, explicit demographic dynamics, resource productivity with stochastic shortfalls, and alternative strategies comparing monument building versus high reproduction. Our central questions are fourfold. First, what combinations of resource uncertainty favour costly signalling over high reproduction? Second, can costly signalling be adaptive even when it produces smaller populations? Third, do empirically-grounded environmental parameters for Rapa Nui and Rapa Iti predict their observed cultural trajectories? Fourth, can we derive a quantitative threshold from the modified Price equation that matches simulation results?

## 2. Theoretical framework: extending the Price equation

### 2.1 Relationship to existing theory

Several important contributions have explored the Price equation under stochastic environments. Grafen [46] addressed whether organisms should maximise arithmetic or geometric mean fitness under uncertainty, showing that natural selection maximises arithmetic mean fitness when reproductive value is properly weighted. Rice [47] developed a stochastic extension revealing an "even-moment effect" where selection can favour traits that reduce fitness variance. Frank [48] provided a comprehensive review of the equation's mathematical properties.

Our approach differs in four key respects. First, we introduce an explicit environmental uncertainty parameter measurable from palaeoclimate and archaeological data. Second, we derive strategy-specific fitness functions where uncertainty differentially affects competing strategies. Third, we derive a critical threshold that provides quantitative predictions. Fourth, we identify differential survival during environmental crises as the key mechanism, creating between-group selection that overcomes within-group costs rather than relying on variance reduction per se.

### 2.2 The modified Price equation

The standard Price equation for multilevel selection decomposes evolutionary change as:

$$\Delta\bar{p} = \frac{\text{Cov}(w_g, p_g)}{\bar{w}} + \frac{E(w_g \Delta p_g)}{\bar{w}}$$

where the first term represents between-group selection (covariance between group fitness and trait frequency) and the second represents within-group selection (fitness-weighted average of within-group change). For costly signalling to spread, between-group benefits must exceed within-group costs.

Our modification makes both terms explicit functions of environmental uncertainty σ. Group fitness becomes:

$$w_g(\sigma) = p_g \cdot W_{\text{signal}}(\sigma) + (1 - p_g) \cdot W_{\text{non-signal}}(\sigma)$$

The key insight is that σ modulates the relative strength of between-group versus within-group selection. As σ increases, differential survival during environmental crises increases fitness variance between groups, thereby strengthening the between-group selection term. Above a critical threshold σ*, between-group selection becomes strong enough to overcome within-group costs, and costly signalling is favoured.

### 2.3 Environmental uncertainty parameter

We define a composite environmental uncertainty parameter σ that captures the combined effect of shortfall frequency, magnitude, and duration:

$$\sigma = \frac{\text{magnitude} \times \text{duration}}{\text{frequency}}$$

where frequency is measured in years between shortfall events (higher values = less frequent), magnitude is the proportional reduction in productivity (0 to 1), and duration is the number of years the shortfall persists. High σ indicates an environment characterised by frequent, severe, and prolonged shortfalls. This parameter is measurable from palaeoclimate reconstructions and serves as a bridge between environmental conditions and evolutionary dynamics.

In our model, duration depends on magnitude: duration = max(1, int(1 + magnitude × 2.5)). This captures the empirical pattern that severe droughts tend to persist longer than mild ones.

### 2.4 Strategy-specific fitness functions

We model fitness as depending on three components.

**Survival component.** During shortfalls, groups must survive on reduced resources. We assume signallers have a survival advantage because their signals attract cooperation or because signal quality correlates with resource management capacity:

$$S_{\text{signal}}(\sigma) = 1 - \alpha\sigma; \quad S_{\text{non-signal}}(\sigma) = 1 - \beta\sigma$$

where α < β indicates signallers experience smaller survival penalties.

**Conflict component.** Groups compete for resources, with conflict more likely during shortfalls. Signals deter conflict, reducing mortality:

$$M_{\text{signal}} = m_0(1 - r); \quad M_{\text{non-signal}} = m_0$$

where m₀ is baseline conflict mortality and r is the conflict reduction factor.

**Reproductive cost.** Signallers divert a fraction C of resources to signal production:

$$R_{\text{signal}} = 1 - C; \quad R_{\text{non-signal}} = 1$$

### 2.5 Critical threshold derivation

Combining these components, the fitness of signallers and non-signallers becomes:

$$W_{\text{signal}}(\sigma) = (1 - C)(1 - \alpha\sigma)(1 - m_0(1 - r))$$

$$W_{\text{non-signal}}(\sigma) = (1 - \beta\sigma)(1 - m_0)$$

Signalling is favoured when W_signal > W_non-signal. Setting these equal and solving for the critical threshold (full derivation in electronic supplementary material):

$$\sigma^* \approx \frac{C}{\beta - (1 - C)\alpha}$$

### 2.6 Parameter justification

We estimate model parameters from archaeological and ethnographic evidence (full justification in electronic supplementary material).

**Reproductive cost (C = 0.35)**: Monument construction diverts approximately 35% of group productivity. This estimate draws on experimental archaeology of moai transport [49], comparative labour studies showing Mesoamerican monument construction consumed 25-40% of community capacity [50,51], and ethnographic observations that Maring kaiko festivals consume 30-40% of household production [52].

**Vulnerability differential (α = 0.30, β = 0.90)**: Signallers experience lower mortality during crises due to cooperation networks. Ethnographic evidence shows that !Kung hxaro exchange networks reduced starvation risk by 60-70% during drought [53], and Basarwa groups with stronger reciprocal ties experienced significantly lower shortfall mortality [54]. Our parameters imply signallers experience approximately one-third the vulnerability of non-signallers.

**Baseline conflict mortality (m₀ = 0.15)**: Annual conflict mortality draws on Bowles' [55] compilation of hunter-gatherer warfare data (0.5-2% annual mortality) and Keeley's [56] analysis showing conflict deaths of 15-25% in tribal societies with active warfare.

**Conflict reduction (r = 0.75)**: Costly signals deter conflict through honest information about competitive ability [35,36]. Ethnographic evidence from Enga tee exchanges shows that ceremonial displays reduce intergroup raiding by 60-80% [57].

Using these parameters: σ* = 0.35 / (0.90 - 0.65 × 0.30) = 0.35 / 0.705 ≈ 0.50. The key insight is not the specific numerical value but that such a critical threshold exists, providing a boundary where the dominant strategy switches.

### 2.7 Theoretical predictions

This framework generates specific, testable predictions. The environmental parameter space should show a diagonal boundary separating signalling-favourable regions (high uncertainty) from reproduction-favourable regions (low uncertainty). The mechanism predicts that costly signalling succeeds through differential survival during crises, creating between-group selection that overcomes within-group reproductive costs. This leads to a demographic paradox: signalling-favourable regions should show lower total populations but higher competitive success. Archaeologically, monument building should correlate with high environmental uncertainty, while stable environments should favour demographic maximisation and defensive strategies such as fortifications.

## 3. Methods: agent-based model validation

### 3.1 Model overview

To validate the theoretical framework, we developed a spatially-explicit agent-based model representing competing groups on an island landscape. Agent-based modelling has become an essential tool for archaeological research, enabling exploration of complex adaptive systems [58]. Our approach follows traditions established in studies of Kayenta Anasazi dynamics [59] and Mesa Verde polity formation [60].

The model simulates 100-200 year trajectories at annual time steps, tracking territory control, population dynamics, resource production, monument investment, and conflict outcomes. Two strategies compete: monument builders that invest 35% of productivity in signals (reducing conflict by 75% through mutual deterrence) and high-reproduction groups that maximise demographic growth.

### 3.2 Spatial structure

The landscape consists of a 40×40 grid containing 1600 cells, initially divided among 16-20 groups depending on the scenario. Each cell is characterised by four attributes: ownership, indicating which group controls it; productivity, with base values ranging from 0.8 to 1.2 that are subject to stochastic shortfalls; carrying capacity, defining maximum population density at 8-15 individuals per cell; and monument investment, tracking cumulative costly signalling by the controlling group.

### 3.3 Strategic variation

Each group adopts one of two strategies representing fundamentally different approaches to resource allocation. The costly signalling strategy invests 35% of annual productivity in monument construction. These monuments provide no direct subsistence benefit and represent a pure cost that reduces immediate population growth. However, investment in monuments yields a 75% reduction in conflict probability when interacting with other monument-building neighbours.

The high reproduction strategy redirects resources that would otherwise go to monuments into additional reproduction, applying a 40-50% bonus to population growth. This strategy maximises demographic expansion during productive periods but tolerates higher conflict rates.

### 3.4 Model dynamics

Each simulated year proceeds through five phases. The first phase calculates resource production, where each cell generates resources according to its base productivity value. Stochastic shortfalls occur at intervals determined by the shortfall frequency parameter (every 5-20 years). Importantly, the magnitude of the shortfall (ranging from 0.2 to 0.8) affects both the depth of productivity reduction and the duration: mild shortfalls of 0.2 magnitude last only 1 year, whereas severe shortfalls of 0.8 magnitude persist for 2-3 years.

The second phase handles resource allocation. Monument-building groups allocate 35% of production to monument construction, with the remaining 65% supporting the population. High-reproduction groups direct all resources plus a 40-50% bonus toward population support.

The third phase models population dynamics. Deaths occur through natural mortality, conflict casualties, and starvation when resources fall below population needs. Births are proportional to available resources after costs.

The fourth phase simulates territorial competition. Conflict probability depends on the strategies of interacting groups: when both groups are monument builders, conflict probability drops to 25% of baseline (75% reduction). Conflict outcomes depend on population size, monument investment, and stochastic elements. Winners gain contested cells while losers suffer 20-25% population mortality.

The fifth phase handles group extinction and territory inheritance. Groups whose population falls below one individual go extinct, with territory absorbed by neighbours proportional to shared border length.

### 3.5 Conflict resolution mechanism

The conflict mechanism warrants particular emphasis as it elucidates how monuments function as costly signals. The model incorporates three key dynamics. First, a deterrence effect operates when two monument-building groups share a border: conflict probability drops by 75%, representing mutual recognition that both groups have signalled commitment and capacity. Second, mixed interactions between monument builders and high-reproduction groups proceed at baseline conflict rates. Third, population size confers an advantage in conflict outcomes, but frequent conflicts impose mortality costs that can negate demographic advantages.

### 3.6 Environmental parameters

For Rapa Nui, parameters are grounded in palaeoclimate reconstructions [61]: shortfall magnitude 0.6 (60% reduction, based on sediment cores showing 50-67% precipitation deficits during 1550-1700 CE), frequency 6 years (ENSO-driven drought clustering), and base productivity 0.8 (marginal conditions). For Rapa Iti, parameters reflect stable conditions: magnitude 0.3, frequency 18 years, and base productivity 1.2 (stable, productive conditions with 2,500 mm annual precipitation).

### 3.7 Simulation design

We systematically explored parameter space across shortfall frequency (5-20 years, 16 values) and magnitude (0.2-0.8, 13 values), yielding 208 scenarios with 10 replicates each. Sensitivity analysis comprised 5 complete phase-space explorations, yielding 10,400 total simulations.

## 4. Results

### 4.1 Quantitative validation of Price equation predictions

The modified Price equation predicts a diagonal boundary at critical threshold σ* separating signalling-favourable from reproduction-favourable regions. The observed ABM boundary runs diagonally from approximately (frequency=5, magnitude=0.45) to (frequency=20, magnitude=0.75), with mean absolute deviation less than 0.08 σ units across the parameter space. Theory predicts signalling dominance should increase monotonically with environmental uncertainty; ABM results confirm this with correlation r = 0.87 (p < 0.001) across 208 parameter combinations.

The case studies validate the framework. Rapa Nui parameters (frequency=6, magnitude=0.6) yield 92% monument-builder dominance. Rapa Iti parameters (frequency=18, magnitude=0.3) yield 87% high-reproduction dominance. Both outcomes match theoretical predictions.

Extended validation confirms theoretical predictions. Temporal simulations (1000 replicates over 200 years) demonstrate that Rapa Nui conditions produce a strong signalling advantage (final dominance +0.43, 95% CI [+0.41, +0.45]) while Rapa Iti conditions show near-neutral outcomes (final dominance +0.07, 95% CI [+0.06, +0.08]). The difference between conditions is statistically robust (Cohen's d = 1.35, p < 0.0001).

### 4.2 Regional patterns

The phase space divides into distinct regions. In the signalling-favourable region (upper-left of the phase space), frequent shortfalls (every 5-10 years) combined with high magnitude (0.5-0.8) creates strong selection for monument building, with dominance values reaching +0.75 as monument builders comprise 87% of final populations. In the reproduction-favourable region (lower-right), rare shortfalls (every 15-20 years) combined with low magnitude (0.2-0.4) strongly favours demographic maximisation, with dominance values reaching -0.75. The transition boundary runs diagonally, and shifts of just 2 years in shortfall interval or 0.1 in magnitude substantially alter outcomes.

### 4.3 Demographic paradox confirmed

The highest populations occur in reproduction-favourable regions (1400+ individuals), while signalling-favourable regions show substantially lower populations (1200-1300). Critically, monument builders dominate despite lower populations, empirically confirming the demographic paradox.

Controlled comparisons under moderate-high stress (frequency=8 years, magnitude=0.6) reveal striking patterns (electronic supplementary material). Monument construction reduces final population by 22% but reduces total mortality by 39%, resulting in fewer deaths overall. The per capita survival rate is higher among monument builders (0.75 deaths per capita versus 0.95). Monument builders effectively "buy" lower mortality through demographic constraint.

When both strategies compete directly, high-reproduction groups suffer 38 times higher per-capita mortality when competing against monument builders in stressful environments. They become caught in a demographic trap. During productive periods they boost population, but when shortfalls arrive they exceed carrying capacity and experience catastrophic mortality. Desperate for resources, they engage in territorial conflicts that impose further losses, ultimately approaching extinction. Monument builders avoid this trap by maintaining population below carrying capacity throughout the cycle.

### 4.4 Temporal dynamics

Under frequent stress (frequency=6, magnitude=0.6), monument builders maintain steady populations of approximately 600-700 with minimal fluctuations during shortfalls, gradually absorbing territories from extinct reproduction groups. High-reproduction groups exhibit boom-bust cycles with rapid growth followed by catastrophic crashes, ultimately approaching extinction because they cannot maintain population below carrying capacity. Under stable conditions (frequency=18, magnitude=0.3), the pattern reverses: monument builders decline from 600 to 300, unable to compete demographically, while high-reproduction groups grow steadily to 1,200 and translate demographic dominance into territorial expansion.

### 4.5 Case study validation

Simulations using empirically-derived parameters for Rapa Nui (frequency=6, magnitude=0.6) and Rapa Iti (frequency=18, magnitude=0.3) reproduce the archaeological contrast between these islands. Under Rapa Nui conditions, monument builders account for 92% of population by year 200, control 93% of territory, and record only 287 total conflicts. The simulation reproduces archaeological patterns: extensive monuments, moderate population (approximately 3,000), increased construction during drought, and territorial organisation around monument complexes. Under Rapa Iti conditions, high-reproduction groups account for 87% of population with 912 total conflicts, matching archaeological observations of limited monumentality, emphasis on fortifications (14 hilltop fortifications documented [62]), and higher sustainable population density. Rapa Nui simulations show 20% lower final population, 68% fewer conflicts, and conflict rate of 1.4 per year compared with 4.6 per year for Rapa Iti.

### 4.6 Robustness

Sensitivity analysis across 10,400 simulations confirms that core patterns are robust. Strategy switches occur in approximately 34% of parameter points, but this variability concentrates near the transition boundary where strategies have similar fitness. The diagonal boundary orientation and position remain consistent across all runs, with mean standard deviation in dominance values of 0.10.

## 5. Discussion

### 5.1 The demographic paradox resolved

Our central finding challenges conventional demographic reasoning: costly signalling can be adaptive precisely because it produces smaller populations. In environments characterised by frequent, severe resource shortfalls, monument-building groups dominate competitively despite 20-40% lower equilibrium populations.

This paradox resolves through three interconnected mechanisms operating simultaneously. First, monument builders maintain populations below carrying capacity through conservative life history strategies that channel resources into fewer, better-supported offspring rather than maximising fertility. This K-selected approach avoids density-dependent mortality. During shortfalls, monument-building groups experience moderate mortality but avoid catastrophic density-dependent crashes. Second, when monument builders interact, mutual signalling creates 75% conflict reduction through deterrence. This effect compounds over time because high-reproduction groups engage in frequent territorial conflicts at rates three to four times higher, with cumulative conflict mortality exceeding 40% of total deaths. Third, monument builders maintain stable territories that allow sustained long-term productive capacity.

### 5.2 Theoretical synthesis

Our model synthesises three previously competing frameworks.

Dunnell [34,63] proposed that "waste," energy expenditure diverted from reproduction that cannot be recovered, is adaptive in marginal and unpredictable environments. His argument was that waste creates a buffer between population size and carrying capacity. Neiman [64] criticised Dunnell's waste concept as "naive group selection" and proposed an alternative framework based on costly signalling theory. Madsen et al. [65] reframed waste as variance-reducing bet-hedging.

Carleton et al. [66] recently tested Dunnell's hypothesis using agent-based modelling and quantitative genetic methods. Their results were unambiguous: pure waste without functional benefits was subject to strong negative selection regardless of environmental variability. This finding is critical because it demonstrates that waste alone cannot explain monument building. For costly behaviours to be adaptive, they must provide functional benefits that offset their energetic costs.

Our model demonstrates that these frameworks can be productively synthesised. Monument building operates as waste in Dunnell's sense (diverting 35% of resources), as costly signalling in Neiman's sense (reducing conflict by 75%), and as bet-hedging (reducing variance through lowered reproductive output). The 75% conflict reduction represents the functional benefit rendering monument building adaptive. The phase-space structure demonstrates precisely when this modified waste hypothesis succeeds.

### 5.3 Archaeological implications

The model provides a novel interpretation of monument construction as adaptive insurance against resource uncertainty, rather than surplus disposal, elite competition, or maladaptive excess.

Several lines of evidence support this interpretation. Monument construction intensifies during drought periods [16], precisely when the model predicts signalling investment should increase. Monuments cluster near critical freshwater resources [16], consistent with signalling territorial control over vital assets. Monument builders sustain moderate populations rather than maximising demographic growth, as the model predicts. The timing of when moai construction ceased remains uncertain, presenting an important test of the model's predictions. Radiocarbon dates from the Rano Raraku quarry extend into the post-European contact period [67], though whether these represent active carving is unclear. Europeans arriving in 1722 observed moai standing on ahu platforms but did not witness statue transport. If monument construction did decline as environmental conditions stabilised following the Little Ice Age drought, this would be consistent with an adaptive response to reduced resource stress. However, this hypothesis requires further chronological investigation to test. Finally, Rapa Nui lacks evidence of intensive fortification, unlike Rapa Iti [62]. This contrast aligns with the model's prediction that signalling-dominated environments experience low conflict rates, reducing the need for defensive structures.

The model predicts three distinct adaptive regimes across Pacific islands: (1) frequent, severe stress favours intensive costly signalling through monuments; (2) stable but competitive environments favour defensive fortifications; (3) stable, abundant resources require neither. This pattern extends beyond Polynesia. Gobekli Tepe emerged during climate instability and ceased as the Holocene climate stabilised. The Hopewell earthworks appeared in variable river valley environments. Malta's temples were built on drought-vulnerable islands.

### 5.4 Theoretical contributions

This study makes three primary contributions. First, we extended the Price equation to incorporate environmental uncertainty as an explicit parameter, transforming it from a retrospective accounting tool into a predictive framework. Second, the model extends costly signalling theory by demonstrating that environmental parameters determine whether costly signalling is adaptive. Signalling is not universally beneficial; it occupies a specific region of environmental phase space. Third, the model provides a formal framework for cultural group selection under environmental uncertainty, addressing when group-beneficial traits can persist despite individual costs.

## 6. Conclusion

We began with a puzzle that has occupied archaeologists for generations: why do societies invest in monumental architecture when those resources could support larger populations? Our approach extended the Price equation for multilevel selection to incorporate environmental uncertainty, yielding critical threshold σ*. We validated this using an agent-based model spanning 10,400 simulations.

The model resolves the demographic paradox by showing that lower population is not a cost but the mechanism through which costly signalling achieves competitive advantage. Monument builders maintain populations below carrying capacity, thereby avoiding catastrophic crashes during shortfalls. They reduce conflict through mutual deterrence and maintain stable territories that sustain long-term productivity.

Applied to Polynesian case studies, the framework correctly predicts divergent trajectories. Rapa Nui's environmental parameters place it in the signalling-favourable region, consistent with its extensive monument tradition. Rapa Iti's stable climate places it in the reproduction-favourable region, consistent with its emphasis on fortifications.

Monument building should be interpreted not as surplus disposal, elite competition, or maladaptive excess, but as adaptive insurance against environmental uncertainty. The demographic paradox is resolved: a lower population is the mechanism by which costly signalling achieves competitive advantage when frequent resource stress renders conflict reduction more valuable than demographic growth. The nearly 1,000 moai of Rapa Nui stand not as monuments to ecological folly but as evidence of a successful adaptive strategy that enabled persistence through centuries of environmental challenge.

## Ethics

This work did not require ethical approval as it involved computational modelling and analysis of published archaeological data only.

## Data accessibility

All model source code, simulation data, analysis scripts, and figures are available at [Repository URL]. The data are provided in electronic supplementary material [68].

## Declaration of AI use

We have not used AI-assisted technologies in creating this article.

## Authors' contributions

[Author initials]: conceptualisation, formal analysis, investigation, methodology, software, visualisation, writing (original draft, review and editing). [Author initials]: conceptualisation, funding acquisition, methodology, supervision, writing (review and editing).

## Conflict of interest declaration

We declare we have no competing interests.

## Funding

[Funding details to be added]

## References

1. Quinn CP. 2019 Costly signaling theory in archaeology. In *Handbook of evolutionary research in archaeology* (ed AM Prentiss), pp. 73-93. Cham: Springer.
2. Trigger BG. 2003 *Understanding early civilizations: a comparative study*. Cambridge: Cambridge University Press.
3. Dietrich O, Notroff J, Dietrich L. 2018 Masks and masquerade in the Early Neolithic: a view from Upper Mesopotamia. *Time Mind* **11**, 3-21.
4. Schmidt K. 2010 Gobekli Tepe: the Stone Age sanctuaries. *Doc. Praehist.* **37**, 239-256.
5. Parker Pearson M. 2012 *Stonehenge: exploring the greatest Stone Age mystery*. London: Simon & Schuster.
6. Carr C, Case DT (eds). 2005 *Gathering Hopewell: society, ritual, and ritual interaction*. New York: Springer.
7. Lynott MJ. 2014 *Hopewell ceremonial landscapes of Ohio*. Oxford: Oxbow Books.
8. Kidder TR et al. 2009 Poverty Point Mound A: final report of the 2005 and 2006 field seasons. Baton Rouge: Louisiana Division of Archaeology.
9. Malone C. 2007 Ritual spaces and structure at the Maltese temple sites. In *Handbook of archaeological theories* (eds RA Bentley, HDG Maschner, C Chippindale). Lanham: AltaMira Press.
10. Hunt TL, Lipo CP. 2011 *The statues that walked: unraveling the mystery of Easter Island*. New York: Free Press.
11. Lipo CP, DiNapoli RJ, Hunt TL. 2022 Claims and evidence in the population history of Rapa Nui (Easter Island). In *The prehistory of Rapa Nui (Easter Island)* (eds B Vogt, A Kuhlem, A Mieth, H-R Bork), pp. 511-540. Cham: Springer.
12. Lipo CP, Hunt TL. 2025 The walking moai hypothesis. *J. Archaeol. Sci.* **183**, 106383. (doi:10.1016/j.jas.2025.106383)
13. Parker Pearson M et al. 2019 Megalith quarries for Stonehenge's bluestones. *Antiquity* **93**, 45-62.
14. Childe VG. 1950 The urban revolution. *Town Plan. Rev.* **21**, 3-17.
15. Dietrich O, Heun M, Notroff J, Schmidt K, Zarnkow M. 2012 The role of cult and feasting in the emergence of Neolithic communities. *Antiquity* **86**, 674-695.
16. DiNapoli RJ, Lipo CP, Brosnan T, Hunt TL, Hixon S, Morrison AE, Becker M. 2019 Rapa Nui (Easter Island) monument (ahu) locations explained by freshwater sources. *PLOS ONE* **14**, e0210409.
17. Hayden B. 1995 Pathways to power: principles for creating socioeconomic inequalities. In *Foundations of social inequality* (eds TD Price, GM Feinman), pp. 15-86. New York: Plenum.
18. Hayden B. 2001 Fabulous feasts: a prolegomenon to the importance of feasting. In *Feasts* (eds M Dietler, B Hayden), pp. 23-64. Washington, DC: Smithsonian Institution Press.
19. Carr C. 2006 Rethinking interregional Hopewellian "interaction." In *Gathering Hopewell* (eds C Carr, DT Case), pp. 575-623. New York: Springer.
20. Renfrew C. 1973 Monuments, mobilization and social organization in Neolithic Wessex. In *The explanation of culture change* (ed C Renfrew), pp. 539-558. London: Duckworth.
21. Dancey WS, Pacheco PJ (eds). 1997 *Ohio Hopewell community organization*. Kent, OH: Kent State University Press.
22. Boersema JJ, Huele R. 2019 Pondering the population numbers of Easter Island's past. In *Easter Island and the Pacific* (eds B Vogt, A Kuhlem, A Mieth, H-R Bork), pp. 83-92. Rapa Nui Press.
23. Ioannidis AG et al. 2021 Paths and timings of the peopling of Polynesia inferred from genomic networks. *Nature* **597**, 522-526.
24. DeMarrais E, Castillo LJ, Earle T. 1996 Ideology, materialization, and power strategies. *Curr. Anthropol.* **37**, 15-31.
25. Stein R et al. 2025 Prolonged drought on Rapa Nui during the decline of megalithic monument construction. *Commun. Earth Environ.* **6**, 865.
26. Banning EB. 2011 So fair a house: Gobekli Tepe and the identification of temples in the Pre-Pottery Neolithic of the Near East. *Curr. Anthropol.* **52**, 619-660.
27. Bar-Yosef O, Belfer-Cohen A. 1989 The origins of sedentism and farming communities in the Levant. *J. World Prehist.* **3**, 447-498.
28. Kuijt I, Finlayson B. 2009 Evidence for food storage and predomestication granaries 11,000 years ago in the Jordan Valley. *Proc. Natl Acad. Sci. USA* **106**, 10966-10970.
29. Sherratt A. 1997 *Economy and society in prehistoric Europe*. Princeton: Princeton University Press.
30. Whittle A. 1996 *Europe in the Neolithic*. Cambridge: Cambridge University Press.
31. Bradley R. 1998 *The significance of monuments*. London: Routledge.
32. DiNapoli RJ, Morrison AE, Lipo CP, Hunt TL, Lane BG. 2017 East Polynesian islands as models of cultural divergence. *J. Isl. Coast. Archaeol.* **13**, 1-18.
33. Anderson A, Kennett DJ. 2012 Taking the high ground: the archaeology of Rapa. In *Taking the high ground* (eds A Anderson, DJ Kennett). Canberra: ANU E Press.
34. Dunnell RC. 1989 Aspects of the application of evolutionary theory in archaeology. In *Archaeological thought in America* (ed CC Lamberg-Karlovsky), pp. 35-49. Cambridge: Cambridge University Press.
35. Zahavi A. 1975 Mate selection: a selection for a handicap. *J. Theor. Biol.* **53**, 205-214.
36. Grafen A. 1990 Biological signals as handicaps. *J. Theor. Biol.* **144**, 517-546.
37. Winterhalder B, Lu F, Tucker B. 1999 Risk-sensitive adaptive tactics. *J. Archaeol. Res.* **7**, 301-348.
38. Glatz C, Plourde AM. 2011 Landscape monuments and political competition in Late Bronze Age Anatolia. *Bull. Am. Sch. Orient. Res.* **361**, 33-66.
39. Kolb MJ. 1994 Monumentality and the rise of religious authority in precontact Hawai'i. *Curr. Anthropol.* **35**, 521-547.
40. Bliege Bird R, Codding BF, Kauhanen PG, Bird DW. 2012 Aboriginal hunting buffers climate-driven fire-size variability in Australia's spinifex grasslands. *Proc. Natl Acad. Sci. USA* **109**, 10287-10292.
41. Sosis R, Bressler ER. 2003 Cooperation and commune longevity: a test of the costly signaling theory of religion. *Cross-Cult. Res.* **37**, 211-239.
42. Lipo CP, DiNapoli RJ, Hunt TL. 2022 Population structure. In *The prehistory of Rapa Nui (Easter Island)* (eds B Vogt, A Kuhlem, A Mieth, H-R Bork), pp. 511-540. Cham: Springer.
43. Halstead P, O'Shea J. 1989 Introduction: cultural responses to risk and uncertainty. In *Bad year economics* (eds P Halstead, J O'Shea), pp. 1-7. Cambridge: Cambridge University Press.
44. Price GR. 1970 Selection and covariance. *Nature* **227**, 520-521.
45. Price GR. 1972 Extension of covariance selection mathematics. *Ann. Hum. Genet.* **35**, 485-490.
46. Grafen A. 2000 Developments of the Price equation and natural selection under uncertainty. *Proc. R. Soc. B* **267**, 1223-1227.
47. Rice SH. 2008 A stochastic version of the Price equation. *BMC Evol. Biol.* **8**, 262.
48. Frank SA. 2012 Natural selection. IV. The Price equation. *J. Evol. Biol.* **25**, 1002-1019.
49. Lipo CP, Hunt TL, Haoa SR. 2013 The 'walking' megalithic statues (moai) of Easter Island. *J. Archaeol. Sci.* **40**, 2859-2866.
50. Abrams EM. 1994 *How the Maya built their world*. Austin: University of Texas Press.
51. Erasmus CJ. 1965 Monument building: some field experiments. *Southwest. J. Anthropol.* **21**, 277-301.
52. Rappaport RA. 1968 *Pigs for the ancestors*. New Haven: Yale University Press.
53. Wiessner P. 1982 Risk, reciprocity and social influences on !Kung San economics. In *Politics and history in band societies* (eds E Leacock, R Lee), pp. 61-84. Cambridge: Cambridge University Press.
54. Cashdan E. 1985 Coping with risk: reciprocity among the Basarwa of northern Botswana. *Man* **20**, 454-474.
55. Bowles S. 2009 Did warfare among ancestral hunter-gatherers affect the evolution of human social behaviors? *Science* **324**, 1293-1298.
56. Keeley LH. 1996 *War before civilization*. New York: Oxford University Press.
57. Wiessner P. 2006 From spears to M-16s: testing the imbalance of power hypothesis among the Enga. *J. Anthropol. Res.* **62**, 165-191.
58. Lake MW. 2014 Trends in archaeological simulation. *J. Archaeol. Method Theory* **21**, 258-287.
59. Axtell RL et al. 2002 Population growth and collapse in a multiagent model of the Kayenta Anasazi. *Proc. Natl Acad. Sci. USA* **99**, 7275-7279.
60. Crabtree SA, Bocinsky RK, Hooper PL, Ryan SC, Kohler TA. 2017 How to make a polity (in the central Mesa Verde region). *Am. Antiq.* **82**, 71-95.
61. Roman M et al. 2021 A multi-decadal geochemical record from Rano Aroi (Easter Island/Rapa Nui): implications for the environment, climate and humans during the last two millennia. *Quat. Sci. Rev.* **268**, 107115.
62. Kennett DJ, McClure SB. 2012 The archaeology of Rapan fortifications. In *Taking the high ground* (eds A Anderson, DJ Kennett), pp. 203-234. Canberra: ANU E Press.
63. Dunnell RC, Greenlee DM. 1999 Late Woodland period "waste" in the Ohio River Valley. *J. Anthropol. Archaeol.* **18**, 376-395.
64. Neiman FD. 1998 Conspicuous consumption as wasteful advertising. In *Rediscovering Darwin* (eds CM Barton, GA Clark), pp. 267-290. Arlington: American Anthropological Association.
65. Madsen ME, Lipo CP, Cannon MD. 1999 Fitness and reproductive trade-offs in uncertain environments. SAA Monographs.
66. Carleton WC, McCauley B, Costopoulos A, Collard M. 2019 Agent-based model experiments cast doubt on Dunnell's adaptive waste explanation for cultural elaboration. *STAR* **5**, 1-18.
67. Sherwood S, Van Tilburg J, Barrier CR, Horrocks M, Dunn RK, Huebert J, Ramírez-Aliaga JM. 2019 New excavations in Easter Island's statue quarry: soil fertility, site formation and chronology. *J. Archaeol. Sci.* **111**, 104994. (doi:10.1016/j.jas.2019.104994)
68. [Authors]. 2025 Data from: The paradox of monumental architecture. Dryad Digital Repository.

---

## Figure Legends

**Figure 1.** Pacific overview map showing the locations of Rapa Nui (Easter Island) and Rapa Iti in the Pacific Ocean, providing geographic context for the case study comparison. Despite shared Polynesian ancestry, these islands developed dramatically different cultural trajectories.

**Figure 2.** The Price equation for multilevel selection. (*a*) The equation partitions evolutionary change into between-group selection (covariance between group fitness and trait frequency) and within-group selection (expected change within groups). (*b*) Between-group selection operates through differential survival during shortfalls, whereby groups with more monument builders (MB) survive, whereas groups dominated by high-reproduction (HR) strategies go extinct. (*c*) Within-group selection opposes costly signalling because high-reproduction individuals out-reproduce monument builders within any group. (*d*) The central question: under what environmental conditions does between-group selection become strong enough to overcome within-group costs?

**Figure 3.** Shortfall frequency comparison showing population dynamics and resource availability under frequent (6-year cycle, left panels) versus rare (18-year cycle, right panels) shortfall regimes, holding magnitude constant.

**Figure 4.** Shortfall magnitude comparison showing population dynamics under mild (30% reduction, left panels) versus severe (60% reduction, right panels) shortfall regimes, holding frequency constant.

**Figure 5.** Combined shortfall scenarios showing population dynamics across the environmental parameter space. The diagonal pattern emerges clearly: monument building dominates under frequent-severe conditions, while high reproduction dominates under rare-mild conditions.

**Figure 6.** Modified Price equation framework and predictions. (*a*) Expected fitness under environmental uncertainty for signalling (blue) and non-signalling (orange) strategies, showing crossover at the critical threshold σ*. (*b*) Decomposition of Price equation components. (*c*) Predicted phase space with theoretical boundary. (*d*) Framework summary.

**Figure 7.** Model dynamics overview. (*a*) Annual simulation cycle. (*b*) Conflict probability matrix showing 75% reduction for monument builder pairs. (*c*) Resource allocation comparison. (*d*) Conflict outcome determinants.

**Figure 8.** Environmental phase space structure. (*a*) Strategy dominance across environmental parameter space from 10,400 simulations. (*b*) Total equilibrium population. The diagonal boundary separates signalling-favourable (orange, upper left) from reproduction-favourable (purple, lower right) regions. Cyan circle marks Rapa Nui; yellow square marks Rapa Iti.

**Figure 9.** Validation of modified Price equation predictions against agent-based model results. (*a*) Theoretical prediction. (*b*) Emergent phase space from simulations. (*c*) Selection component decomposition. (*d*) Theory versus simulation comparison (r = 0.969). (*e*) Temporal dynamics (1000 replicates). (*f*) Parameter sensitivity analysis.

**Figure 10.** Temporal dynamics by environmental condition. Top panels: frequent stress environment (frequency=6, magnitude=0.6). Bottom panels: stable environment (frequency=18, magnitude=0.3). Left panels show population by strategy (blue = monument builders, red = high reproduction); right panels show cumulative conflicts.

**Figure 11.** Rapa Nui vs. Rapa Iti case study comparison. Top row: Rapa Nui simulation (frequent severe drought). Bottom row: Rapa Iti simulation (stable conditions). Left panels show territory maps at year 200 (orange = monument builders; purple = high reproduction). Centre panels show population time series. Right panels show cumulative conflicts.
