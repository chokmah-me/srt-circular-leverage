<p class="hebrew-epigraph" dir="rtl" lang="he">אִם יִרְצֶה הַשֵּׁם</p>

# Circular Leverage in Bank-NBFI Synthetic Risk Transfer Networks

**Daniyel Yaacov Bilar**, Chokmah LLC, chokmah-dyb@pm.me ORCID: [0000-0002-9040-6914](https://orcid.org/0000-0002-9040-6914)
v2.1: [PENDING, November 2026] (v2: 17 August 2026; v1: 17 April 2026)  


---

## Abstract

Synthetic Risk Transfers (SRTs) let banks shed credit risk to non-bank financial intermediaries (NBFIs) while keeping the underlying loans on their balance sheets. A structural vulnerability arises when the same banks extend credit lines to the funds that buy their SRT protection, creating a circular leverage loop in which the capital relief is partly self-funded. We formalize this loop as a single parameter, λ, the fraction of total SRT protection weight financed by the originating bank or its affiliates. Using a directed network model of bank-NBFI SRT relationships, we simulate contagion cascades across 1,000 random network realizations for each λ value. The simulation shows a two-stage phase transition: cascade size first departs meaningfully from its baseline at $λ_{onset}$ ≈ 0.85–0.95 (the exact position depends on network density), then jumps sharply at λ* ≈ 0.95 where Dragon King events emerge from the loop mechanism itself. The transition *location* is invariant across network density, investor concentration, shock size, and tranche thickness; what density controls is cascade *magnitude* at high λ, which scales from 0.18 to 0.61 across the tested range. Since v1 (April 2026), three independent lines of evidence have partially substantiated the circular leverage channel: transaction-level ECB data show banks are 57 to 66% more likely to sell SRTs to investors they also finance, with an estimated 26% of SRT funding traceable to bank credit (Osberghaus and Schepens, 2026); the FSB's May 2026 private credit report documents bank credit lines to private credit funds at the same loop the BIS discusses as “circles of risk”; and the ECB has launched a dedicated survey of SRT financing practices. We propose six publicly observable proxy metrics ranked by sensitivity-weighted ordinal position relative to λ*. As of Q3 2026, three of six read red, one amber and one green; the CDS index reading awaits ISDA's Q3 data. BDC price dispersion eased from its Q1 extreme, and index CDS activity fell back after a record Q1. SOFR-OIS remains green, consistent with its predicted role as a lagging indicator. v2.1 pins numeric status rules for the dispersion and CDS metrics, which restate both Q2 readings from red to amber. One number, λ, would let supervisors place banks on the phase diagram. It is already known to each originating bank and is not reported. Simulation code is released under MIT license.

**Keywords:** synthetic risk transfer, circular leverage, network contagion, phase transition, Dragon King, LPPLS, private credit, systemic risk

---

## Audience-Targeted Summaries

*Five framings of the same result for different readers. Readers familiar with one framing can skip to §1.*

**For the expert (financial economist or regulator).** This paper formalizes circular leverage in bank-NBFI Synthetic Risk Transfer networks through parameter λ (self-funding fraction). Using network contagion simulations across 1,000 Monte Carlo runs, it identifies a two-stage transition: first departure from baseline at $λ_{onset}$ ≈ 0.85–0.95, then a sharp jump at λ* ≈ 0.95 where Dragon King events emerge, cascades that cannot be diversified away because correlation is endogenous to the funding loop. The transition location is invariant across network density, concentration, and shock parameters; only cascade magnitude scales with density (0.18 to 0.61 across the tested range). This v2 revision incorporates the first transaction-level academic study of SRTs (Osberghaus and Schepens, 2026, using ECB AnaCredit data), which estimates aggregate self-funding at roughly 26% and documents two additional channels (monitoring degradation and strategic loan selection) not modeled here. As of Q3 2026, three of six read red, one amber, one green, and one pending. Critical policy implication: disclosure of λ would enable macroprudential supervision at a stable threshold.

**For the practitioner (risk manager or bank executive).** Your bank extends credit lines to funds that buy your SRT protection, creating a hidden feedback loop. When stress hits, calling those credit lines can force fund failures, wiping out your capital relief and triggering further contractions. The danger zone starts around λ = 0.85–0.95, where λ is self-funded protection divided by total protection. Below that zone the system absorbs shocks; above it, cascades become self-reinforcing. The paper gives you six market signals to watch (BDC prices, PIK ratios, CLO spreads, among others) that fire before traditional funding stress indicators like SOFR-OIS. As of Q3 2026, three of six read red, one amber, one green, and one awaits data. Redemption requests at the largest funds are past their peak, but gates still bind and queues persist. Banks have started tightening leverage lines to private credit funds and limiting how much AI-linked debt they will underwrite. A new CDS index (FINDX) exists but has traded thinly so far. You cannot measure your own λ without disclosure, but you can watch the cockpit.

**For the general public.** Banks have found a way to make loans appear less risky on paper without actually reducing the risk. They sell "insurance" on their loans to investment funds, but often lend money to those same funds to buy the insurance. It is like insuring your house against fire and then lending the down payment to the insurance company. If there is a fire, you are partly paying yourself. Researchers found that this arrangement stays stable up to a critical point around 95% self-funding, then suddenly becomes fragile. Since this paper was first published, European regulators have confirmed the pattern exists using actual transaction data: banks really do lend to the same funds that buy their insurance, and roughly a quarter of the insurance money traces back to the bank's own credit. As of Q3 2026, three warning signs read red, one amber, one green, and one pending, but regulators still cannot see the key number that would tell them how close we are to danger.

**For the skeptic.** Since v1, the central parameter λ has moved from unobservable to partially estimated: Osberghaus and Schepens (2026) place aggregate self-funding at roughly 26%, well below the simulation's critical zone. That 26% is a market-wide average; per-bank tail values remain unknown. The six proxy metrics still rely on judgment-assigned sensitivity weights, not statistical estimation. The LPPLS framework remains conceptual vocabulary, not empirical prediction. Network topology is still stylized, though AnaCredit data could in principle calibrate a more realistic graph. No central bank intervention is modeled, though the ECB has now launched a survey that partially addresses the disclosure gap. The 0.95 threshold's stability across parameters is a property of the simulated random graph; real-world heterogeneity could shift it. The cockpit's Q1 signals were post-hoc observations; their worsening through Q2/Q3 provides partial out-of-sample tracking but does not constitute prediction. These are legitimate limitations the authors flag directly in §8.

**For the decision-maker (policymaker or regulator).** You need one number: λ, the fraction of SRT protection financed by the originating bank's own credit. It is already sitting in bank risk systems but is not reported. Disclosure would let you place institutions on a phase diagram with a stable critical zone at 0.85–0.95. The paper proposes a conservative supervisory limit of λ ≤ 0.30, far below the danger zone, with margin for error. Without disclosure, you must rely on six public market metrics (Table 2), three red, one amber, one green, one pending as of Q3 2026. The ECB has launched a survey of SRT financing practices (March 2026) and the FSB has issued a dedicated private credit vulnerabilities report (May 2026), but neither constitutes the standing Pillar 3 disclosure this paper recommends. The traditional interbank funding indicator (SOFR-OIS) ranks last; the upstream signals fire earlier. The policy ask is minimal: one Pillar 3 disclosure item, not new capital requirements or bans.

---

## 1. Introduction

Banks and their regulators have been playing a version of the same game since Basel I: regulators assign risk weights to assets, banks find instruments that reduce those weights without reducing the underlying risk. Synthetic Risk Transfers are the current iteration. A bank keeps a pool of corporate loans on its balance sheet, structures a credit protection agreement with a non-bank fund, and tells its regulator that the risk has moved. In many cases it has. In some cases it has not, and it has just become harder to see.

The mechanism that makes the transfer illusory is circular leverage. Section 2 describes it in detail. The short version: banks routinely extend prime brokerage credit to the same funds that buy their SRT protection. Under stress, that shared funding source turns the protection seller into an extension of the bank's own balance sheet. The insured and the insurer share a funding source.

At the time of v1 (April 2026), neither the BIS (2026) nor the IMF (2025) had been able to measure how common this loop is. Since then, three developments have partially closed that gap. First, Osberghaus and Schepens (2026) published the first academic study of SRT markets using transaction-level data from the ECB's AnaCredit credit registry, finding that banks are 57 to 66% more likely to sell SRTs to investors they also finance and that roughly 26% of SRT funding may trace back to bank credit. Second, the FSB issued a dedicated report on private credit vulnerabilities (May 2026) that documents bank credit lines to private credit funds, and the BIS (2026) discusses the same loop as “circles of risk” (citing ESRB 2025). Third, the ECB launched a survey of SRT financing practices (March 2026), specifically probing which banks provide funding to SRT buyers. These developments partially validate the circular leverage channel without resolving the disclosure problem: λ remains unreported at the individual bank level. This paper formalizes the loop, shows that its consequences are nonlinear, and provides a set of public signals that track the system's proximity to a phase transition without requiring access to the undisclosed data.

The paper makes four contributions, with a fifth added in v2. First, we define λ, the self-funding fraction, as the key parameter governing cascade risk in an SRT network, and show via simulation that cascade size is discontinuous in λ, not smooth. Second, we show that the transition *location* is invariant across all structural parameters we tested (network density, investor concentration, shock size, tranche thickness): what density controls is cascade *magnitude* at high λ, not where the cliff sits. The 95% threshold is therefore a stable target for supervision. Third, we use Sornette's Dragon King theory to characterize the regime above λ* as qualitatively different from ordinary tail risk: diversification cannot protect against it because the correlation is endogenous to the loop. Fourth, we build a cockpit of six publicly observable metrics, ranked by sensitivity-weighted ordinal position relative to λ*, and report their readings. As of Q3 2026 they read three red, one amber, one green, and one pending. Fifth (new in v2), we connect the simulation's theoretical channel to the first empirical evidence from Osberghaus and Schepens (2026), who document both the interconnectedness our model assumes and two additional channels (monitoring degradation and strategic loan selection) that our model does not capture (Section 2.4).

One thing this paper does not do: we do not formally fit LPPLS parameters to SRT issuance time series or predict a critical time. The LPPLS framework appears here as a conceptual vocabulary for super-exponential growth, not as an empirical result. We state this clearly wherever the framework is invoked.

---

## 2. The Circular Leverage Loop

### 2.1 How an SRT works

A bank holds a reference portfolio of, say, $1 billion in leveraged corporate loans. It cannot sell them without damaging its client relationships, and it does not want to hold capital against the full risk-weighted amount. So it structures a synthetic securitization. The portfolio's credit risk is sliced into tranches: a senior piece (typically 80% or more of the notional) that the bank retains, a mezzanine piece (the next 7-10%), and a first-loss piece (the bottom 5-8%). The bank finds a buyer for the mezzanine and first-loss tranches, usually a private credit fund, hedge fund, or insurer. The buyer either deposits cash into a segregated account (funded structure) or signs a guarantee (unfunded). The bank pays the buyer a premium (often 8-11% annually in the current environment) and in exchange receives regulatory recognition that the covered portion of the portfolio can be assigned a lower risk weight. Capital is freed; lending capacity grows; the cycle repeats.

Nothing about this structure is inherently problematic. The risk has genuinely moved if the fund is independently capitalized and uncorrelated with the bank's own distress. The BIS (2026) estimates that by end-2024 almost €800 billion of loans were covered by such instruments globally, a fivefold increase since 2016. North American issuance has risen more recently, after the Federal Reserve recognized Credit-Linked Notes as a valid capital relief tool.

### 2.2 Where the loop enters

Banks extend credit to investment funds as a normal part of prime brokerage. A private credit fund with $500 million under management might carry $200-300 million in repo financing from one or more bank counterparties, using its loan book as collateral. This is standard practice and usually benign.

The problem is when a fund uses that repo financing to buy SRT protection from the same bank providing the repo. Now the capital relief the bank receives is partly backed by its own credit. Define λ as the fraction of a fund's SRT position funded by credit from the originating bank or its affiliates:

$$\lambda = \frac{\text{protection funded by originating bank credit}}{\text{total protection notional}}$$

At λ = 0, the fund is independently financed and the transfer is genuine. At λ = 1, the bank is effectively insuring itself through a fund-shaped intermediary. Real transactions sit somewhere in between. The BIS (2026) and IMF (2025) both identify this loop but note they cannot measure it because λ is not a required disclosure item anywhere in the Basel framework.

### 2.3 The failure chain

Under stress the mechanics are straightforward. A sector-wide shock (software loan impairments from AI disruption, say, or a sudden energy price reversal) causes losses in the reference portfolio that exceed the first-loss tranche thickness δ. The CLN triggers. The fund must pay the bank from its collateral account. If the fund is repo-financed by the originating bank, the bank is simultaneously receiving a protection payment and extending new credit to fund it. When the fund's collateral is exhausted, it defaults on the protection. The bank's RWA relief evaporates. If enough protection fails at once, the bank's capital ratio falls below regulatory minimums, forcing it to call in other credit lines, contract lending, or raise equity. Each contraction makes the situation worse for other funds with correlated positions.

The loop does not require fraud or misrepresentation. It can emerge entirely from normal prime brokerage relationships. A bank's credit committee and its SRT desk may not communicate about shared counterparty exposure. The BIS (2026) identifies six distinct risk transfer chains involving SRTs, including one in which credit risk transferred from banks to funds via SRTs returns to the banking sector through other banks financing those funds ("circles of risk," borrowing the ESRB's terminology). The BIS characterizes the scale of these loops as "modest" based on anecdotal evidence, while noting that limited and fragmented information "heightens the potential for SRT-related risks to build up undetected." The BCBS (2026) separately notes that data on SRT financing is scarce and that supervisors are in the early stages of understanding banks' SRT financing activities.

