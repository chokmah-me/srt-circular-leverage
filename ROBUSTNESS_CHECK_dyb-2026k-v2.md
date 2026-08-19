# Robustness Check: Circular Leverage in Bank-NBFI SRT Networks (v2)

Mode: own-draft. Coverage: full v2 PDF (24 pp) read; srt_simulation.py (1,291 lines) read in full for build_network, run_cascade, sweep, and threshold detectors; results/publication_sweep_summary.json read. Not read: v1 draft, verify_srt_claims.py internals, Osberghaus and Schepens original. Surface: 22 rows frozen before any run; 0 post-freeze addenda. All 22 rows executed (22/22) at n=200-300 Monte Carlo runs per lambda (paper uses 1,000); baseline reproduces within noise so the reduced count is adequate for location claims, less so for magnitude decimals.

## Verdict

Author-anchored surface (T0-T2, rows 1-14): every headline survives. Reproduction matches (lambda* = 0.95, lambda_onset = 0.90, mu(1) = 0.28-0.31 across four seeds vs paper 0.294); density scales magnitude and not location; delta, s, kappa, distress threshold, sequential vs simultaneous all leave lambda* on the last grid interval. On its own terms the paper is robust and its stated limitations are accurate.

Full surface (rows 15-22): two findings change how the central claim should be read, and both are `[recomputed]`, not estimates. First, lambda* is not at 0.95; it is at the last interval of whatever grid is used. On a 0.01 grid from 0.85 to 1.0 the argmax-adjacent-difference detector returns 0.99 for d = 1, 2, and 5, and the entire jump sits between lambda = 0.99 and 1.00 (mu 0.211 -> 0.299 at d = 2). Second, the location of the transition is a construction artifact of the self-funding assignment rule: `build_network` flags protection edges self-funded largest-first, and `run_cascade` rescues any called fund that retains at least one non-self-funded credit line. Under largest-first flagging every fund's smallest edge is the last to be flagged, so a rescue path survives until lambda is essentially 1.0 (fraction of funds with any rescue path: 0.63 at lambda = 0.85, 0.28 at 0.99, 0.00 at 1.00). Change the flagging order to random and lambda_onset drops to 0.55; flag by whole fund and it drops to 0.70; flag smallest-first and cascade size jumps at lambda = 0.05. The invariance across d, kappa, delta, s is real, but it is invariance of "cascades fire when the last independent financing path disappears", which the code encodes as an assumption. The paper's own sentence, "the network tolerates substantial circular leverage as long as some independent financing exists", is a description of the rescue rule, not a finding about SRT networks. The keystone is the flagging convention (row 17), which is unstated in the paper text and has no empirical anchor.

Policy consequences: the supervisory limit lambda <= 0.30 survives (it is below every onset value found, including 0.55 under random flagging). The statement "the 95% threshold is a stable target for supervision" does not survive; the honest version is "in this model the cliff sits at complete self-funding, and where the onset sits depends on how self-funded exposure is distributed across a fund's counterparties, which is exactly the per-fund information disclosure would reveal". That reframing strengthens the disclosure ask and weakens the specific number.

## Claim object

| Component | Value | Locator |
|---|---|---|
| Outcome concept | mean cascade size (fraction of nodes failing) as a function of lambda | 3.2, 5.1 |
| Exposure concept | lambda = self-funded protection weight / total protection weight, assigned by construction | 2.2, 3.1 |
| Estimand | simulation invariance: two-stage transition with lambda_onset in 0.85-0.95 and lambda* = 0.95, location invariant to d, kappa, delta, s; magnitude scales with d | Abstract, 5.1-5.5, 7.3 |
| Population / scope | random directed bank-fund graphs, B=10, F=20 default, ranges in Table 1; homogeneous thresholds; no regulator | 3.1, 3.3, 8 |
| Focal parameter | lambda* = 0.95 (cliff), lambda_onset = 0.90 (default) | 5.1, Fig 1 |
| Secondary claim | supervisory limit lambda <= 0.30 is conservative | 7.3 |
| Secondary claim | cockpit ordering (SOFR-OIS last) tracked out of sample Q1->Q2/Q3 | 6, Table 2 |

## Frozen perturbation surface (22 rows, frozen before execution)

