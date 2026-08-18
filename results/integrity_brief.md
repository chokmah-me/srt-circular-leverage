# Integrity brief — circular-networks-SRT-networks

## Status
`circular-networks-SRT-networks — limited (I1 limited empirical-coding; I3 pass online (6 resolved, 0 unresolved))`

Pinned draft: `dyb-2026k-circular-nw-risk-v2.md`. Not scientifically Verified. Not peer review.

## Reproduce
```
python C:/Users/Elke Shayna/Documents/00Dev/manuscript-integrity-gate/scripts/audit_manuscript.py --project . --manuscript dyb-2026k-circular-nw-risk-v2.md --propose-bindings
python C:/Users/Elke Shayna/Documents/00Dev/manuscript-integrity-gate/scripts/audit_manuscript.py --project . --manuscript dyb-2026k-circular-nw-risk-v2.md --online
python verify_srt_claims.py
```

## Surfaces
- Manuscript: `dyb-2026k-circular-nw-risk-v2.md`
- Manifest: `integrity-manifest.json`
- Bibliography: none (author–year + markdown References with URLs/DOIs)
- Results: `results/publication_sweep_summary.json`, `results/model_parameters.json`, `results/srt_claim_verify.json`, `results/osberghaus_passage_check.md`
- Code: `srt_simulation.py`, `verify_srt_claims.py`

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| I1 numbers | limited | 56 result-claims; 0 unbound. Cited percents are empirical-coding. Publication 95 / 18 / 61 bound to the n=1000 sweep summary, not the n=80 gate. |
| I2 protocol | limited | “re-ran” = `python srt_simulation.py`. Thin CCG re-ran 2026-08-18: **pass** (λ_onset=0.90, λ*=0.95, μ(1)/μ(0)=3.68). CCG still does not underwrite §5.5.1. |
| I3 references | **pass (online)** | 6 Crossref DOIs resolved, 0 unresolved. Official-report URLs (BIS, BCBS, FSB, ECB BLS, Machado, Boston Fed, Osberghaus PDF) have no Crossref DOI and were not existence-checked by the resolver. |
| I4 method–artifact | limited (same algorithm class) | Named files exist. Cascade rules match `run_cascade`. |
| I5 overclaim | warn | Lexicon “first” / “First”. |

## Blocking
none remaining

## Residual pass (2026-08-18)

1. **DOIs / URLs on References.** Added Crossref-resolving DOIs for Filimonov 2013, IMF WP/25/200, IMF WP/26/23, Sornette 2003 (ebook), Sornette & Ouillon 2012, Wosnitza & Sornette 2015. Official landing URLs for BIS QR Mar 2026, BCBS d607, ECB BLS Apr 2026, FSB May 2026, Machado 24 Mar 2026, Boston Fed CPP 26-6, Osberghaus WP 3210 PDF. ECB PDF metadata DOI `10.2866/9337769` is a live Handle but **not** in Crossref — left out of the draft so `--online` would not false-fail it.
2. **Osberghaus passage check.** 57–66%, ~26% (attribution-conditional), 15% median junior tranche, 12–25% / 35% / 70% monitoring, 60bn→300bn, 35 banks / 10%, 70% transfer-probability at the SME-factor jump: **match**. See `results/osberghaus_passage_check.md`.
3. **Support repairs.** Monitoring “12 to 28%” → “12–25%” (source p. 7). “mid-2024 / over 300bn” → “end-2024 / 300bn”. Removed the unfound “asymmetric deterioration vs improvement” sentence. Garbled “Sandomenico et al. 2015” → Wosnitza and Sornette (2015), DOI 10.1140/epjb/e2015-50019-9.
4. **Thin CCG.** `python verify_srt_claims.py` exit 0.
5. **CITATION.cff.** Placeholder `https://doi.org/[Zenodo DOI upon deposit]` → `https://doi.org/10.5281/zenodo.19632278`.

## WARN
- I3 `author_year_unindexed` (no `.bib`; month tokens `April 2026` etc. are scanner false positives).
- Cockpit Q2/Q3 color calls and most press snapshots still have no file in this repo.
- FSB $1.5–2.0T and BIS €800bn / 5× were not passage-checked this pass.
- “First academic study” is the authors’ own claim (also on the SUERF brief).
- Do not bind publication μ(1)=0.294 to `srt_claim_verify.json` (n=80, μ(1)=0.313).

## Not checked
Novelty, live 1,000-run re-run this pass, Lean, cockpit press primary sources, FSB/BIS numeric passage check.

## Evidence
- `results/integrity_audit.json`
- `results/unbound_result_claims.md`
- `results/osberghaus_passage_check.md`
- `results/srt_claim_verify.json`

## Residual (still open)
- [ ] Passage-check BIS €800bn / 5× and FSB $1.5–2.0T
- [ ] Cockpit Q2/Q3 readings still have no archived snapshot file
- [ ] Full `python srt_simulation.py` not re-run this pass (defaults unchanged; summary JSON from last publication run still current)
- [ ] Release-sync beyond the CFF URL (README badges, ZENODO.md, site catalog) — not started
- [ ] `CITATION.cff` `preferred-citation` YAML nesting still looks malformed