### 2.4 Empirical evidence for the loop (new in v2)

Osberghaus and Schepens (2026) provide the first transaction-level evidence for the circular leverage channel, using the ECB's AnaCredit credit registry. Their data covers the European SRT market, where outstanding synthetically transferred corporate loans quintupled from roughly 60 billion euros at end-2018 to 300 billion euros at end-2024, surpassing traditional securitization for corporate loans. Thirty-five banks, many among the largest in the euro area, had more than 10% of their corporate loan portfolio synthetically transferred.

Three findings are directly relevant to this paper.

**Interconnectedness.** Banks are 57 to 66% more likely to sell an SRT to a non-bank investor with which they also have a credit relationship. The study also finds a slight increase in outstanding bank loan liabilities of SRT investors in the months before the SRT investment, consistent with partial debt financing of the SRT position. Their estimate implies that roughly 26% of SRT funding may trace back to bank credit. In the terms of our model, this places the aggregate market-wide lambda at approximately 0.26, well below the critical zone at 0.85 to 0.95. The study also reports a median junior tranche thickness of 15%, nearly double our default δ = 0.08. We re-ran the simulation at δ = 0.15; the phase transition is unchanged (Section 5.5.1, Figure 6).

That estimate is reassuring at the market-wide level but does not address the tail. Our phase transition concerns the per-bank lambda, not the market average. A bank at the 95th percentile of self-funding could sit at lambda above 0.85 even if the mean is 0.26. The AnaCredit data could in principle identify such outliers; the aggregate statistic alone cannot.

**Monitoring degradation.** After transferring a loan's credit risk via SRT, banks reduce the frequency with which they update internal probability-of-default estimates by 12–25% on average (Osberghaus and Schepens, 2026, p. 7; Table 9 reports 12–13% on the update-frequency measure and about 26% on the volatility of PD estimates). When a bank transfers its entire exposure to a firm, that reduction reaches 35% on the frequency measure and 70% on the PD-volatility measure. This is a channel our cascade model does not capture. In our simulation, reference portfolio quality is fixed at the time of the initial shock. The Osberghaus-Schepens finding implies that reference portfolio quality silently deteriorates after SRT issuance, which would increase the probability and severity of the initial shock over time. A v3 model extension could make shock probability s a function of time-since-SRT-issuance, calibrated to the documented monitoring reduction.

**Strategic loan selection.** Banks cherry-pick loans that are capital-expensive relative to their economic riskiness for inclusion in SRT portfolios. The study exploits the EU's "SME supporting factor," a regulatory provision that creates a discontinuity in risk weights at a 50 million euro revenue threshold, to identify this selection causally. The probability of a loan being synthetically transferred increases by up to 70% at this threshold. Banks then redeploy freed capital into new lending, leaving themselves effectively less capitalized after the SRT even though reported ratios are unchanged. This adverse selection mechanism amplifies the systemic risk of the circular leverage loop: the bank's retained portfolio is riskier per unit of capital than its pre-SRT portfolio, so the same external shock produces a larger capital shortfall.

The FSB's May 2026 report on private credit vulnerabilities (Financial Stability Board, 2026) independently validates the interconnectedness finding at a global scale. Across FSB members, official data capture about $220 billion of drawn and undrawn bank credit lines to private credit funds; commercial estimates run from about $270 billion to $500 billion. The BIS (2026) discusses the same loop as “circles of risk” (ESRB 2025): credit transferred out via an SRT can return if other banks finance the protection buyer.

### 2.5 Field evidence since v2 (new in v2.1)

Four developments between August and October 2026 bear on the loop.

**The call channel is live.** Banks have begun tightening back-leverage terms for private credit funds: higher cost, tighter covenants, and reported pauses on new lines (Troutman Pepper Locke, July 2026; Bloomberg, 12 March 2026). In our model this is the step where a distressed bank calls credit lines to funds. The trigger here was loan-value cuts tied to AI disruption, not SRT losses, so this shows the channel operates. It does not show that λ is high.