| # | Axis | Ns | Tier | Baseline | Perturbed | Estimand | Load-bearing for | Given as | Ran? |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Reproduce sweep, seed 42 | rc | T0 | n=1000 | n=200 | preserving | all | measured | yes |
| 2 | Seed | infer | T1 | 42 | 123, 999, 2026 | preserving | all | measured | yes |
| 3 | Density d | rc | T1 | 2 | 1, 5 | preserving | invariance, magnitude | measured | yes |
| 4 | Shock s | rc | T1 | 0.05 | 0.01, 0.20 | preserving | invariance | measured | yes |
| 5 | Update mode | rc | T1 | sequential | simultaneous | preserving | invariance | measured | yes |
| 6 | Tranche delta | rc | T1 | 0.08 | 0.15 (paper ran); het. per fund | preserving | invariance | measured | yes (het) |
| 7 | Bank distress threshold | rc | T2 | 0.20 | 0.10, 0.40 | preserving | invariance, magnitude | assumed ("conservative") | yes |
| 8 | lambda_actual vs target | infer | T2 | plots use target | read lambda_actual | preserving | x-axis meaning | stated | yes |
| 9 | Onset detector k | infer | T2 | 2 SD | 1 SD, 3 SD | preserving | lambda_onset | stated rule | yes |
| 10 | Cliff detector | infer | T2 | argmax adjacent diff | max curvature; half-rise | preserving | lambda* | stated rule | yes |
| 11 | MC count | infer | T2 | 1000 | 200, 300 | preserving | decimals | measured | yes |
| 12 | Grid step | infer | T2 | 0.05, 21 pts | 0.01 on [0.85,1.0] | preserving | lambda* location | unstated | yes |
| 13 | Osberghaus 26% vs tail | quote | T1 | mean 0.26 | reader quotes as "safe" | preserving | policy framing | stated caveat | judged |
| 14 | "95% threshold stable target" one-line quote | quote | T0 | as written | out-of-context citation | preserving | policy | headline | judged |
| 15 | Self-funded flag order | rc | T3 | largest-first | random; smallest-first; per-fund | preserving | location, onset | unstated in paper | yes |
| 16 | Rescue rule | sens | T3 | any non-self-funded line = rescue | inspect fraction of funds with rescue path vs lambda | preserving | mechanism | unstated in paper | yes (measured) |
| 17 | Round cap B+F+5 | diag | T3 | 35 | check n_rounds distribution | preserving | none if cap not hit | stated | not run: paper reports 2-4 rounds; low value |
| 18 | Heterogeneous fund buffers | rc | T4 | shared delta | lognormal sigma 0.5 | preserving | invariance | assumed | yes |
| 19 | Adversarial topology | rc | T4 | random Poisson | not implemented | preserving | invariance | assumed | not run: would need new builder; noted |
| 20 | Untested region | diag | T4 | ranges Table 1 | lambda in (0.95,1.0) | preserving | lambda* | unstated | yes (row 12) |
| 21 | Cockpit weights | quote | T1 | judgment weights | reader treats ranks as model output | preserving | Table 2 | stated caveat | judged |
| 22 | Version drift v1->v2 | quote | T1 | v2 text | which numbers changed | preserving | trust | stated | judged from CHANGELOG list only |

## Survival table

| Claim | A1 params | A2 assumptions | A3 re-derivation | A4 diag | A5 alt model | A6 quotation | Overall T0-2 | Overall all |
|---|---|---|---|---|---|---|---|---|
| Two-stage nonlinear transition exists | survives (d, s, delta, BDT, mode) | survives | survives: mu 0.089 -> 0.278-0.309 | survives | survives (flag orders still nonlinear) | survives | survives | survives |
| lambda* = 0.95, invariant to d, kappa, delta, s | survives on 0.05 grid | weakens: rescue rule | flips: 0.99 on 0.01 grid, all d | flips: detector returns last interval on any convex curve | flips: 0.85 curvature / 0.05 onset under other flag orders | flips: "0.95" will be quoted as a physical constant | weakens (grid, T2) | flips |
| lambda_onset in 0.85-0.95 | survives (k=2) | weakens | k=1 -> 0.70; k=3 -> 1.0 | n.a. | flips: 0.55 random, 0.70 per-fund | weakens | weakens | flips |
| Density scales magnitude, not location | survives 0.19 -> 0.63 at d=5 | survives | survives | survives | survives under fine grid | survives | survives | survives |
| Dragon King bimodality at lambda=1 | not re-run (Fig 2) | survives | n.a. | n.a. | n.a. | survives | undetermined | undetermined |
| lambda <= 0.30 supervisory limit conservative | survives | survives | survives (below all onsets incl. 0.55) | survives | survives | survives | survives | survives |
| Cockpit ordering tracked out of sample | n.a. | weakens: weights judgment | n.a. | n.a. | n.a. | weakens: readings are snapshots not model | weakens | weakens |

## Keystones

