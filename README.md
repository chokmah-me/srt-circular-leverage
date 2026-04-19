# Circular Leverage in Bank-NBFI SRT Networks

**Preprint:** [[Zenodo DOI — add upon deposit] ](https://zenodo.org/records/19632278) 
**License:** MIT (code) · CC BY 4.0 (paper)  
**Status:** Preprint, April 2026

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

# Full run (publication quality, ~5 min)
python srt_simulation.py

# Fast development run (~30 sec)
python srt_simulation.py --quick
```

Outputs land in `figures/`:
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
srt_simulation.py     # all code: network builder, cascade engine,
                      # Monte Carlo sweep, plots, proxy metrics, main()
srt_paper.md          # paper (Markdown source)
figures/              # generated output (created on first run)
README.md
LICENSE
requirements.txt
CITATION.cff
```

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
  doi     = {[DOI upon deposit]}
}
```

---

## License

Code: MIT. Paper text: CC BY 4.0. See `LICENSE`.