**Banks are also refusing to warehouse new AI risk.** In October 2026, JPMorgan and Goldman Sachs underwrote only $1.3 billion of a $5 billion loan package for Volta Infrastructure, an AI cloud company, leaving the $3.7 billion GPU-backed tranche to clear on a best-efforts basis at yields near 11% (Bloomberg, 12 October 2026). Apollo reportedly anchored the deal with a $1.5 billion order (Semafor, 13 October 2026). This is a second contraction mechanism, distinct from calling existing lines: banks pass the riskiest AI debt directly to non-bank lenders at origination. Whether those lenders fund the position with bank credit is exactly the quantity λ measures, and it is not disclosed.

**Redemption runs are past peak but queue rather than clear.** Q3 2026 requests eased at several flagship semi-liquid funds, yet gates kept binding (§6, Metric 1). A study of 136 tender-offer filings for ten non-traded BDCs finds requests rose from 1.2% to 6.9% of shares outstanding, with caps binding at seven of ten funds, and that gates defer redemption demand rather than remove it [Research Square, 2026; VERIFY authors]. A fund that cannot shed liabilities depends more on bank lines if its SRT positions draw.

**SRT is moving into concentrated pools, sometimes bought by insiders.** Banks with large AI data-centre exposure have approached investors about SRT structures that move the riskiest tranches off balance sheet while keeping a retained slice (Financial Times, May 2026 [VERIFY: cite FT directly]). TD Bank structured a data-centre SRT with a forward-flow feature that lets the reference pool grow over time (Bloomberg, 22 April 2026), and Deutsche Bank is working on one tied to about €2 billion of project finance debt including data centres (Bloomberg, 7 September 2026). Market participants report that data-centre SRTs price at 7% to 9%, tighter than the 8% to 12% range for broader infrastructure SRTs, and that the typical buyer already holds equity in the underlying assets (Octus, 2026). A protection seller that also owns the reference asset is a wrong-way exposure of the same family as λ: its ability to pay falls exactly when the protected loans fail.

---

## 3. Network Model

### 3.1 Construction

We model the SRT ecosystem as a directed graph G = (V, E) with two types of nodes and two types of edges.

**Nodes.** $V = V_B ∪ V_F$ where $V_B$ is a set of B bank nodes and $V_F$ is a set of F fund nodes. Default parameters are B = 10, F = 20, consistent with a mid-sized regional market rather than the full global network. Results hold across topology changes (Section 4.3).

**Edges.** Protection edges run from fund to bank $(f → b)$ with weight equal to the fraction of aggregate protection notional that fund f provides to bank b. Credit line edges run from bank to fund $(b → f)$ with weight equal to the notional of the credit facility. Each credit line edge carries a boolean attribute `self_funded`: True if the originating bank of the protection edge is also the provider of the credit line, False otherwise.

**Parameter λ.** We set λ by construction: protection edges are sorted by weight and flagged as self-funded until their cumulative weight reaches λ × (total protection weight). The realized λ differs slightly from the target due to discrete edge sizing; it is stored on each graph as λ_actual. Plots use the requested (target) λ on the x-axis.

**Investor concentration κ.** Motivated by the IMF (2025) finding that the top 10 investors hold over 75% of banks’ outstanding SRT exposure, we assign protection weights from a concentration-adjusted exponential distribution. The parameter κ controls what fraction of funds holds the bulk of exposure; default κ = 0.75.

The full network builder is implemented in `build_network()` in the accompanying code. Protection weights normalize to sum to 1.0 across the network; the total protection weight is thus interpretable as a fraction of aggregate bank RWA.

### 3.2 Cascade engine

**Initial shock.** At t = 0, a fraction s of total protection weight defaults, distributed across the most-exposed funds first (correlated shock hitting the largest positions). This is more realistic than random distribution for the kind of sector-wide repricing events (software loans, energy credits) that motivate the paper.

**Fund failure condition.** A fund fails when its cumulative loss exceeds its capital buffer, defined as protection_notional × δ where δ is the first-loss tranche thickness. Default δ = 0.08.

**Bank distress condition.** A bank becomes distressed when it loses more than 20% of its total SRT-derived RWA relief through fund failures. This threshold reflects the regulatory reality that a bank facing a large sudden jump in RWAs must either raise capital quickly or contract lending; 20% is a conservative estimate of the point at which that pressure becomes acute.

**Circular leverage channel.** When a bank becomes distressed, it calls in credit lines to self-funded funds (those where `self_funded = True`). A called fund must find replacement financing. If no alternative solvent bank credit line exists, the fund fails.

**Propagation.** We use sequential updating as the default: within each round, funds and banks are processed in random order, and failures are applied immediately. Simultaneous updating is available as an alternative mode for cross-validation (`mode='simultaneous'`). The two modes produce consistent results at the aggregate level; sequential is more realistic because real contagion is path-dependent.

The cascade runs until no new failures occur or a safety cap of $(B + F + 5)$ rounds is reached. In practice, cascades terminate in 2-4 rounds for most parameter combinations.

### 3.3 Key parameters

Table 1 summarizes the model parameters, defaults, and ranges tested.

| Parameter | Symbol | Default | Range |
|-----------|--------|---------|-------|
| Banks | B | 10 | 5–20 |
| Funds | F | 20 | 10–50 |
| Self-funding fraction | λ | sweep | 0.0–1.0 |
| Tranche thickness | δ | 0.08 | 0.04–0.15 |
| Shock size | s | 0.05 | 0.01–0.20 |
| Investor concentration | κ | 0.75 | 0.40–0.98 |
| Network density (bank connections per fund) | d | 2.0 | 1.0–5.0 |
| Monte Carlo runs | — | 1,000 | — |

*Table 1. Model parameters. Density is an expected value; per-fund connections are drawn from a clamped Poisson centered on d.*

---

## 4. LPPLS and Dragon King Framing

*Note on scope: We use the LPPLS model in this section as a conceptual and motivating framework, not as a formal empirical test. The growth trajectory of global SRT issuance (roughly 5x between 2016 and 2024 per BIS (2026); European outstanding stock quintupling from 60 billion to 300 billion euros over 2018 to 2024 per Osberghaus and Schepens (2026); global private credit now estimated at $1.5 to 2.0 trillion by the FSB (2026)) is consistent with super-exponential expansion, but we do not fit LPPLS parameters to this data, do not estimate a critical time $t_c$, and make no forecast. The ECB's April 2026 Bank Lending Survey reports that banks expect securitization to further increase lending volumes, consistent with continued acceleration.*

### 4.1 The LPPLS model as a vocabulary

Sornette and colleagues developed the Log-Periodic Power Law Singularity model to describe the mathematical signature of unsustainable growth regimes (Sornette, 2003; Filimonov and Sornette, 2013). The model posits that the logarithm of a growing observable follows:

$$\ln p(t) = A + B($t_c$ - t)^m \left[1 + C \cos\left(\omega \ln($t_c$ - t) + \phi\right)\right]$$

where $$t_c$$ is the critical time, $m ∈ (0,1)$ is the power law exponent, and ω captures the frequency of log-periodic oscillations. The model has three signatures: super-exponential growth (acceleration faster than exponential), log-periodic "shivers" (accelerating oscillations whose frequency increases as $t_c$ approaches), and a finite critical time beyond which the trajectory becomes unsustainable.

The practical value of this vocabulary for our paper is a rigorous name for a system that looks locally stable but is globally accelerating toward a phase transition. Below λ*, the SRT network looks stable: losses are absorbed, cascades terminate quickly, banks report adequate capital. Above λ*, the same system can fail catastrophically from a shock that would have been contained at lower λ. The LPPLS framework describes how systems reach that threshold without anyone declaring an alarm. We do not claim the SRT market is on an LPPLS trajectory; we use the framework to frame what undisclosed accumulation toward λ* would look like from the outside.

### 4.2 Dragon Kings versus Black Swans

Nassim Taleb's Black Swan (Taleb, 2007) describes extreme events that lie in the fat tail of a power-law distribution: rare, large, unpredictable, exogenous. Dragon Kings (Sornette and Ouillon, 2012) are something else: events that sit *beyond* the power-law tail, generated by a distinct mechanism (a bifurcation, a tipping point, a positive feedback loop) rather than by the same process that generates ordinary large events.

The distinction matters for risk management. Fat tails can be partially hedged through diversification: holding many uncorrelated positions limits exposure to any single tail event. Dragon Kings cannot be diversified away because their mechanism is the *correlation structure itself*. When the circular leverage loop fires, the failure of one fund tightens credit availability for all funds in the network simultaneously. There is no uncorrelated position to hide in.

Our simulation tests whether the SRT circular leverage loop produces Dragon King-type cascade distributions. The test is straightforward: at low λ, does the cascade size distribution look like a power law? At high λ, does it develop outlier mass that sits beyond the power law fit? Figure 2 answers yes to both questions.

Dragon Kings are in principle suppressible. Sornette's experiments with coupled chaotic circuits showed that small, targeted perturbations applied to the feedback mechanism itself can prevent extreme events from escalating (Sornette and Ouillon, 2012). The perturbation must act on the loop, not merely on observers' knowledge of it.