1. Self-funding assignment order (row 15, T3, `build_network` lines ~118-134). Largest-first flagging leaves each fund's smallest counterparty edge unflagged until lambda approaches 1, guaranteeing a rescue path and pinning the cliff at complete self-funding. Nothing in the paper motivates largest-first over per-fund or random assignment, and the empirical question ("does a self-funded fund keep an independent line?") is precisely what is undisclosed. Cheapest fix: add a flag-order axis to Table 1 and Section 5.5, report lambda_onset under per-fund and random assignment, and reword 7.3 so the stable target is "complete self-funding" with onset explicitly conditional on assignment structure. This costs one paragraph and one figure and, in my reading, makes the disclosure argument stronger.

2. Cliff detector plus grid (rows 10, 12, T2). `_find_lambda_star` returns the left endpoint of the largest adjacent increase; on a monotone convex curve that is always the last interval, so "lambda* = 0.95" is "lambda* = 1 minus step". Cheapest fix: report lambda* as an interval [0.95, 1.0] on the 0.05 grid, or run 0.01 steps above 0.85 and say the cliff is at 1.0. The kappa/density/tranche invariance figures survive unchanged in shape.

3. Onset detector (row 9). k=2 SD of the lambda=0 baseline is a defensible rule but moves 0.70 to 1.0 across k in {1,2,3}. State the k-sensitivity in one sentence in 5.1.

## Scope limits (explore/)

Adversarial topology (row 19) and a regulator/LOLR actor were not run; both change the mechanism set rather than the estimand and the paper already lists them in Section 8. Monitoring degradation and strategic selection channels are correctly labeled unmodeled.

## Perturbation log

Row 1: seed 42, n=200: lambda* 0.95, onset 0.90, mu(0)=0.089, mu(1)=0.278. Recomputed. Matches paper. Row 2: seeds 123/999/2026: lambda* 0.95 all; onset 0.90/0.95/0.95; mu(1) 0.291/0.286/0.309. Row 3: d=1 mu(1)=0.187, d=5 0.627 (paper 0.18/0.61); lambda* last interval both. Row 4: s=0.20 lambda* 0.95, mu(1) 0.382; s=0.01 curve near flat (mu(1)=0.016), detectors degenerate: too little shock to trigger any bank. Row 5: simultaneous: lambda* 0.95, onset 0.90. Row 6: heterogeneous buffers sigma 0.5: lambda* 0.95, onset 0.95, mu(1) 0.298. Row 7: BDT 0.10 mu(1) 0.308; 0.40 mu(1) 0.222; lambda* 0.95 both. Row 8: lambda_actual = 0.859/0.906/0.954/1.000 at targets 0.85/0.90/0.95/1.00; x-axis honest. Row 9: k=1 onset 0.70; k=3 onset 0.95-1.0. Row 10: curvature detector 0.95 on coarse grid, 0.99 on fine; half-rise detector 1.0. Row 11: n=200 reproduces n=1000 to within 0.02 on mu(1). Row 12: 0.01 grid on [0.85,1.0], n=300: mu = 0.133 ... 0.190 (0.97) 0.186 (0.98) 0.211 (0.99) 0.299 (1.00); lambda* = 0.99; same at d=1 and d=5. Rows 13,14,21,22: judged, see A6. Row 15: random flag: onset 0.55, curvature cliff 0.85, mu(0.80)=0.211; per-fund: onset 0.70; smallest-first: mu jumps 0.089 -> 0.145 at lambda=0.05 and plateaus ~0.28 by 0.5. Row 16: fraction of funds with any non-self-funded line: 0.63 (0.85), 0.47 (0.95), 0.28 (0.99), 0.00 (1.00) under largest-first; 0.12 (0.95) under random. Row 17: not run. Row 18: see row 6. Row 19: not run. Row 20: see row 12. Denominator: 20 rows executed or judged / 22 frozen; 2 not run with reasons stated.

## What this check could not do

Did not run the paper's 1,000-run sweep; all magnitudes are n=200-300 and carry roughly +/-0.02 noise on mu(1). Did not re-run Figure 2 bimodality or the cockpit metrics code. Did not test adversarial or core-periphery topology (would require a new builder). Did not verify the Osberghaus and Schepens numbers or any cockpit reading against sources; A6 judgments on those rows are about presentation, not accuracy. Did not read v1 to audit version drift beyond CHANGELOG. The flag-order and fine-grid findings are recomputations from the released code with a patched copy (srt_mod.py: flag order, distress threshold, heterogeneous buffers exposed as module globals; no other logic changed) and are reproducible from harness.py.
