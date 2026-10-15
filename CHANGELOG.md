# Changelog

All notable changes to this companion repository are documented here.

## [Unreleased] — 2026-10-15 — v2.1 prep (pending ISDA Q3)

- Paper v2.1 (`dyb-2026k-circular-nw-risk-v2.1.md` / `.pdf`): empirical refresh only. No simulation re-run; λ_onset, λ*, density and δ results unchanged
- Cockpit Q3 2026: 3 RED / 1 AMBER / 1 GREEN / 1 PENDING (v2: 5 RED / 1 GREEN at Q2/Q3)
- New §2.5 field evidence: bank back-leverage tightening, Volta underwriting pullback, gate queues, data-centre SRTs bought by asset owners
- New §8 limitation: granular reference pools assumed; concentrated data-centre pools violate it
- `srt_simulation.py`: `COCKPIT_CURRENT` updated to Q3 2026 readings and thresholds; new `COCKPIT_AS_OF`; CSV columns now `current_value`, `threshold`, `as_of` (was `current_value_q1_2026`). Readings are display only and do not enter `lambda_trigger`, `lead_fraction` or rank
- Added `bdc_dispersion.py` (Metric 2) and `results/metric2_bdc_dispersion.csv`; market deps in `requirements-market.txt`, kept out of `requirements.txt` and out of `verify_srt_claims.py`
- Added Figure 7 (`plot_metric2_sparkline.py`): Metric 2 sparkline through Q3 2026, 1.25x / 2.0x reference lines. Simulation Figures 1-6 unchanged

### Restated (v2 readings changed under v2.1 rules)

- Metric 2 (BDC dispersion), Q2 2026: RED → AMBER. v2 was judged by eye; v2.1 pins the measure (15-name panel, quarter-rebased median daily std) and thresholds (1.25x / 2.0x the 2023-24 median). The old code threshold ("std dev > 15%") is dropped
- Metric 5 (CDS index volume), Q2 2026: RED → AMBER under the pinned level rule (1.25x / 2.0x the 2023-24 median quarter, ~$2.85T ISDA index notional). Q3 is PENDING until ISDA's Q3 SwapsInfo review (expected mid-November 2026)
- Metric 5, Q1 2026 figure and source replaced: "$4.5T, +69% YoY, record" (Kobeissi Letter, social media) → $7.4T, +39.8% YoY (ISDA SwapsInfo Q1 2026). Reading stays RED
- Metric 5 text: FINDX no longer described as a real-time price for private credit risk; it traded thinly (IFR, May 2026)

### Not adopted (failed verification)

- Moody's downgrade of major US banks (28 Sep 2026): aggregator only
- Tradeweb credit derivatives ADV as a Metric 5 input: single venue, rose while market-wide ISDA volume fell in Q2

## [Unreleased] — 2026-10-15 — Figure 1 axis labels (repo-only)

- Kept Figure 1 λ_onset / λ* labels fully inside the axes (`srt_simulation.py` + regenerated PNG/PDF)
- Repo companion only — no new Zenodo paper version; science path and claims unchanged

## [Unreleased] — 2026-09-04 — figure restyle (repo-only)

- Restyled Figures 1–6 (PNG/PDF): in-figure titles, reading guides, reserved title/footer bands
- Updated `srt_simulation.py` figure pipeline to match; science path and claims unchanged
- Repo companion only — no new Zenodo paper version; Zenodo PDF pin remains v2 `21995468`
- `ZENODO.md`: record legacy OSF paper mirrors refreshed for v2

## [Unreleased] — 2026-08-18 — robustness check (v2 companion)

- Added `ROBUSTNESS_CHECK_dyb-2026k-v2.md`: full-surface stress test of paper v2 (22 frozen rows; own-draft mode)
- Headline T0–T2 claims reproduce; keystones call out self-funding flag order and λ* grid/detector artifacts
- Repo companion only — no new Zenodo paper version
- Zenodo `21995468`: metadata note + `isSupplementedBy` URL to the GitHub robustness check (same DOI; file bucket locked without a new version)

## [2.0] — 2026-08-18 — paper v2

- Paper v2 (`dyb-2026k-circular-nw-risk-v2.md` / `.pdf`): Osberghaus and Schepens (2026) calibration, Figure 6 (δ = 0.15 vs 0.08), cockpit through Q2/Q3 2026, Tufte restyle of Figures 1–5
- Citation repairs: BIS/BCBS wording, Wosnitza and Sornette (2015), IMF (2025) for the 75% top-10 figure, Osberghaus monitoring and stock-date wording
- Release surfaces: `ZENODO.md`; `CITATION.cff` (concept `10.5281/zenodo.19632277`; v2 `10.5281/zenodo.21995468`)
- Thin claim gate still green (seed 42, n_runs=80): λ_onset=0.90, λ*=0.95, μ(1)/μ(0)=3.68

## [Unreleased] — 2026-08-18 — claim-gate re-verify

- Re-ran `srt-phase-transition` via `verify_claim_project.py`: **pass** (seed 42, n_runs=80, 6.4s)
- Observed values unchanged: λ_onset=0.90, λ\*=0.95, μ(1)/μ(0)=3.68, jump ratio=12.1
- Refreshed `results/` evidence, including `claim_verify_brief.md`
- README: dropped “new” labels; listed last-verified date and full evidence set

## [Unreleased] — 2026-08-17 — figure embeds

- Paper md now embeds Figures 1–5 (`fig1_phase_transition.png` … `fig5_density_sensitivity.png`) so Typora can export a figure-bearing PDF. No figure restyle.

## [Unreleased] — 2026-08-07

### Added

- **Computational claim gate** for load-bearing phase-transition claims:
  - `verify_srt_claims.py` — thin Monte Carlo harness (seed 42, n_runs=80)
  - `claim-manifest.json` — `cd-claim-gate/v1` claim `srt-phase-transition`
  - `results/` evidence: `claim_verify_meta.json`, `claim_verify_out.txt`,
    `srt_claim_verify.json`, `claim-holds-brief.md`
- README **Quickstart** now starts with the claim gate before full / `--quick` runs
- This CHANGELOG

### Notes

- Gate checks λ_onset / λ\* location, two-stage order, and nonlinearity — **not**
  a substitute for the publication 1000-run sweep or density magnitude claims
- Non-claims and residual risk: `results/claim-holds-brief.md`
- Re-run: `python verify_srt_claims.py` or
  `verify_claim_project.py --project .` from computational-claim-gate