For SRT networks, the feedback mechanism is the self-funded credit line. A direct perturbation would sever or limit that link. Disclosure is the policy instrument that makes severing possible: once λ is reported, supervisors can require banks above a threshold to reduce self-funded exposure before the loop reaches criticality, and market counterparties can reprice or withdraw from relationships where circular leverage is concentrated. Disclosure does not automatically cut the loop, but it creates the conditions under which market discipline and regulatory pressure can do so. That is the chain. The dragon is not slain by publishing a number; it is slain by what happens after the number is known.

---

## 5. Simulation Results

### 5.1 Phase transition in cascade size

The primary result is mean cascade size (fraction of the network failing) as a function of λ, averaged over 1,000 Monte Carlo runs per λ value. We report two threshold measures. The first, $λ_{onset}$, is the smallest λ at which mean cascade size first exceeds the λ=0 baseline by more than two standard deviations; it marks where the system departs from normal. The second, λ*, is the λ with the maximum adjacent increase in mean cascade size; it marks the cliff itself. At default parameters, $λ_{onset}$ ≈ 0.90 and λ* ≈ 0.95. Cascade size is approximately flat from λ = 0 to λ ≈ 0.65, rises modestly through $λ_{onset}$, then jumps sharply at λ*. At λ = 1.0, mean cascade size reaches 0.29, roughly three times the λ = 0 baseline of 0.09. The standard deviation of cascade size also peaks near λ*, a classic signature of critical-point behavior. Figure 1 plots this curve.

![Figure 1: Mean cascade size versus self-funding fraction λ. Grey window is [λ_onset, λ*]; shaded band is ±1 SD; dashed line is the λ = 0 baseline. Direct-labeled values are mean cascade at λ = 0 and λ = 1.](fig1_phase_transition.png)

Below $λ_{onset}$, the circular leverage loop exists but most self-funded protection has enough non-self-funded backup: when a bank becomes distressed and calls its self-funded credit lines, the affected funds can find alternative financing and honor their protection commitments. Between $λ_{onset}$ and λ*, cascades start to involve bank distress but typically stop after one or two rounds. Above λ*, independent financing is insufficient. Called credit lines cause fund failures, which trigger more bank distress, which causes more credit line calls. The loop becomes self-reinforcing.

That λ* sits near 0.95 rather than at, say, 0.5 is itself informative. The network tolerates substantial circular leverage as long as some independent financing exists. The policy concern is not the existence of circular leverage but its *undisclosed accumulation* toward high λ values. A disclosed λ = 0.9 would be correctable. An undisclosed one is not.

### 5.2 Dragon King signature in cascade distributions

At λ = 0.10 (stable regime), the cascade size distribution is tight and right-skewed, consistent with power-law tail behavior. At λ = 1.00 (Dragon King regime), a second mode appears at large cascade sizes, representing runs in which the loop fires fully. This outlier mass is not part of the same distribution as the bulk outcomes; it is generated by a distinct mechanism (the credit line call cascade) that is absent at low λ. Figure 2 shows these distributions at λ = 0.10, 0.50, and 1.00.

![Figure 2: Cascade-size distributions at λ = 0.10 (stable), 0.50, and 1.00 (Dragon King), on a shared x-scale. Dotted line is the 95th percentile of the stable-regime distribution; dashed line and number are the panel median; rug marks individual Monte Carlo outcomes.](fig2_distributions.png)

This is the Dragon King signature: not a fatter tail, but a qualitatively different process producing outcomes that sit beyond the tail. Standard Value-at-Risk and Expected Shortfall measures calibrated on the bulk distribution will underestimate the true risk in the Dragon King regime by a large margin.

### 5.3 Sensitivity to investor concentration

We sweep κ across a wider range than our earlier draft, from 0.40 (exposure spread broadly across funds) to 0.98 (exposure highly concentrated in the top funds, matching the BIS top-10 statistic). Figure 3 plots mean cascade curves for κ = 0.40, 0.75, and 0.98. The curves are nearly coincident.

![Figure 3: Mean cascade versus λ across investor concentration κ. The three curves coincide; max |Δμ| at λ = 1 is printed on the figure.](fig3_sensitivity.png) Both $λ_{onset}$ and λ* sit in the same zone (≈ 0.90–0.95) across all three settings, and cascade size at λ = 1.0 is within sampling noise of the baseline value. In this parametrization, κ is not a first-order driver of where the phase transition sits.

This does not mean concentration is irrelevant for policy. It means our simplified model does not capture the mechanisms through which concentration would amplify cascade severity (heterogeneous fund capitalization, idiosyncratic manager reputation effects, or sectoral clustering of reference portfolios). The IMF (2025) top-10 statistic remains a legitimate supervisory concern; our model simply does not reproduce it as a large effect.

### 5.4 Sensitivity to network density

We added a density parameter d (expected number of bank connections per fund) and swept d from 1.0 (each fund repo-financed by a single bank) to 5.0 (each fund has broad redundancy across banks). Higher d means more alternative-financing paths for any one fund: when a bank calls its self-funded credit line, the fund is more likely to find another solvent bank to replace it. Figure 5 plots mean cascade curves for d = 1, 2, 3, and 5.

![Figure 5: Mean cascade versus λ across network density d. Right-edge numbers are mean cascade at λ = 1. Grey window is [min λ_onset, λ*]; the cliff location is invariant, the height is not.](fig5_density_sensitivity.png)

Two findings are notable. First, the transition *location* is almost completely invariant: λ* sits at 0.95 for every d we tested, and $λ_{onset}$ ranges from 0.85 (d = 1) to 0.95 (d ≥ 3). Second, the transition *magnitude* scales dramatically with d. At d = 1, cascade size at λ = 1.0 is 0.18; at d = 5 it is 0.61, roughly 3.5 times larger. The intuition is that more transmission paths mean more banks simultaneously affected when many funds fail, which means more self-funded credit lines are called in the next round, which means more fund failures.

This is the opposite of the classical "diversification reduces risk" intuition and is the clearest Dragon King signature in the parameter sweep. More alternative-financing paths do make the baseline (low λ) cascade slightly larger, but they do not shift where the cliff sits and they make the cliff itself much steeper. The policy implication is that the 95% threshold is a reliable target for supervision across realistic network topologies; what network density controls is how bad the cascade becomes once that threshold is crossed.

### 5.5 Stability across parameters

Running the model with simultaneous rather than sequential updating produces qualitatively identical transition behavior with slightly larger cascade sizes at high λ. Varying B (banks) between 5 and 20 and F (funds) between 10 and 50 shifts both thresholds by at most ±0.05. Increasing tranche thickness δ from 0.04 to 0.15 and shock size s from 0.02 to 0.15 leaves λ* at 0.95 throughout; only $λ_{onset}$ moves modestly within the 0.85–0.95 window. The primary driver of cascade magnitude is density, but the primary driver of cascade *onset* is λ itself.

### 5.5.1 Empirical tranche calibration (new in v2)

Osberghaus and Schepens (2026) report a median junior tranche thickness of 15% in European SRT transactions, nearly double the paper's default δ = 0.08. We re-ran the full 1,000-run Monte Carlo sweep at δ = 0.15 to test whether the empirically observed tranche structure shifts the phase transition. It does not. λ* = 0.95 at both δ = 0.08 and δ = 0.15. The two mean-cascade curves are nearly indistinguishable across the full lambda range (Figure 6); the maximum pointwise difference is 0.007, within sampling noise. Cascade magnitude at λ = 1.0 is 0.294 (δ = 0.08) versus 0.289 (δ = 0.15).

![Figure 6: Mean cascade size versus λ at δ = 0.08 (paper default, solid) and δ = 0.15 (empirical median from Osberghaus and Schepens (2026), dashed). One ±1 SD band (δ = 0.08). Vertical marks show λ_onset tightening onto λ* at the thicker tranche. max |Δμ| is printed on the figure.](fig6_tranche_comparison.png)

The density sweep at δ = 0.15 confirms the same invariance reported in §5.4: λ* = 0.95 at every density from 1.0 to 5.0, with cascade magnitude scaling from 0.18 (d = 1) to 0.62 (d = 5), matching the δ = 0.08 results.

One difference between the two settings: $λ_{onset}$ tightens from 0.90 (δ = 0.08) to 0.95 (δ = 0.15) at the default density. A thicker first-loss tranche absorbs more of the initial shock before funds fail, so the system departs from baseline later. The transition zone narrows from a five-point window [0.90, 0.95] to a single grid point at 0.95. The cliff is sharper with the empirically realistic tranche: there is less warning between "normal" and "cascade." This narrowing strengthens the case for early disclosure. A supervisor watching for the onset signal at δ = 0.08 has a five-point window; at δ = 0.15, onset and cliff are the same point.

### 5.6 LPPLS illustration

Figure 4 shows a synthetic LPPLS time series parameterized to produce a ~5x rise with log-periodic oscillations of the kind documented in credit-market time series (Wosnitza and Sornette, 2015). The figure is labeled synthetic and carries no cascade-onset overlay: mapping a λ value to a time position would imply a $t_c$ prediction that this paper explicitly disclaims. The figure illustrates what super-exponential growth with shivers looks like. It is not evidence of where the real SRT market sits.

