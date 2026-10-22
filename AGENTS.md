# AGENTS.md — srt-circular-leverage

Phase-transition sims for circular leverage in bank–NBFI SRT networks. When banks fund the NBFIs that buy their SRT protection, capital relief is partly self-funded.

## Commands

```powershell
pip install -r requirements.txt
python verify_srt_claims.py          # ~10s claim gate (load-bearing)
python srt_simulation.py             # full publication run (~5 min)
python srt_simulation.py --quick     # figures only, no claim asserts
python plot_metric2_sparkline.py
```

Python 3.10+. No API keys. Gate evidence in `results/`; figures in `figures/`.

## Work rules

- Branch `v2.1` is the working paper draft; `master` is published v2. Do not merge `v2.1` without the user's word.
- `[VERIFY]` tags in the draft are open items, not decoration; do not silently resolve them.
- `verify_srt_claims.py` is thin MC (see `claim-manifest.json`). It is not the 1000-run publication sweep.

## Pointers

- `README.md` — quickstart, DOI, cockpit metrics
- `claim-manifest.json` — executable claim
- `ROBUSTNESS_CHECK_dyb-2026k-v2.md` — frozen stress surface
- `CITATION.cff` / `ZENODO.md` — cite / DOI map
