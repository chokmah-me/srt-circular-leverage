# Circular Leverage in Bank-NBFI SRT Networks

**Preprint:** [https://zenodo.org/records/19632278](https://doi.org/10.5281/zenodo.19632278)

**License:** MIT (code) · CC BY 4.0 (paper)  

**Status:** Preprint, April 2026

**Claim gate (new):** `python verify_srt_claims.py` — thin re-run of load-bearing phase-transition claims (~10s). See [Quickstart](#quickstart), [Computational claim gate](#computational-claim-gate-thin-mc), and [CHANGELOG.md](CHANGELOG.md).

---

## What this paper does

Synthetic Risk Transfers let banks offload credit risk to private funds while keeping the underlying loans on their books. A structural flaw arises when the same bank extends a credit line to the fund that buys its protection. The fund's ability to pay under stress depends on credit from the bank whose loans are defaulting. We call the fraction of protection funded this way λ.

We build a directed network model of bank-NBFI SRT relationships and simulate contagion cascades across 1,000 random network realizations per λ value. Main result: cascade risk is not linear in λ. It shows a two-stage transition, first departing from baseline at λ_onset ≈ 0.85–0.95, then jumping sharply at λ* ≈ 0.95. The transition *location* is invariant across network density, investor concentration, shock size, and tranche thickness. What density does control is cascade *magnitude* beyond the threshold, from 0.18 at low density to 0.61 at high density.

We also propose six publicly observable proxy metrics, no Bloomberg required, ranked by sensitivity-weighted ordinal position relative to λ*. As of Q1 2026, four of six are red.

---

## Quickstart

```bash
git clone https://github.com/chokmah-me/srt-circular-leverage
cd srt-circular-leverage
pip install -r requirements.txt

# 1) Claim gate first (~10s): λ_onset / λ* location, two-stage order, nonlinearity
#    Exit 0 = load-bearing sim claims still hold under thin MC (not full 1000-run sweep)
python verify_srt_claims.py

# 2) Full run (publication quality, ~5 min)
python srt_simulation.py

# 3) Fast development run (~30 sec) — figures only, no claim asserts
python srt_simulation.py --quick
```

Gate evidence lands in `results/` (`claim_verify_meta.json`, `srt_claim_verify.json`, brief).  
Simulation outputs land in `figures/`:
- `fig1_phase_transition.pdf` — main result
- `fig2_distributions.pdf` — Dragon King vs power-law tail
- `fig3_sensitivity.pdf` — investor concentration sensitivity
- `fig4_lppls_illustration.pdf` — synthetic LPPLS motivating figure (labeled synthetic)
- `fig5_density_sensitivity.pdf` — network density sensitivity (new)
- `cockpit_metrics.csv` — six proxy metrics with Q1 2026 readings

---

## Requirements

Python 3.10+. No proprietary data. No API keys.

```
numpy>=1.24
networkx>=3.0
matplotlib>=3.7
scipy>=1.10
```

---

## Repository structure

```
srt_simulation.py         # network builder, cascade engine, MC sweep, plots, main()
verify_srt_claims.py      # computational claim gate (thin MC) — NEW
claim-manifest.json       # claim-gate manifest (cd-claim-gate/v1) — NEW
results/                  # gate evidence + claim-holds brief — NEW
figures/                  # generated figures / cockpit CSV
dyb-2026k-circular-nw-risk-v1.md   # paper (Markdown source)
README.md
CHANGELOG.md
LICENSE
requirements.txt
CITATION.cff
```

---

## Computational claim gate (thin MC)

**What it is.** A fast, seeded harness that re-runs the paper’s *load-bearing simulation* claims and fails with a clear reason if they break. Prefer this after any edit to the cascade engine or sweep helpers.

**Checked (thin MC, seed 42, n_runs=80):**

- `lambda_actual` tracks requested λ; cascade size ∈ [0, 1]
- λ_onset and λ\* in high-λ bands (paper ≈ 0.85–0.95 / ≈ 0.95)
- two-stage order (onset ≤ star)
- high-λ cascade elevated vs baseline; jump concentrated at high λ

**Not checked:** full 1000-run publication sweep; density magnitude 0.18–0.61; multi-seed stability; cockpit *market* readings; LPPLS fits. Policy: `results/claim-holds-brief.md`. Changelog: [CHANGELOG.md](CHANGELOG.md).

```bash
# From this repo root (same deps as the sim)
python verify_srt_claims.py

# Or via computational-claim-gate (writes/refreshes results/claim_verify_*.{json,txt})
python path/to/computational-claim-gate/scripts/verify_claim_project.py --project .
```

Manifest: `claim-manifest.json` (claim id `srt-phase-transition`).
---

## Reproducing specific results

**Verify stability across seeds:**
```python
from srt_simulation import main
for seed in [42, 123, 999, 2026]:
    main(seed=seed, n_runs_sweep=500, out_dir=f'figures_seed_{seed}')
```

**Run simultaneous vs sequential cascade comparison:**
```python
from srt_simulation import build_network, run_cascade, sweep_lambda
import numpy as np

grid = np.linspace(0, 1, 21)
seq = sweep_lambda(lambda_grid=grid, n_runs=500, mode='sequential')
sim = sweep_lambda(lambda_grid=grid, n_runs=500, mode='simultaneous')
# seq and sim produce consistent phase transitions;
# simultaneous yields slightly larger cascades at high λ
```

**Inspect the cockpit CSV:**
```python
import csv
with open('figures/cockpit_metrics.csv') as f:
    for row in csv.DictReader(f):
        print(row['rank'], row['signal'], row['metric'])
```

---

## What this paper does NOT do

- Fit LPPLS parameters to real SRT issuance data
- Predict a critical time t_c
- Empirically estimate current market λ (it is not disclosed)
- Model central bank intervention or sovereign backstops

Figure 4 is synthetic and labeled as such. Do not treat it as a forecast.

---

## Citation

See `CITATION.cff` or use the Zenodo DOI. BibTeX:

```bibtex
@article{bilar2026piggybacking,
  title   = {Circular Leverage in
            Bank-NBFI Synthetic Risk Transfer Networks},
  author  = {Bilar, Daniyel Yaacov},
  year    = {2026},
  journal = {Zenodo preprint},
  doi     = {10.5281/zenodo.19632278}
}
```

---

## License

Code: MIT. Paper text: CC BY 4.0. See `LICENSE`.