![Figure 4: Synthetic LPPLS illustration. Solid: full law; dashed: envelope with C = 0. Horizontal axis is the synthetic coordinate t/t_c. No empirical fit. No t_c prediction.](fig4_lppls_illustration.png)

---

## 6. The Cockpit: Six Public Proxy Metrics

λ is not disclosed. That is the problem. The cockpit is the workaround: a set of publicly observable signals that track the network's proximity to λ* without requiring regulatory data. Each metric is free, updated at least monthly, and connected to either λ or κ via the model.

The simulation provides the ranking methodology, but with an important caveat that we state plainly. For each metric we assign a sensitivity weight (documented in the code) reflecting how directly we think it tracks the model's state variables: fund solvency, reference portfolio quality, interbank funding stress. These weights are judgment calls, not estimated parameters. The simulation computes a single baseline λ at which mean cascade size first exceeds its λ=0 level by two standard deviations, then scales that baseline by each metric's sensitivity weight to produce an ordinal $λ_{trigger}$. The resulting numbers should be read as ranks, not as precise thresholds: saying "metric 1 is earlier than metric 6" is meaningful; saying "metric 1 triggers at exactly λ = 0.59" is not. We have rounded Table 2 values to one decimal place to reflect this.

A second caveat applies specifically to SOFR-OIS. The model contains no interbank funding market, so SOFR-OIS's last-place rank is not derived from a simulated transmission channel. It is a consequence of the sensitivity weight we assigned (0.30) based on the theoretical argument that interbank stress is downstream of fund failures. Readers who disagree with that assumption should adjust the weight and re-run the code.

| Rank | Metric | Q1 2026 | Q2 2026 | Q3 2026 | $λ_{trigger}$ (ordinal) | Source |
|------|--------|---------|---------|---------|---------------------|--------|
| 1 | Secondary market pricing / BDC NAV discount | RED | RED | RED | ~0.6 | Setter Capital; BDC prices; tender filings |
| 2 | BDC stock price dispersion | RED | AMBER* | AMBER | ~0.6 | Daily closes; `bdc_dispersion.py` |
| 3 | PIK ratio in BDC 10-Q filings | RED | RED | RED | ~0.6 | SEC EDGAR; Boston Fed |
| 4 | CLO BB minus AAA spread | AMBER/RED | RED | RED | ~0.6 | Valuation Research; SIFMA |
| 5 | CDS index volume / CDX Financials (FINDX) | RED | AMBER* | PENDING | ~0.7 | ISDA SwapsInfo; IFR |
| 6 | SOFR-OIS spread | GREEN | GREEN | GREEN | ~0.8 | FRED; NY Fed |

*Table 2. Cockpit metrics ranked by sensitivity-weighted ordinal position. Updated in v2.1 to Q3 2026. Metric 2 reads amber; Metric 5 is pending ISDA's Q3 review (mid-November). *Q2 readings for Metrics 2 and 5 are restated from red (v2, judged by eye) to amber under the numeric rules pinned in v2.1; both Q1 readings are red under either method. λ_trigger rounds to one decimal to signal that differences within 0.05 should not be over-interpreted. Metrics 1 to 4 cluster as "early warning", metric 5 is "mid-warning", metric 6 is "late-warning and by assumption". Signal readings are empirical snapshots from public sources, not model output.*

### Metric 1: Secondary market pricing of private credit fund stakes

What it measures: the price at which investors sell private credit fund stakes on the secondary market, relative to reported NAV. A discount signals that market participants believe NAV is overstated or that liquidity is worth a premium, both conditions that precede formal fund stress. Blue Owl fell to an all-time low of $7.95 on April 2, 2026, down 68% from its January 2025 high. Redemption requests from the 12 largest non-traded BDCs averaged 12.1% of NAV in Q1 2026 (median 10.1%), well above the 5% gating threshold (With Intelligence, April 2026). Total Q1 redemption requests reached $20.8 billion across the sector (Woozle Research, April 2026). Moody's downgraded the BDC sector outlook from stable to negative on April 7, 2026. Q2 data show BDC unrealized losses reaching 2.35% of NAV, the worst quarter since 2022 (Reuters analysis of 51 BDCs). Q3 2026 requests eased at several flagship funds but stayed far above caps. Cliffwater's $31 billion interval fund, gated since Q1 (7% paid against about 14% requested), capped Q3 at 5% against about 16% requested, close to Q2's 17% (Private Equity Wire, September 2026). Blue Owl's technology-focused OTIC drew requests near 39% against a 5% cap [VERIFY: tender filing]. Blue Owl halted redemptions from OBDC II entirely earlier in 2026 and began selling assets [VERIFY: date and filing], the terminal state of a queue that does not clear. The UK FCA proposed 90-day notice periods for illiquid retail funds (CP26/35, 8 October 2026). We keep the metric red: the flow of new requests is past peak; the stock of unmet requests is not. Where to find it: publicly listed BDC prices on NYSE/NASDAQ; Setter Capital publishes a secondary market discount index.

### Metric 2: BDC stock price dispersion

What it measures: the cross-sectional standard deviation of publicly traded Business Development Company stock prices. v2.1 pins the computation. For each quarter, prices of a fixed 15-name panel (ARCC, OBDC, FSK, GSBD, GBDC, BXSL, MAIN, HTGC, TSLX, OCSL, PSEC, MFIC, CSWC, NMFC, CGBD) are divided by their first close of the quarter, the cross-sectional standard deviation is taken each day, and the quarter's reading is the median of those daily values. Re-basing each quarter removes the drift that comes from normalizing to a single start date. Status is set against the 2023-2024 median (0.037): red above 2.0 times, amber above 1.25 times. The thresholds are judgment calls, like the sensitivity weights. As a robustness check, the dispersion of quarterly total returns gives the same direction but never reaches red. BDCs hold the types of private credit loans that back SRT reference portfolios. When BDCs trade at similar prices, the market sees uniform credit quality. When dispersion rises sharply, the market is differentiating between managers, a sign that heterogeneous stress is emerging in the underlying portfolio. The script is in the repository (bdc_dispersion.py) and writes results/metric2_bdc_dispersion.csv. No Bloomberg required. Moody's downgraded the BDC sector outlook from stable to negative in Q1 2026; FSK and Goldman Sachs BDC cut dividends in January and February 2026. Readings: Q1 2026 0.074 (2.0 times baseline, red); Q2 0.047 (amber); Q3 0.049 (1.35 times, amber). Dispersion is off its Q1 extreme but has not returned to baseline. The metric is noisy: it read amber in Q1 2023 and Q4 2024 without a matching credit event, and only Q1 2026 crossed the red line in four years of data. Where to find it: Yahoo Finance tickers for ARCC, OBDC, FSK, GSBD, GBDC, and peers.

### Metric 3: PIK ratio in BDC 10-Q filings

What it measures: the fraction of interest income that borrowers pay by capitalizing interest onto the loan principal rather than paying cash (Payment-in-Kind). "Bad PIK" (unplanned PIK toggles due to cash shortfalls rather than contractual PIK provisions) reached 6.4% of total private debt volume in Q1 2026 according to KBRA and Fitch, up from 2.0% in 2022. The Federal Reserve Bank of Boston (August 2026) documents a 67% increase in PIK usage across BDC loans since early 2022, from roughly 6% to 10%, spread across nearly every industry. Lincoln International data show roughly 11% of valued loans carrying PIK interest, with more than half being "bad PIK" not part of original deal terms, amounting to roughly 6% of portfolios requiring interest-payment accommodation. An Ocorian survey (May 2026) of 300 private capital executives found that 96% expect PIK prevalence to increase, and 90% believe growing PIK usage risks masking underlying borrower stress. Distressed maturity extensions overtook PIK/interest deferrals as the leading default mechanism in Q2 2026 (Fitch). Two Q3 readings point in different directions. The BDC median non-accrual ratio reached 2.8% in Q2 2026, the highest since 2017 [VERIFY: primary]. PIK provisions in new loans fell about 46% as lenders tightened terms (WSJ, August 2026 [VERIFY]). The stock of PIK in existing books remains high; the flow is easing. We keep the metric red on the stock. Where to find it: quarterly 10-Q filings on SEC EDGAR, interest income schedules.

### Metric 4: CLO BB minus AAA spread

What it measures: the yield premium demanded by investors in BB-rated CLO tranches over AAA-rated tranches of the same vehicle. CLO reference portfolios overlap substantially with SRT reference portfolios, as both draw from the leveraged loan market. A widening BB-AAA gap signals that mezzanine investors are repricing risk: they are demanding more compensation for the same tranching structure. US CLO BB spreads widened 161 basis points in Q1 2026 alone; BBB by 77 basis points (VanEck, June 2026). Manager-tier dispersion widened sharply: the BB spread difference between Tier 1 and Tier 4 managers reached approximately 400 basis points in US CLOs (TwentyFour Asset Management, March 2026). Middle-market CLO spreads have widened faster than broadly-syndicated-loan CLOs, reflecting credit dispersion and AI-driven software loan stress (Valuation Research Corp., Q2 2026). Through July 2026, BB CLO spreads remain wide of their one-year median (Santander US Capital Markets, August 2026). In Q3 2026, broadly syndicated loan spreads retraced part of the March widening and mezzanine CLO spreads compressed. The BB tranche was the exception: it kept widening modestly while AAA tightened by about 2bp (Valuation Research Corp., Q3 2026). Because the metric is the BB-AAA gap, it widened again in Q3. The reading stays red, though the broader CLO market is calmer than in Q1. Where to find it: FRED (ICE BofA series); SIFMA CLO data; JP Morgan CLOIE index.

