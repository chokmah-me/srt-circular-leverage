#!/usr/bin/env python3
"""
Computational claim gate for circular-networks-SRT-networks.

Load-bearing *simulation* claims from the preprint (dyb-2026k):
  - cascade risk is nonlinear in λ (two-stage transition)
  - λ* (cliff) sits near 0.95; λ_onset in the high-λ band
  - network builder approximately realizes requested λ

This is a thin Monte Carlo harness (reduced n_runs), not the publication
sweep (1000 runs). Full multi-seed invariance and density magnitude
scaling (0.18–0.61) are non-claims here — re-run srt_simulation.py for those.

Exit 0 iff all checks pass. Prints why each check fails.
Seeded; no hidden RNG.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

import srt_simulation as s

# ---------------------------------------------------------------------------
# Gate policy (recorded in results metadata when run under claim gate)
# ---------------------------------------------------------------------------
SEED = 42
N_RUNS = 80  # thin gate; paper uses 1000
SHOCK = 0.05
GRID = np.linspace(0.0, 1.0, 21)

# Tolerances: wider than paper prose to absorb MC noise at N_RUNS=80.
# Paper: λ_onset ≈ 0.85–0.95, λ* ≈ 0.95 (grid step 0.05).
ONSET_LO, ONSET_HI = 0.75, 0.95
STAR_LO, STAR_HI = 0.90, 1.00
# High-λ mean cascade must clearly exceed baseline
MIN_HIGH_OVER_BASE = 1.8
# Largest adjacent jump must dominate early (λ < 0.5) jumps
MIN_JUMP_RATIO = 4.0
# lambda_actual vs requested |error| for a single draw (approx enforcement)
LAMBDA_ACTUAL_TOL = 0.12

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def _fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def _ok(msg: str) -> None:
    print(f"OK:   {msg}")


def check_structural() -> dict:
    """Network builder + cascade API invariants (no large MC)."""
    rng = np.random.default_rng(SEED)
    report: dict = {"checks": []}

    for target in (0.0, 0.5, 0.95, 1.0):
        G = s.build_network(lam=target, rng=rng)
        actual = float(G.graph.get("lambda_actual", float("nan")))
        if not np.isfinite(actual):
            _fail(f"lambda_actual missing for target λ={target}")
        err = abs(actual - target)
        # At λ=0 exact zero is expected; elsewhere approximate
        tol = 1e-9 if target == 0.0 else LAMBDA_ACTUAL_TOL
        if err > tol:
            _fail(
                f"lambda_actual off target: target={target:.2f} "
                f"actual={actual:.3f} |err|={err:.3f} > tol={tol}"
            )
        res = s.run_cascade(G, shock_size=SHOCK, rng=rng)
        if "cascade_size" not in res:
            _fail("run_cascade missing cascade_size")
        cs = float(res["cascade_size"])
        if not (0.0 <= cs <= 1.0 + 1e-9):
            _fail(f"cascade_size out of [0,1]: {cs}")
        report["checks"].append(
            {"lam_target": target, "lam_actual": actual, "cascade_size": cs}
        )
        _ok(f"structure λ_target={target:.2f} actual={actual:.3f} cascade={cs:.4f}")

    report["ok"] = True
    return report


def check_phase_transition() -> dict:
    """
    Thin Monte Carlo: two-stage transition location and nonlinearity.

    Paper claims (computational, not proof):
      λ_onset ≈ 0.85–0.95, λ* ≈ 0.95; jump is concentrated at high λ.
    """
    rng = np.random.default_rng(SEED)
    s.RNG = rng  # module default if any path omits rng=

    t0 = time.perf_counter()
    sw = s.sweep_lambda(
        lambda_grid=GRID,
        n_runs=N_RUNS,
        shock_size=SHOCK,
        rng=rng,
    )
    elapsed = time.perf_counter() - t0

    lam = sw["lambda_grid"]
    mu = sw["mean_cascade"]
    sd = sw["std_cascade"]
    lonset = float(s._find_lambda_onset(lam, mu, sd, k=2.0))
    lstar = float(s._find_lambda_star(lam, mu))
    diffs = np.diff(mu)
    max_jump = float(diffs.max())
    early_max = float(diffs[:10].max())  # λ steps in [0, 0.5]
    mu0 = float(mu[0])
    mu1 = float(mu[-1])

    print(
        f"[phase] seed={SEED} n_runs={N_RUNS} shock={SHOCK} "
        f"elapsed={elapsed:.1f}s"
    )
    print(
        f"[phase] λ_onset={lonset:.2f}  λ*={lstar:.2f}  "
        f"μ(0)={mu0:.4f}  μ(1)={mu1:.4f}  "
        f"max_jump={max_jump:.4f}  early_max_jump={early_max:.4f}"
    )

    if not (ONSET_LO <= lonset <= ONSET_HI):
        _fail(
            f"λ_onset={lonset:.2f} outside gate band [{ONSET_LO}, {ONSET_HI}] "
            f"(paper ≈ 0.85–0.95; thin MC may shift slightly)"
        )
    _ok(f"λ_onset={lonset:.2f} in [{ONSET_LO}, {ONSET_HI}]")

    if not (STAR_LO <= lstar <= STAR_HI):
        _fail(
            f"λ*={lstar:.2f} outside gate band [{STAR_LO}, {STAR_HI}] "
            f"(paper ≈ 0.95)"
        )
    _ok(f"λ*={lstar:.2f} in [{STAR_LO}, {STAR_HI}]")

    if lonset > lstar + 1e-9:
        _fail(f"two-stage order broken: onset {lonset:.2f} > star {lstar:.2f}")
    _ok(f"onset ≤ star ({lonset:.2f} ≤ {lstar:.2f})")

    if mu0 <= 0:
        ratio = float("inf") if mu1 > 0 else 0.0
    else:
        ratio = mu1 / mu0
    if ratio < MIN_HIGH_OVER_BASE:
        _fail(
            f"high-λ cascade not elevated enough: μ(1)/μ(0)={ratio:.3f} "
            f"< {MIN_HIGH_OVER_BASE} (μ0={mu0:.4f} μ1={mu1:.4f})"
        )
    _ok(f"μ(1)/μ(0)={ratio:.3f} ≥ {MIN_HIGH_OVER_BASE}")

    if early_max <= 0:
        jump_ratio = float("inf") if max_jump > 0 else 0.0
    else:
        jump_ratio = max_jump / early_max
    if jump_ratio < MIN_JUMP_RATIO:
        _fail(
            f"nonlinearity weak: max_jump/early_max={jump_ratio:.3f} "
            f"< {MIN_JUMP_RATIO} (max={max_jump:.4f} early={early_max:.4f})"
        )
    _ok(f"max_jump/early_max={jump_ratio:.3f} ≥ {MIN_JUMP_RATIO}")

    return {
        "ok": True,
        "seed": SEED,
        "n_runs": N_RUNS,
        "shock_size": SHOCK,
        "elapsed_sec": round(elapsed, 3),
        "lambda_onset": lonset,
        "lambda_star": lstar,
        "mean_cascade_lambda0": mu0,
        "mean_cascade_lambda1": mu1,
        "max_adjacent_jump": max_jump,
        "early_max_adjacent_jump": early_max,
        "high_over_base_ratio": ratio,
        "jump_ratio": jump_ratio,
        "policy": {
            "onset_band": [ONSET_LO, ONSET_HI],
            "star_band": [STAR_LO, STAR_HI],
            "min_high_over_base": MIN_HIGH_OVER_BASE,
            "min_jump_ratio": MIN_JUMP_RATIO,
        },
        "mean_cascade": [float(x) for x in mu],
        "lambda_grid": [float(x) for x in lam],
    }


def main() -> int:
    print("verify_srt_claims.py — computational claim gate (thin MC)")
    print(f"seed={SEED} n_runs={N_RUNS} (paper full sweep uses 1000)")
    print("non-claims: density magnitude 0.18–0.61, multi-seed stability,")
    print("            cockpit Q1-2026 market readings, LPPLS fit")
    print()

    structural = check_structural()
    print()
    phase = check_phase_transition()

    RESULTS.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "srt-claim-verify/v1",
        "ok": True,
        "seed": SEED,
        "n_runs_gate": N_RUNS,
        "structural": structural,
        "phase_transition": phase,
    }
    out = RESULTS / "srt_claim_verify.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print()
    print(f"wrote {out}")
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError:
        raise SystemExit(1)
