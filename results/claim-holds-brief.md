# Claim-holds brief — circular-networks-SRT-networks

## Status
**Verified** (thin Monte Carlo gate, 2026-08-18; `status=pass`)

## Claims

| id | command | exit | notes |
|----|---------|------|-------|
| `srt-phase-transition` | `python verify_srt_claims.py` | 0 | 6.4s; seed 42; n_runs=80 |

### Observed (gate run)

| quantity | value | gate band |
|----------|-------|-----------|
| λ_onset | 0.90 | [0.75, 0.95] |
| λ* | 0.95 | [0.90, 1.00] |
| μ(λ=1)/μ(λ=0) | 3.68 | ≥ 1.8 |
| max_jump / early_max | 12.1 | ≥ 4.0 |

Structural checks: `lambda_actual` tracks requested λ; cascade_size ∈ [0, 1].

## Seeds / env / platform

- Seed: **42** (`DEFAULT_SEED` / harness `SEED`)
- n_runs (gate): **80** (paper publication sweep: **1000**)
- Shock size: 0.05
- Grid: linspace(0, 1, 21)
- Interpreter: host Python with numpy, networkx, matplotlib, scipy
- Evidence written by `computational-claim-gate` `verify_claim_project.py` (2026-08-18T01:37:27Z)

## Not checked here

- Full publication Monte Carlo (1000 runs / κ / density sweeps)
- Density *magnitude* scaling 0.18–0.61 at high λ
- Multi-seed stability of λ*
- Cockpit proxy **market** readings (Q1 2026) — judgment + public data, not sim
- LPPLS parameter fits or critical-time prediction (paper non-claim)
- Mathematical proof of the transition (MC only)

## Evidence

- `results/claim_verify_meta.json`
- `results/claim_verify_out.txt`
- `results/claim_verify_brief.md`
- `results/srt_claim_verify.json` (harness payload)
- Project `claim-manifest.json`

## Residual risk

Thin n_runs can shift λ_onset by one grid step (±0.05) under RNG or code edits; bands are intentionally wider than paper prose. A green gate does **not** re-prove the full preprint figures — re-run `python srt_simulation.py` for publication-grade artifacts.