### Metric 5: CDS index volume

What it measures: the total notional traded in CDX investment grade and high yield indices, and (new in v2) the CDX Financials Index (FINDX). High volume does not indicate the direction of stress (buyers and sellers both contribute) but record volume indicates that a large number of institutional participants are actively seeking protection or expressing views on corporate credit. Index credit derivatives traded notional reached $7.4 trillion in Q1 2026, up 39.8% year on year, led by CDX IG (ISDA SwapsInfo, May 2026). S&P Dow Jones launched the CDX Financials Index (FINDX) on April 13, 2026, the first standardized CDS index covering private credit fund managers (S&P Dow Jones Indices, January 2026 methodology; Woozle Research, April 2026). FINDX includes 25 North American financial entities, with roughly 12% directly tied to private credit managers including Blackstone, Apollo, Ares, Carlyle, and Blue Owl. Six major banks distribute the product: JPMorgan, Bank of America, Barclays, Deutsche Bank, Goldman Sachs, and Morgan Stanley. FINDX gives a standardized price for financial-sector credit risk with some private credit content, but it has traded thinly. It recorded about $1.5 billion of notional in its first four weeks, against $600 billion on CDX IG over the same span, and its spread fell from 109bp at launch to 98bp; dealers described it as a poor proxy for private credit stress (IFR, May 2026). Market-wide index CDS activity also cooled after Q1: traded notional rose 39.8% year on year in Q1 2026 to $7.4 trillion but fell 2.6% in Q2 to $5.1 trillion (ISDA SwapsInfo, May and August 2026). Single-venue figures run hotter (Tradeweb credit derivatives ADV rose 19.6% in Q2 while the market fell), so we do not use them as a market proxy. Under the rule pinned below (P9c), Q1 reads red and Q2 amber; Q3 is pending. v2.1 pins the reading. The quarterly value is ISDA SwapsInfo index credit derivatives traded notional (US-reported). Status compares that level to the 2023-2024 median quarter, about $2.9 trillion: red above 2.0 times ($5.8 trillion), amber above 1.25 times ($3.6 trillion). A level rule avoids the base effect in year-on-year growth; Q2 2025 contained the April 2025 tariff shock. Readings: Q1 2026 $7.4 trillion (2.6 times, red); Q2 2026 $5.1 trillion (1.8 times, amber). The index market has grown since 2024 (every 2025 quarter sits near 1.8 times baseline), so this rule leans toward amber in calm periods. FINDX trading is reported as context, not scored. Baseline derivation [VERIFY: replace with exact quarterly figures from the ISDA PDFs]: Q1 2023 3.7, Q2 2023 2.2, Q1 2024 2.9, Q2 2024 2.9 (from Q1 and H1 releases); Q3/Q4 2023-2024 back-solved from rounded YTD and full-year growth rates, so about ±$0.2T each. Median $2.9T. Where to find it: DTCC public trade repository; ISDA market surveys; S&P CDX Financials methodology.

### Metric 6: SOFR-OIS spread

What it measures: the spread between the Secured Overnight Financing Rate (repo-based) and the Overnight Index Swap rate (expected policy rate). A wide spread signals that secured interbank funding is becoming expensive relative to the risk-free rate, a sign of funding stress in the repo market, which is a primary channel for bank-to-fund credit extension. In early October 2026, SOFR printed at or a few basis points below IORB (3.87% to 3.90%), with the 99th percentile about 5bp above IORB. This holds after the Federal Reserve raised rates on 16 September 2026. Funding markets show no stress. This metric ranks last in the simulation because interbank funding stress is a downstream consequence of fund failures, not an upstream signal. It historically lags credit deterioration by months. Where to find it: FRED series SOFR; NY Fed daily publications.

### The SOFR-OIS result

The cockpit's structural finding is the gap between when different signals fire. SOFR-OIS, the traditional indicator of interbank funding stress, ranks last in Table 2. Two reasons combine to put it there. First, the model does not contain an interbank funding market, so SOFR-OIS's rank is partly an artifact of the sensitivity weight we assigned based on theoretical argument rather than simulated mechanics. Second, the theoretical argument is straightforward: SOFR-OIS reflects stress in the repo market, which tightens only after fund failures have already propagated through the network. Its ordinal position in Table 2 is closer to the cliff than any other metric, which in practical terms means almost no runway before cascade onset.

The five metrics that rank higher (BDC prices, PIK ratios, CLO spreads, CDS volume) are upstream: they reflect deterioration in the underlying private credit portfolios before that deterioration has forced fund failures or bank credit line calls. Practitioners who rely primarily on SOFR-OIS as a funding-stress indicator will see a green signal until very late in the cascade sequence. Through Q2 2026, all five upstream metrics showed stress while SOFR-OIS stayed flat. In Q3, three upstream metrics stayed red, one eased to amber, one awaits data, and SOFR-OIS stayed green through a rate hike. Six months of readings since v1 are consistent with the predicted firing sequence, but they do not separate two stories: an ordinary credit cycle peaking around Q2, or a pause before further stress. The ordering has not been contradicted; it has not been confirmed either.

---

## 7. Regulatory Implications

### 7.1 The one number that matters

The simulation identifies λ as the key variable. It is already known to the originating bank: a bank knows which credit lines it has extended and to which counterparties, and it knows which funds hold its SRT protection. Requiring banks to disclose λ in Pillar 3 reports (even as a range, even annually) would give regulators the information needed to place each institution on the phase diagram. Banks near λ* would face scrutiny and corrective pressure before a cascade begins.

This is a minimalist ask. We are not proposing a ban on circular leverage structures or a new capital surcharge. We are proposing that one ratio be reported. The BIS (2026) calls for enhanced disclosure of SRT investor funding structures; we formalize what that disclosure should contain.

Since v1, the ECB has taken the closest step toward this disclosure. In March 2026, ECB Supervisory Board member Pedro Machado announced a new survey of banks to analyze SRT financing practices, including the provision of funding by "significant banks" to investors in SRTs originated by other banks (Machado, 2026). Bloomberg reported the ECB is probing leverage underpinning the SRT market and seeking details of which banks lend to SRT buyers. This is a one-time survey, not a standing Pillar 3 disclosure requirement. The gap between a survey and a permanent reporting obligation is the gap between knowing once and watching continuously. Permanent disclosure is the prerequisite for the suppression mechanism described in Section 7.4.

### 7.2 Concentration limits as a complementary tool

Section 5.3 revisits investor concentration (κ) as a potential driver of cascade severity. In our model κ proved a weaker effect than we initially conjectured; the transition sits in the same zone across κ ∈ [0.40, 0.98]. This does not eliminate the IMF (2025) concern about top-10 exposure concentration, but the case for κ-targeted policy in our framework rests on mechanisms we do not simulate (heterogeneous fund capitalization, reputation effects). A supervisory expectation that no single investor hold more than, say, 15–20% of a bank's outstanding SRT exposure is still defensible on general prudential grounds; we simply cannot claim our simulation supports it as a strong lever.

### 7.3 The macroprudential threshold

The simulation places both threshold measures, $λ_{onset}$ and λ*, in the 0.85–0.95 range across every parameter combination tested (density 1–5, κ 0.40–0.98, shock 0.02–0.15, tranche 0.04–0.15). The transition location is therefore a stable target for supervision: a bank whose reported λ approaches 0.85 is approaching the zone where cascade behavior begins to depart from normal, regardless of the broader network's density or concentration structure. What density does control is cascade *magnitude* at and above the threshold: a denser network produces larger failures when the threshold is crossed, which is itself an argument for conservative pre-threshold limits.

Given this stability, a supervisory limit of λ ≤ 0.30 provides a generous margin below the transition zone for all parameter combinations we tested. The limit is not calibrated to be just below $λ_{onset}$; it is calibrated to be far enough below that normal variation in reported λ does not risk approaching the cliff. We see no mechanism in our simulation by which the transition location would move meaningfully below 0.85, but we acknowledge that real SRT networks have features (geographic fragmentation, cross-border regulatory arbitrage, correlated reference portfolios) that our random graph does not capture.

### 7.4 The pro-cyclical capital backdrop (new in v2)

On March 19, 2026, the US federal banking agencies re-proposed the Basel III endgame, reversing the original 2023 proposal. The original framework sought a roughly 19% capital increase for the largest US banks. The reproposal instead delivers an estimated $87.7 billion in system-wide CET1 relief, with capital requirements going down across all bank categories (Holland and Knight, June 2026; Freshfields, March 2026). The comment period closed on 18 June 2026; as of October 2026 no final rule has been issued. [VERIFY at ship date]

