# Changelog

All notable changes to this companion repository are documented here.

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