This creates a pro-cyclical dynamic directly relevant to the SRT market. Lower capital requirements increase banks' incentive to use SRTs (more capital to free means more demand for the instrument) while simultaneously reducing the capital buffer available to absorb the cascades our model describes. The Osberghaus-Schepens finding that banks redeploy freed SRT capital into new lending rather than building buffers amplifies this concern: capital relief is immediately recycled into new risk, not held in reserve. The paper's recommendation for a conservative supervisory limit of lambda at or below 0.30 becomes more urgent if the capital floor itself is lower. The combination of easier capital rules, continued SRT market growth, and undisclosed circular leverage accumulation is the worst-case scenario for supervisory capacity.

### 7.5 Slaying the dragon

Sornette's key insight about Dragon Kings is that they are suppressible in ways Black Swans are not (Sornette and Ouillon, 2012). A Black Swan (an exogenous, unpredictable shock) cannot be prevented, only absorbed. A Dragon King (an endogenously generated extreme event) can be deflected by identifying and acting on the feedback mechanism that drives it. In coupled chaotic circuit experiments, tiny perturbations applied directly to the feedback loop prevented cascades that would otherwise have become extreme.

For SRT networks, the feedback mechanism is the self-funded credit line. Disclosure is the first step toward cutting it: once λ is reported, supervisors can require banks above a threshold to reduce self-funded exposure, and counterparties can reprice or withdraw from concentrated relationships. Market discipline and regulatory pressure are the actual intervention; disclosure is the prerequisite. A bank that must report λ = 0.88 in its Pillar 3 filing will hear about it from investors and supervisors before it hears about it from a cascade. That is the suppression mechanism. The cockpit provides the early warning. Disclosure creates the conditions for a response.

---

## 8. Limitations

We list our limitations directly.

**λ is partially estimated but not disclosed per-bank.** In v1, lambda was entirely unobservable. Osberghaus and Schepens (2026) now estimate aggregate self-funding at roughly 26%. The PRA's April 2025 "Dear CFO" letter identified that SRT financing was associated with approximately 10% of the outstanding global SRT market (BCBS, 2026). These are market-wide aggregates; per-bank lambda remains unreported. The simulation's value is in characterizing the shape of the risk (nonlinear, concentrated near lambda*), not in estimating where any individual bank sits on the lambda axis. That distinction is what disclosure would resolve.

**Network topology is stylized.** Real SRT networks have heterogeneous bank sizes, fund strategies, and cross-border structures that our random graph does not capture. The BIS (2026) notes that European banks dominate issuance while North American funds dominate buying, a geographic asymmetry our model ignores. The AnaCredit data used by Osberghaus and Schepens could in principle calibrate a more realistic topology, though the data is not publicly available. The density sweep in §5.4 remains our best parametric test: lambda* stays at 0.95 across every density we tested. What topology does appear to affect is cascade *magnitude* at high lambda, which scales with density.

**No central bank intervention.** The model does not include lender-of-last-resort interventions, emergency liquidity facilities, or sovereign backstops. Since v1, the ECB has launched a survey of SRT financing practices (March 2026) and the FSB has announced four formal workstreams on private credit vulnerabilities (May 2026). These represent the first concrete steps toward the supervisory response our model omits, but they are monitoring actions, not intervention mechanisms. The model describes the mechanics of unconstrained contagion; real outcomes depend on policy responses we do not model.

**Monitoring degradation and strategic loan selection are not modeled.** Osberghaus and Schepens (2026) document two channels absent from our simulation: banks reduce borrower monitoring after SRT transfer, and they cherry-pick capital-expensive loans. Both would increase the probability and severity of the initial shock in our cascade engine. Incorporating these channels would likely lower the effective lambda_onset and increase cascade magnitude, making our current results conservative.

**Reference pools are assumed granular.** The model draws the initial shock across a diversified loan pool. SRTs on AI data-centre debt reference a few large, correlated exposures with single-tenant and construction risk, and some are bought by investors who hold equity in the same assets (§2.5). Market participants note that even a 30% data-centre share can erode a thin first-loss tranche (Octus, 2026). In such pools the shock s is lumpy rather than smooth, and tranche thickness δ offers less protection than its nominal size suggests. A v3 extension could draw s from a concentrated, heavy-tailed distribution for a subset of pools, and add a second wrong-way flag for protection sellers that own the reference asset.

**LPPLS is illustrative.** We have not fitted LPPLS parameters to SRT issuance data, estimated $t_c$, or made any prediction about when or whether a critical transition will occur. The framework provides vocabulary, not forecast. Figure 4 is a synthetic illustration; any reader who treats it as a predictive chart has misread it.

**Sensitivity weights are assumptions.** The ranking of the six cockpit metrics in Table 2 depends on sensitivity weights assigned by judgment, not estimation. The λ_trigger values should be read as approximate ordinal positions. The ordering is plausible given the theoretical connections between each metric and the model's state variables, but it is not derived from data. We flag this both here and in the cockpit section itself.

---

## 9. Conclusion

The SRT market solves a genuine problem. Banks need capital relief; investors need yield. Most of the time it works as described. The structural flaw we have analyzed is not in the instrument but in the funding structure of its buyers. When the same bank that originates protection also finances the fund that provides it, the capital relief is partly self-funded. This circular leverage, parameterized as λ, is the variable that determines whether the SRT network distributes risk or concentrates it.

The simulation result is clear: cascade risk in an SRT network is not linear in λ. Below a transition zone, the network absorbs shocks through distributed loss-taking. Above it, a qualitatively different process takes over, the credit line call cascade that is the fingerprint of the Dragon King regime. Standard tail-risk models miss this because they assume the correlation structure is exogenous. In the Dragon King regime, correlation is the mechanism.

The transition sits in the same place across every structural parameter we tested. $λ_{onset}$ (first departure from baseline) ranges 0.85–0.95; λ* (the cliff) sits at 0.95. Network density does not shift this zone, but it does scale the severity of the cascade beyond it, from 18% of the network failing at low density to 61% at high density. A network of real complexity is likely on the high-magnitude side of that range, which strengthens rather than weakens the case for early disclosure.

We cannot place the real market on this phase diagram. Lambda is not disclosed at the per-bank level. Osberghaus and Schepens (2026) place the market-wide average at roughly 0.26, well below the critical zone, but the distribution's tail is unknown. What we can say is that six proxy metrics designed to track proximity to the critical zone read, as of Q3 2026, three red, one amber and one green, with the CDS index reading pending. The one indicator that remains green (SOFR-OIS) is, by the model's assumption, a lagging signal that fires after fund failures have already occurred. Since v1, the downstream metric has stayed flat while upstream metrics worsened, then partly eased. Whether this reflects proximity to the transition zone or ordinary credit cycle stress, we cannot say with the data available. The model gives us the mechanism and the warning structure; it does not tell us where we are.

The six months since v1 have moved the paper's central claim from theoretical to partially empirical. The circular leverage channel exists in real transaction data. The monitoring degradation and strategic loan selection channels, absent from our model, make the real system more fragile than our simulation suggests. Regulators have begun to look, which is progress. They have not yet required disclosure, which is not. Meanwhile banks have begun cutting the leverage lines that close the loop, are passing new AI debt to non-bank lenders at origination, and are transferring data-centre risk through SRTs into pools the model treats as diversified.

One number would tell us. Lambda is already sitting in bank risk systems, computable from credit facility records and SRT counterparty lists. It is not being reported. The US Basel III reproposal (March 2026), by lowering capital requirements, has increased both the incentive to issue SRTs and the systemic cost of the cascades they can produce. Disclosure is the prerequisite for supervision, market discipline, and any intervention targeted at the feedback loop itself. Until then, the cockpit is the best we can do from outside.

---

## References

[Authors]. (2026). *Do redemption gates discipline or destabilize? Evidence from the 2026 run on semi-liquid private credit funds*. Research Square. https://www.researchsquare.com/article/rs-10704359/v1

Bank for International Settlements. (2026). *The rise and risks of synthetic risk transfers*. BIS Quarterly Review, March 2026. https://www.bis.org/publ/qtrpdf/r_qt2603c.htm

Basel Committee on Banking Supervision. (2026, February 17). *Synthetic risk transfers*. BCBS report d607. https://www.bis.org/bcbs/publ/d607.htm

Bloomberg. (2026, April 22). *TD Bank mulls hedging data center debt with rare SRT deal*. https://www.bloomberg.com/news/articles/2026-04-22/td-bank-mulls-hedging-data-center-debt-with-rare-srt-deal

Bloomberg. (2026, September 7). *Deutsche Bank hedges data center risk in SRT on €2 billion book*.

Bloomberg. (2026, October 12). *JPMorgan, Goldman curb exposure on $5 billion Volta AI loan*. https://www.bloomberg.com/news/articles/2026-10-12/jpmorgan-goldman-curb-exposure-on-5-billion-volta-ai-loan-sale

European Central Bank. (2026, April). *Euro Area Bank Lending Survey, Q1 2026*. Ad hoc securitization questions. https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.pr260428~6b156107c1.en.html

Federal Reserve Bank of Boston. (2026, August). *Early Warning Signals in Private Credit? What BDC Portfolios Reveal about Emerging Risks*. Current Policy Perspectives 26-6. https://www.bostonfed.org/publications/current-policy-perspectives/2026/early-warnings-private-credit-bdc-portfolios.aspx

Filimonov, V., and Sornette, D. (2013). A stable and robust calibration scheme of the log-periodic power law model. *Physica A*, 392(17), 3698-3707. https://doi.org/10.1016/j.physa.2013.04.012

European Systemic Risk Board. (2025, May). *Unveiling the impact of STS on-balance-sheet securitisation on EU financial stability*.

Financial Conduct Authority. (2026, October 8). *CP26/35*. [VERIFY: URL]

Financial Stability Board. (2026, May 6). *Report on Vulnerabilities in Private Credit*. https://www.fsb.org/uploads/P060526.pdf

Financial Times. (2026, May). Banks seek to offload data centre risk. [VERIFY: exact title, URL]

IFR. (2026, May). *CDS traders aren't worried about private credit*. https://www.ifre.com/topic-codes/2434154/cds-traders-arent-worried-about-private-credit

International Monetary Fund. (2025). *Recycling Risk: Synthetic Risk Transfers*. IMF Working Paper WP/25/200. https://doi.org/10.5089/9798229027748.001

International Monetary Fund. (2026). *Banking on Nonbanks*. IMF Working Paper WP/26/23. https://doi.org/10.5089/9798229039208.001

ISDA. (2026, May 12). *SwapsInfo First Quarter of 2026 Review*. https://www.isda.org/2026/05/12/swapsinfo-first-quarter-of-2026-review/

ISDA. (2026, August 11). *SwapsInfo First Half of 2026 and the Second Quarter of 2026 Review*. https://www.isda.org/2026/08/11/swapsinfo-first-half-of-2026-and-the-second-quarter-of-2026-review/

Machado, P. (2026, March 24). *Changing the tune but not the tone: synthetic risk transfers in Europe*. ECB Banking Supervision speech. https://www.bankingsupervision.europa.eu/press/speeches/date/2026/html/ssm.sp260324~2b54f795e3.en.html

Octus. (2026). *Investors warn data center SRTs function as asset gathering*. https://octus.com/?p=43623

Octus. (2026). *SRT Weekly Wrap: High issuance volume meets new reality of risk repricing*. https://octus.com/?p=41215

Osberghaus, A., and Schepens, G. (2026). Synthetic, but how much risk transfer? ECB Working Paper No. 3210. https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp3210~e2dc529b33.en.pdf Also SSRN 6482739.

Private Equity Wire. (2026, September). Cliffwater Corporate Lending Fund caps Q3 redemptions at 5%. [VERIFY: URL]

S&P Dow Jones Indices. (2026, January). *CDX Financials Indices Methodology*.

Semafor. (2026, October 13). *Volta's $5 billion debt deal is a pulse check on the AI-financing boom*. https://www.semafor.com/article/10/13/2026/voltas-5-billion-debt-deal-is-a-pulse-check-on-the-ai-financing-boom

Sornette, D. (2003). *Why Stock Markets Crash: Critical Events in Complex Financial Systems*. Princeton University Press. https://doi.org/10.1515/9781400829552

Sornette, D., and Ouillon, G. (2012). Dragon-kings: Mechanisms, statistical methods and empirical evidence. *European Physical Journal Special Topics*, 205(1), 1-26. https://doi.org/10.1140/epjst/e2012-01559-5

Taleb, N.N. (2007). *The Black Swan: The Impact of the Highly Improbable*. Random House.

Troutman Pepper Locke. (2026, July). *Banks are pulling back: What private credit funds need to know now*. https://www.troutman.com/insights/banks-are-pulling-back-what-private-credit-funds-need-to-know-now/

TwentyFour Asset Management. (2026, March). *CLOs reprice as software and geopolitics test sentiment*.

Valuation Research Corp. (2026, June 30). *Structured Products Market Trends: Q2 2026 CLO and ABS Update*.

Valuation Research Corp. (2026). *Structured Products Market Trends: Q3 2026 CLO and ABS Update*. https://www.valuationresearch.com/insights/structured-products-market-trends-q3-2026/

VanEck. (2026, June). *CLOs: Pressure-Tested in Q1, Built for What Comes Next*.

Woozle Research. (2026, April 13). *When Wall Street builds a short: What the S&P CDX Financials Index means for private credit*.

Wosnitza, J.H., and Sornette, D. (2015). Analysis of log-periodic power law singularity patterns in time series related to credit risk. *European Physical Journal B*, 88, 97. https://doi.org/10.1140/epjb/e2015-50019-9

---

## Appendix A: Glossary

A plain-English reference for technical terms used in the paper. Terms are ordered by appearance.

| Term | Plain-English explanation |
|------|---------------------------|
| **Synthetic Risk Transfer (SRT)** | Financial insurance where a bank pays a fund to absorb losses on a loan portfolio, allowing the bank to tell regulators the risk is "transferred" while keeping the actual loans on its books. |
| **Circular leverage (λ)** | The fraction of SRT protection that a bank effectively funds itself. If a bank lends money to the fund that insures its loan portfolio, then under stress the fund needs more credit from the bank exactly when the bank can least afford to provide it. λ measures how much of the protection is funded this way. |
| **Phase transition** | A sharp boundary where a system suddenly changes behavior, like water freezing at 0°C. In this paper, it is the point where stable risk-sharing becomes unstable contagion. |
| **Dragon King** | An extreme event so large it sits *beyond* the normal "fat tail" of a probability distribution, generated by internal feedback mechanisms rather than external shocks. Unlike Black Swans, Dragon Kings are in principle suppressible because their mechanism can be identified and acted on. |
| **Log-Periodic Power Law Singularity (LPPLS)** | A mathematical pattern showing accelerating growth with increasingly frequent oscillations, often documented before market crashes. This paper uses LPPLS as a conceptual lens for super-exponential growth, not as a prediction tool; no LPPLS fit is performed. |
| **Tranche thickness (δ)** | The size of the "first loss" layer in a loan pool. δ = 0.08 means the fund absorbs the first 8% of losses before the bank is affected. |
| **PIK (Payment-in-Kind)** | When borrowers cannot pay cash interest, they add the interest to the loan balance instead. Like paying your credit card minimum by increasing your debt. Rising "bad PIK" ratios signal distressed borrowers. |
| **BDC (Business Development Company)** | A publicly traded company that makes loans to small and mid-sized businesses. Essentially a private credit fund that trades on stock exchanges; BDC prices and 10-Q filings give public windows into private credit health. |
| **CLO (Collateralized Loan Obligation)** | A structured product that pools leveraged loans and slices them into tranches (AAA to BB). The spread between risky (BB) and safe (AAA) tranches signals how much investors fear credit losses. |
| **SOFR-OIS spread** | The difference between what banks charge each other for overnight loans (SOFR) and the risk-free rate (OIS). Wider spreads signal interbank funding stress, but the paper shows this indicator fires late in the cascade sequence. |
| **RWA (Risk-Weighted Assets)** | The regulatory measure of a bank's total risk exposure. Lower RWAs mean the bank can lend more with the same capital cushion. SRTs work by reducing RWAs. |
| **Cascade** | The chain reaction of failures: some loans default, the fund cannot pay, the bank calls its credit line, the fund fails, the bank loses capital relief, the bank calls more credit lines, more funds fail. Cascade size measures what fraction of the network ultimately collapses. |
| **κ (investor concentration)** | The fraction of SRT exposure held by the largest funds. The IMF (2025) reports that the top 10 investors hold over 75% of outstanding exposure; that corresponds to κ ≈ 0.75 in the model. |
| **Network density (d)** | The expected number of banks each fund is connected to. Higher d means more alternative-financing paths per fund. In the model, d controls cascade magnitude at high λ but does not shift the transition location. |

---

## Appendix B: Simulation Code

The full simulation is contained in a single file, `srt_simulation.py`. Dependencies are `numpy`, `networkx`, `matplotlib`, and `scipy`. No proprietary data is required.

To reproduce all figures and the cockpit CSV at publication quality:

```bash
python srt_simulation.py
```

To run a fast development version (300 Monte Carlo runs instead of 1,000):

```bash
python srt_simulation.py --quick
```

Output: `figures/fig1_phase_transition.pdf`, `fig2_distributions.pdf`, `fig3_sensitivity.pdf`, `fig4_lppls_illustration.pdf`, `fig5_density_sensitivity.pdf`, `fig6_tranche_comparison.pdf`, and `figures/cockpit_metrics.csv`.

The random seed is set globally (`DEFAULT_SEED = 42`) for reproducibility. To verify stability across seeds:

```python
from srt_simulation import main
for seed in [42, 123, 999, 2026]:
    main(seed=seed, n_runs_sweep=500, out_dir=f'figures_seed_{seed}')
```

All code is released under the MIT License.
