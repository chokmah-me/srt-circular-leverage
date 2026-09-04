"""
Circular Leverage in Bank-NBFI SRT Networks
Simulation code. MIT License.

Copyright (c) 2026 Daniyel Yaacov Bilar, Chokmah LLC
ORCID: 0000-0002-9040-6914
Contact: chokmah-dyb@pm.me

Sections:
  1. Network builder         (this section)
  2. Cascade engine          (next)
  3. Lambda sweep / Monte Carlo
  4. Plots
  5. Proxy metrics + main
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.stats import powerlaw
from collections import defaultdict
import csv, json, os, textwrap

# ---------------------------------------------------------------------------
# Global RNG — set seed here for reproducibility; pass rng= to override
# ---------------------------------------------------------------------------
DEFAULT_SEED = 42
RNG = np.random.default_rng(DEFAULT_SEED)


# ---------------------------------------------------------------------------
# SECTION 1: Network builder
# ---------------------------------------------------------------------------

def build_network(
    n_banks: int = 10,
    n_funds: int = 20,
    lam: float = 0.3,
    kappa: float = 0.75,
    tranche_thickness: float = 0.08,
    density: float = 2.0,
    rng: np.random.Generator = None,
) -> nx.DiGraph:
    """
    Build a directed bank-NBFI SRT network.

    Nodes
    -----
    Banks  : id 0 .. n_banks-1,  attr type='bank'
    Funds  : id n_banks .. n_banks+n_funds-1,  attr type='fund'

    Edges
    -----
    protection  : fund -> bank, weight = notional protected (fraction of bank's RWA)
                  attr: kind='protection'
    credit_line : bank -> fund, weight = credit extended
                  attr: kind='credit_line', self_funded=True/False

    Parameters
    ----------
    lam              : target self-funding fraction λ. Fraction of total protection
                       weight that is funded by the originating bank's own credit lines.
    kappa            : investor concentration. Top-kappa fraction of funds hold
                       (1 - small_share) of total protection weight.
    tranche_thickness: first-loss tranche as fraction of reference portfolio (δ).
    rng              : numpy Generator; uses module-level RNG if None.

    Returns
    -------
    nx.DiGraph with node/edge attributes set.

    Notes
    -----
    λ is enforced approximately: we flag self_funded edges until their cumulative
    weight / total protection weight >= lam. Exact λ is stored as graph attr
    G.graph['lambda_actual'].
    """
    if rng is None:
        rng = RNG

    G = nx.DiGraph()

    bank_ids = list(range(n_banks))
    fund_ids = list(range(n_banks, n_banks + n_funds))

    # --- Add nodes ---
    for b in bank_ids:
        G.add_node(b, type='bank', solvent=True, rwa_relief=0.0,
                   capital_shortfall=0.0)
    for f in fund_ids:
        G.add_node(f, type='fund', solvent=True, leverage=0.0,
                   protection_notional=0.0)

    # --- Protection edges (fund -> bank) ---
    # Concentration: top kappa*n_funds funds hold most of the exposure.
    # We assign protection weights from a Pareto-like distribution then normalize.
    raw_weights = rng.exponential(scale=1.0, size=n_funds)
    # Enforce concentration: boost top ceil(kappa * n_funds) funds
    n_top = max(1, int(np.ceil(kappa * n_funds)))
    top_idx = np.argsort(raw_weights)[-n_top:]
    raw_weights[top_idx] *= (1.0 / kappa)          # amplify top funds
    raw_weights /= raw_weights.sum()               # normalize to sum=1

    # Each fund connects to a random number of banks around the target `density`.
    # density = expected bank-connections per fund. Higher density = more
    # alternative-financing redundancy = fewer bottlenecks when one bank calls lines.
    # Supported range: 1.0 (single-bank funds) to ~n_banks-1 (highly redundant).
    protection_per_fund = raw_weights   # shape (n_funds,)

    for i, f in enumerate(fund_ids):
        # Draw connections count from a Poisson-like distribution centered on density;
        # clamp to [1, n_banks].
        n_raw = max(1, int(rng.poisson(density)))
        n_connections = int(min(n_raw, n_banks))
        target_banks = rng.choice(bank_ids, size=n_connections, replace=False)
        # Split this fund's weight across its target banks
        split = rng.dirichlet(np.ones(n_connections))
        for b, s in zip(target_banks, split):
            w = float(protection_per_fund[i] * s)
            if G.has_edge(f, b):
                G[f][b]['weight'] += w
            else:
                G.add_edge(f, b, kind='protection', weight=w,
                           self_funded=False)

        G.nodes[f]['protection_notional'] = float(protection_per_fund[i])

    # --- Credit line edges (bank -> fund), enforcing λ ---
    # Strategy: sort protection edges by weight descending; flag as self_funded
    # until cumulative flagged weight / total >= lam.
    total_protection = sum(
        d['weight'] for _, _, d in G.edges(data=True) if d['kind'] == 'protection'
    )

    # Build list of (fund, bank, weight) for protection edges, sorted by weight desc
    prot_edges = sorted(
        [(f, b, G[f][b]['weight'])
         for f, b, d in G.edges(data=True) if d['kind'] == 'protection'],
        key=lambda x: x[2], reverse=True
    )

    cumulative_self = 0.0
    for f, b, w in prot_edges:
        is_self = cumulative_self / total_protection < lam
        G[f][b]['self_funded'] = is_self
        # Add corresponding credit line edge bank -> fund
        G.add_edge(b, f, kind='credit_line', weight=w * 1.1,  # slight leverage
                   self_funded=is_self)
        if is_self:
            cumulative_self += w

    # Store params on graph
    lambda_actual = cumulative_self / total_protection if total_protection > 0 else 0.0
    G.graph.update({
        'n_banks': n_banks,
        'n_funds': n_funds,
        'lambda_target': lam,
        'lambda_actual': lambda_actual,
        'kappa': kappa,
        'tranche_thickness': tranche_thickness,
        'density': density,
        'bank_ids': bank_ids,
        'fund_ids': fund_ids,
    })

    return G


# ---------------------------------------------------------------------------
# SECTION 2: Cascade engine
# ---------------------------------------------------------------------------

def run_cascade(
    G: nx.DiGraph,
    shock_size: float = 0.05,
    mode: str = 'sequential',
    rng: np.random.Generator = None,
) -> dict:
    """
    Simulate a contagion cascade on the SRT network.

    Shock
    -----
    A fraction `shock_size` of total protection weight defaults simultaneously
    at t=0, hitting the largest fund first (most realistic: concentrated shock
    on the most exposed player triggers the cascade).

    Failure conditions
    ------------------
    Fund fails  : cumulative loss > protection_notional * tranche_thickness
    Bank distressed : RWA relief lost from failed funds > bank's capital buffer
                      (approximated as 8% of total protection weight it holds)

    Circular leverage channel
    -------------------------
    When a bank becomes distressed it calls in credit lines to self-funded funds.
    Called credit line = fund must find replacement funding immediately.
    If fund cannot (no solvent alternative bank credit line exists), fund fails.

    Parameters
    ----------
    G          : network from build_network(); NOT modified in place — we work
                 on a copy.
    shock_size : fraction of total protection weight that defaults at t=0.
    mode       : 'sequential' (default, random order within each round) or
                 'simultaneous' (all updates computed before any applied).
    rng        : numpy Generator.

    Returns
    -------
    dict with keys:
        failed_funds      : set of fund node ids that failed
        distressed_banks  : set of bank node ids that became distressed
        cascade_size      : (len(failed_funds) + len(distressed_banks)) /
                            total nodes  — fraction of network that failed
        n_rounds          : number of propagation rounds until quiescence
        lambda_actual     : λ of the network
        initial_shock     : shock_size used
    """
    if rng is None:
        rng = RNG

    # Work on state dicts, not the graph itself, to avoid mutation
    tranche = G.graph['tranche_thickness']
    bank_ids = G.graph['bank_ids']
    fund_ids = G.graph['fund_ids']
    total_nodes = len(bank_ids) + len(fund_ids)

    # State
    fund_loss    = {f: 0.0 for f in fund_ids}   # cumulative loss absorbed
    fund_failed  = {f: False for f in fund_ids}
    bank_relief  = {b: 0.0  for b in bank_ids}  # RWA relief lost so far
    bank_dist    = {b: False for b in bank_ids}  # distressed flag
    called_lines = set()                          # (bank, fund) credit lines called

    # Fund capital buffer: protection_notional * tranche_thickness
    fund_buffer = {
        f: G.nodes[f]['protection_notional'] * tranche
        for f in fund_ids
    }

    # Bank capital buffer: bank becomes distressed when it loses > 20% of its
    # total SRT-derived RWA relief. This is the paper's key threshold assumption.
    # Rationale: losing 20% of capital relief forces a bank to either raise capital
    # or call in credit lines — both trigger the circular leverage channel.
    BANK_DISTRESS_THRESHOLD = 0.20
    bank_buffer = {}
    for b in bank_ids:
        total_prot = sum(
            G[f][b]['weight']
            for f in G.predecessors(b)
            if G[f][b].get('kind') == 'protection'
        )
        bank_buffer[b] = total_prot * BANK_DISTRESS_THRESHOLD

    # --- t=0 shock: hit largest fund proportionally to shock_size ---
    total_prot_weight = sum(
        G.nodes[f]['protection_notional'] for f in fund_ids
    )
    shock_total = shock_size * total_prot_weight

    # Sort funds by notional descending; distribute shock_total across top funds
    # until exhausted (realistic: correlated shock hits most exposed first)
    sorted_funds = sorted(fund_ids,
                          key=lambda f: G.nodes[f]['protection_notional'],
                          reverse=True)
    remaining_shock = shock_total
    initial_failures = []
    for f in sorted_funds:
        if remaining_shock <= 0:
            break
        hit = min(remaining_shock, G.nodes[f]['protection_notional'])
        fund_loss[f] += hit
        remaining_shock -= hit
        if fund_loss[f] > fund_buffer[f]:
            fund_failed[f] = True
            initial_failures.append(f)

    # --- Propagation rounds ---
    n_rounds = 0
    max_rounds = total_nodes + 5

    def _apply_fund_failure(f):
        """Propagate a single fund failure to its bank counterparties."""
        for b in G.successors(f):
            if G[f][b].get('kind') != 'protection':
                continue
            if bank_dist[b]:
                continue
            bank_relief[b] += G[f][b]['weight']
            if bank_relief[b] > bank_buffer[b]:
                bank_dist[b] = True

    def _apply_bank_distress(b):
        """Distressed bank calls in self-funded credit lines."""
        for f in G.successors(b):
            if G[b][f].get('kind') != 'credit_line':
                continue
            if not G[b][f].get('self_funded'):
                continue
            if fund_failed[f]:
                continue
            called_lines.add((b, f))
            has_alternative = any(
                G[b2][f].get('kind') == 'credit_line'
                and not G[b2][f].get('self_funded')
                and not bank_dist[b2]
                for b2 in G.predecessors(f)
                if b2 != b
            )
            if not has_alternative:
                fund_failed[f] = True

    # Propagate t=0 failures to banks before the main loop
    for f in initial_failures:
        _apply_fund_failure(f)
    # If any bank became distressed from initial failures, propagate its calls
    for b in list(bank_ids):
        if bank_dist[b]:
            _apply_bank_distress(b)

    while n_rounds < max_rounds:
        n_rounds += 1

        if mode == 'simultaneous':
            # Snapshot current failure sets; compute all updates; apply at once
            new_fund_failures = [
                f for f in fund_ids
                if not fund_failed[f] and fund_loss[f] > fund_buffer[f]
            ]
            new_bank_distress = []

            for f in new_fund_failures:
                fund_failed[f] = True
            for f in new_fund_failures:
                for b in G.successors(f):
                    if G[f][b].get('kind') != 'protection' or bank_dist[b]:
                        continue
                    bank_relief[b] += G[f][b]['weight']
            for b in bank_ids:
                if not bank_dist[b] and bank_relief[b] > bank_buffer[b]:
                    new_bank_distress.append(b)
            for b in new_bank_distress:
                bank_dist[b] = True
            for b in new_bank_distress:
                _apply_bank_distress(b)

            if not new_fund_failures and not new_bank_distress:
                break

        else:  # sequential (default)
            changed = False
            # Randomize processing order each round
            order_funds = rng.permutation(fund_ids).tolist()
            order_banks = rng.permutation(bank_ids).tolist()

            for f in order_funds:
                if not fund_failed[f] and fund_loss[f] > fund_buffer[f]:
                    fund_failed[f] = True
                    _apply_fund_failure(f)
                    changed = True

            for b in order_banks:
                if not bank_dist[b] and bank_relief[b] > bank_buffer[b]:
                    bank_dist[b] = True
                    _apply_bank_distress(b)
                    changed = True

            # Second fund pass: catch failures triggered by bank distress this round
            for f in order_funds:
                if not fund_failed[f] and fund_loss[f] > fund_buffer[f]:
                    fund_failed[f] = True
                    _apply_fund_failure(f)
                    changed = True

            if not changed:
                break

    failed_funds     = {f for f, v in fund_failed.items() if v}
    distressed_banks = {b for b, v in bank_dist.items() if v}
    cascade_size     = (len(failed_funds) + len(distressed_banks)) / total_nodes

    return {
        'failed_funds':     failed_funds,
        'distressed_banks': distressed_banks,
        'cascade_size':     cascade_size,
        'n_rounds':         n_rounds,
        'lambda_actual':    G.graph['lambda_actual'],
        'initial_shock':    shock_size,
    }


# ---------------------------------------------------------------------------
# SECTION 3: Lambda sweep / Monte Carlo
# ---------------------------------------------------------------------------

def sweep_lambda(
    lambda_grid: np.ndarray = None,
    n_runs: int = 1000,
    n_banks: int = 10,
    n_funds: int = 20,
    kappa: float = 0.75,
    tranche_thickness: float = 0.08,
    density: float = 2.0,
    shock_size: float = 0.05,
    mode: str = 'sequential',
    rng: np.random.Generator = None,
) -> dict:
    """
    Monte Carlo sweep over λ values.
    For each λ, builds n_runs independent random networks and runs a cascade.

    Returns
    -------
    dict: lambda_grid, mean_cascade, std_cascade, all_cascades (full distributions)
    """
    if rng is None:
        rng = RNG
    if lambda_grid is None:
        lambda_grid = np.linspace(0.0, 1.0, 21)

    mean_cascade = np.zeros(len(lambda_grid))
    std_cascade  = np.zeros(len(lambda_grid))
    all_cascades = []

    for i, lam in enumerate(lambda_grid):
        sizes = np.zeros(n_runs)
        for j in range(n_runs):
            G = build_network(n_banks, n_funds, lam=lam, kappa=kappa,
                              tranche_thickness=tranche_thickness,
                              density=density, rng=rng)
            res = run_cascade(G, shock_size=shock_size, mode=mode, rng=rng)
            sizes[j] = res['cascade_size']
        mean_cascade[i] = sizes.mean()
        std_cascade[i]  = sizes.std()
        all_cascades.append(sizes)

    return {
        'lambda_grid':  lambda_grid,
        'mean_cascade': mean_cascade,
        'std_cascade':  std_cascade,
        'all_cascades': all_cascades,
    }


def sweep_kappa_sensitivity(
    lambda_grid: np.ndarray = None,
    kappa_values: list = None,
    n_runs: int = 500,
    **kwargs,
) -> dict:
    """Sweep over multiple kappa values for sensitivity analysis (§5.3)."""
    if lambda_grid is None:
        lambda_grid = np.linspace(0.0, 1.0, 21)
    if kappa_values is None:
        kappa_values = [0.40, 0.75, 0.98]
    return {
        k: sweep_lambda(lambda_grid=lambda_grid, n_runs=n_runs, kappa=k, **kwargs)
        for k in kappa_values
    }


def sweep_density_sensitivity(
    lambda_grid: np.ndarray = None,
    density_values: list = None,
    n_runs: int = 500,
    **kwargs,
) -> dict:
    """
    Sweep over network density values (§5.4).
    Density = expected bank-connections per fund.
    Tests whether alternative-financing redundancy changes λ*.
    """
    if lambda_grid is None:
        lambda_grid = np.linspace(0.0, 1.0, 21)
    if density_values is None:
        density_values = [1.0, 2.0, 3.0, 5.0]
    # Remove density from kwargs if present to avoid double-pass
    kwargs.pop('density', None)
    return {
        d: sweep_lambda(lambda_grid=lambda_grid, n_runs=n_runs, density=d, **kwargs)
        for d in density_values
    }


# ---------------------------------------------------------------------------
# SECTION 4: Plots (Tufte style)
# ---------------------------------------------------------------------------

# Colorblind-safe (Okabe–Ito). Pair with linestyles so prints survive grayscale.
C_BLUE   = '#0072B2'
C_VERM   = '#D55E00'
C_GRAY   = '#666666'
C_GREEN  = '#009E73'
C_ORANGE = '#E69F00'
C_SKY    = '#56B4E9'
C_INK    = '#222222'

_REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def _tufte_ax(ax):
    """Strip to bare minimum: bottom + left spines only, no top/right."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.6)
    ax.spines['bottom'].set_linewidth(0.6)
    ax.tick_params(length=3, width=0.6, labelsize=8)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')


def _reading_guide(fig, text: str, *, x: float = 0.10, width: int = 92) -> None:
    """Place the reading guide fully inside the figure (never below y=0).

    Use va='bottom' near the lower margin so wrapped lines grow upward into the
    reserved footer band instead of clipping off the saved PNG/PDF.
    """
    fig.text(
        x, 0.025,
        textwrap.fill(text, width=width),
        fontsize=6.5, color='#555555', ha='left', va='bottom',
        linespacing=1.2,
    )


def _n_runs(sweep_result: dict) -> int:
    cascades = sweep_result.get('all_cascades')
    if cascades is None or len(cascades) == 0:
        return 0
    return int(len(cascades[0]))


def _save_fig(fig, stem: str, out_dir: str) -> str:
    """Save PDF + PNG at 300 dpi. Sync PNG to repo root when writing to figures/."""
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, f'{stem}.pdf')
    png_path = os.path.join(out_dir, f'{stem}.png')
    fig.savefig(pdf_path, dpi=300, bbox_inches='tight')
    fig.savefig(png_path, dpi=300, bbox_inches='tight')
    if os.path.basename(os.path.normpath(out_dir)) == 'figures':
        fig.savefig(os.path.join(_REPO_ROOT, f'{stem}.png'), dpi=300,
                    bbox_inches='tight')
    return pdf_path


def _find_lambda_star(lambda_grid, mean_cascade):
    """
    Locate λ* as the point of maximum absolute increase between adjacent λ values.
    More robust than second-derivative for noisy Monte Carlo output.
    Interpretation: the 'Dragon King cliff' — where the sharpest jump sits.
    """
    diffs = np.diff(mean_cascade)
    return float(lambda_grid[np.argmax(diffs)])


def _find_lambda_onset(lambda_grid, mean_cascade, std_cascade, k: float = 2.0):
    """
    Locate λ_onset as the first λ where mean cascade exceeds baseline + k * baseline_SD.
    Interpretation: 'first departure from normal' — an earlier, softer threshold
    than λ* (the cliff). Together they bracket the transition zone.
    """
    thresh = mean_cascade[0] + k * std_cascade[0]
    for i, m in enumerate(mean_cascade):
        if m > thresh:
            return float(lambda_grid[i])
    return float(lambda_grid[-1])


def plot_phase_transition(sweep_result: dict, out_dir: str = 'figures') -> str:
    """
    Figure 1: Phase transition — mean cascade size ± 1 SD vs λ.
    Marks the two-stage threshold (λ_onset, λ*) and the λ=0 / λ=1 levels.
    """
    lam   = sweep_result['lambda_grid']
    mu    = sweep_result['mean_cascade']
    sd    = sweep_result['std_cascade']
    lstar = _find_lambda_star(lam, mu)
    lonset = _find_lambda_onset(lam, mu, sd, k=2.0)
    n     = _n_runs(sweep_result)

    # Reserved title / panel / footer bands (avoid label bleed + tight-crop fights)
    fig = plt.figure(figsize=(5.6, 3.8))
    ax = fig.add_axes([0.14, 0.22, 0.82, 0.62])
    _tufte_ax(ax)

    ax.fill_between(lam, np.clip(mu - sd, 0, None), mu + sd,
                    color=C_BLUE, alpha=0.12, linewidth=0, zorder=1)
    ax.plot(lam, mu, color=C_BLUE, linewidth=1.4, solid_capstyle='round', zorder=2)
    ax.axhline(mu[0], color=C_GRAY, linewidth=0.5, linestyle='--', zorder=0)

    # Transition window [λ_onset, λ*] — the two-stage claim
    ax.axvspan(lonset, lstar, color='#999999', alpha=0.10, linewidth=0, zorder=0)
    ax.axvline(lonset, color=C_GRAY, linewidth=0.6, linestyle=':', zorder=1)
    ax.axvline(lstar,  color=C_VERM, linewidth=0.7, linestyle=':', zorder=1)

    # Threshold labels in the top margin of the axes (not on the curve)
    y_hi = max((mu + sd).max() * 1.04, mu.max() + 0.04)
    ax.set_ylim(0, y_hi)
    ax.text(lonset - 0.01, 0.97, rf'$\lambda_{{\mathrm{{onset}}}}\approx{lonset:.2f}$',
            transform=ax.get_xaxis_transform(),
            color=C_GRAY, fontsize=7, va='top', ha='right')
    ax.text(min(lstar + 0.01, 0.995), 0.97, rf'$\lambda^{{*}}\approx{lstar:.2f}$',
            transform=ax.get_xaxis_transform(),
            color=C_VERM, fontsize=7, va='top', ha='left')

    # Direct-label the two levels the text compares (≈3×)
    ax.text(0.012, mu[0] + 0.008, f'{mu[0]:.2f}',
            color=C_BLUE, fontsize=7, va='bottom', ha='left')
    ax.annotate(f'{mu[-1]:.2f}', xy=(1.0, mu[-1]),
                xytext=(-3, 5), textcoords='offset points',
                color=C_BLUE, fontsize=7, ha='right', va='bottom')

    ax.set_xlabel(r'self-funding fraction $\lambda$', fontsize=9, labelpad=6)
    ax.set_ylabel('mean cascade size\n(fraction of network)', fontsize=9, labelpad=6)
    ax.set_xlim(0, 1)
    ax.spines['left'].set_bounds(0, min(mu.max(), y_hi))
    ax.spines['bottom'].set_bounds(0, 1)

    fig.text(0.14, 0.92,
             r'Cascade risk stays near baseline, then jumps in two stages as '
             r'$\lambda$ rises',
             fontsize=9, color=C_INK, ha='left', va='top')
    _reading_guide(
        fig,
        f'Reading guide: the blue curve is average cascade size across {n} '
        r'simulated networks at each $\lambda$; the light band is run-to-run '
        r'spread ($\pm 1$ SD). The grey window marks the two-stage transition '
        r'(soft onset, then the cliff). Dashed line: baseline at $\lambda=0$.',
        x=0.14, width=95,
    )
    # Fixed bbox preserves reserved title/footer bands
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, 'fig1_phase_transition.pdf')
    png_path = os.path.join(out_dir, 'fig1_phase_transition.png')
    fig.savefig(pdf_path, dpi=300, bbox_inches=None)
    fig.savefig(png_path, dpi=300, bbox_inches=None)
    if os.path.basename(os.path.normpath(out_dir)) == 'figures':
        fig.savefig(os.path.join(_REPO_ROOT, 'fig1_phase_transition.png'),
                    dpi=300, bbox_inches=None)
    plt.close(fig)
    return pdf_path


def plot_cascade_distributions(sweep_result: dict, out_dir: str = 'figures') -> str:
    """
    Figure 2: Cascade-size distributions at λ_low, λ_mid, λ_high.
    Shared x-scale so Dragon King mass is visibly beyond the stable-regime support.
    Tufte devices: small multiples, rugs, reference line+band, direct labels,
    micro-table, sparkline linking snapshots to the λ path, range-frames.
    """
    lam_grid = np.asarray(sweep_result['lambda_grid'], dtype=float)
    cascades = sweep_result['all_cascades']
    mu_path = np.asarray(sweep_result['mean_cascade'], dtype=float)
    n_mc = _n_runs(sweep_result)

    n = len(lam_grid)
    idx_lo, idx_mid, idx_hi = 2, n // 2, n - 1
    picks = [
        (float(lam_grid[idx_lo]),  cascades[idx_lo],  'stable',      C_GRAY, idx_lo),
        (float(lam_grid[idx_mid]), cascades[idx_mid], 'mid',         C_SKY,  idx_mid),
        (float(lam_grid[idx_hi]),  cascades[idx_hi],  'Dragon King', C_VERM, idx_hi),
    ]

    xmax = max(float(np.max(data)) for _, data, _, _, _ in picks)
    xmax = max(xmax, 0.05)
    bin_edges = np.linspace(0, xmax, 31)
    p95_stable = float(np.percentile(picks[0][1], 95))

    # Per-panel summaries for micro-table + callouts
    rows = []
    for lv, data, tag, col, _ in picks:
        data = np.asarray(data, dtype=float)
        med = float(np.median(data))
        mean = float(np.mean(data))
        p95 = float(np.percentile(data, 95))
        frac_beyond = float(np.mean(data > p95_stable))
        rows.append(dict(lam=lv, tag=tag, col=col, med=med, mean=mean,
                         p95=p95, frac=frac_beyond, mx=float(data.max())))

    fig = plt.figure(figsize=(7.8, 5.2))
    # Bands: title | sparkline | panels | micro-table | footer
    ax_spark = fig.add_axes([0.10, 0.76, 0.86, 0.07])
    axes = []
    left, width, gap = 0.10, 0.26, 0.045
    for i in range(3):
        axes.append(fig.add_axes([left + i * (width + gap), 0.40, width, 0.28]))

    # --- Sparkline: mean cascade vs λ; dots mark the three panel snapshots ---
    _tufte_ax(ax_spark)
    ax_spark.plot(lam_grid, mu_path, color=C_BLUE, linewidth=1.1,
                  solid_capstyle='round', zorder=2)
    for lv, _, tag, col, idx in picks:
        ax_spark.plot(lv, mu_path[idx], 'o', color=col, markersize=5.5,
                      markeredgecolor='white', markeredgewidth=0.5, zorder=3)
    ax_spark.set_xlim(0, 1)
    y0, y1 = float(mu_path.min()), float(mu_path.max())
    pad = 0.08 * (y1 - y0 + 1e-9)
    ax_spark.set_ylim(y0 - pad, y1 + pad)
    ax_spark.spines['bottom'].set_bounds(0, 1)
    ax_spark.spines['left'].set_bounds(y0, y1)
    ax_spark.set_xticks([0, 0.5, 1.0])
    ax_spark.set_ylabel(r'$\mu$', fontsize=7, rotation=0, labelpad=8, va='center')
    ax_spark.tick_params(labelsize=6)
    fig.text(0.10, 0.845,
             r'Sparkline: mean cascade vs $\lambda$ (colored dots = the three panels)',
             fontsize=6.5, color='0.4', ha='left', va='bottom')

    # --- Small-multiple histograms ---
    hist_counts = []
    for ax, (lv, data, tag, col, _), row in zip(axes, picks, rows):
        _tufte_ax(ax)
        data = np.asarray(data, dtype=float)
        # Reference band: mass beyond stable p95 (the comparison that matters)
        if tag != 'stable':
            ax.axvspan(p95_stable, xmax, color=C_VERM, alpha=0.07, linewidth=0,
                       zorder=0)
        counts, _, _ = ax.hist(data, bins=bin_edges, color=col, alpha=0.82,
                               linewidth=0, zorder=2)
        hist_counts.append(counts)
        ax.axvline(p95_stable, color='#aaaaaa', linewidth=0.7, linestyle=':',
                   zorder=3)
        ax.axvline(row['med'], color=col, linewidth=1.0, linestyle='--', zorder=4)
        # Direct labels on the two reference lines (first/last panel only to cut clutter)
        if tag == 'stable':
            ax.text(p95_stable, 0.92, r'stable $p_{95}$',
                    transform=ax.get_xaxis_transform(), fontsize=6, color='0.45',
                    ha='left', va='top', rotation=90)
        if tag == 'Dragon King':
            ax.text(row['med'] + 0.01 * xmax, 0.92, 'median',
                    transform=ax.get_xaxis_transform(), fontsize=6, color=col,
                    ha='left', va='top', rotation=90)
        # Mass-beyond callout (upper-left — keeps the micro-table clear below)
        ax.text(0.04, 0.92, rf'{100 * row["frac"]:.0f}% $>p_{{95}}$',
                transform=ax.transAxes, fontsize=7.5, color=col,
                ha='left', va='top', fontweight='bold')
        tag_bit = f' ({tag})' if tag != 'mid' else ''
        ax.set_title(rf'$\lambda={lv:.2f}${tag_bit}',
                     fontsize=9, pad=3, fontweight='normal',
                     color=C_VERM if tag == 'Dragon King' else C_INK)
        ax.set_xlim(0, xmax)
        ax.spines['bottom'].set_bounds(0, xmax)

    ymax = max(c.max() for c in hist_counts) if hist_counts else 1.0
    rug_y = -0.07 * ymax
    for ax, (_, data, _, col, _) in zip(axes, picks):
        data = np.asarray(data, dtype=float)
        ax.plot(data, np.full_like(data, rug_y, dtype=float),
                '|', color=col, alpha=0.25, markersize=3.2, markeredgewidth=0.45)

    for i, ax in enumerate(axes):
        ax.set_ylim(rug_y * 1.9, ymax * 1.12)
        ax.spines['left'].set_bounds(0, ymax)
        if i > 0:
            ax.tick_params(labelleft=False)
            ax.spines['left'].set_visible(False)

    axes[0].set_ylabel('count of networks', fontsize=8, labelpad=4)
    axes[1].set_xlabel('cascade size (fraction of network)', fontsize=8, labelpad=4)

    # --- Micro-table (exact values; n is small: 3 cells) ---
    fig.text(0.10, 0.325, r'Summary (shared $x$-scale):',
             fontsize=7.5, color='0.3', ha='left', va='top')
    headers = [r'$\lambda$', 'regime', 'median', 'mean',
               r'% $>p_{95}^{\mathrm{stable}}$', 'max']
    col_x = [0.10, 0.22, 0.40, 0.52, 0.66, 0.88]
    for x, h in zip(col_x, headers):
        fig.text(x, 0.285, h, fontsize=6.5, color='0.45', ha='left', va='top')
    for r_i, row in enumerate(rows):
        y = 0.250 - r_i * 0.032
        vals = [
            f'{row["lam"]:.2f}',
            row['tag'],
            f'{row["med"]:.2f}',
            f'{row["mean"]:.2f}',
            f'{100 * row["frac"]:.0f}%',
            f'{row["mx"]:.2f}',
        ]
        for x, v in zip(col_x, vals):
            fig.text(x, y, v, fontsize=7, color=row['col'], ha='left', va='top',
                     fontweight='bold' if row['tag'] == 'Dragon King' else 'normal')

    fig.text(0.10, 0.97,
             r'Above the cliff, large cascades become common — not rare tail events',
             fontsize=9, color=C_INK, ha='left', va='top')
    _reading_guide(
        fig,
        f'Reading guide: sparkline = average cascade along $\\lambda$ '
        f'(dots = panels). Histograms share one $x$-scale. '
        f'Dotted line + pink band: beyond stable-regime $p_{{95}}={p95_stable:.2f}$. '
        f'Dashed: median. Rug: one tick per run. Table: exact summaries. '
        f'{n_mc} networks per panel.',
        width=100,
    )

    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, 'fig2_distributions.pdf')
    png_path = os.path.join(out_dir, 'fig2_distributions.png')
    for path in (pdf_path, png_path):
        fig.savefig(path, dpi=300, bbox_inches=None)
    if os.path.basename(os.path.normpath(out_dir)) == 'figures':
        fig.savefig(os.path.join(_REPO_ROOT, 'fig2_distributions.png'),
                    dpi=300, bbox_inches=None)
    plt.close(fig)
    return pdf_path


def plot_sensitivity(kappa_results: dict, out_dir: str = 'figures') -> str:
    """
    Figure 3: Mean cascade vs λ for multiple κ values.
    Coincidence is the finding — linestyles distinguish series; max |Δ| is on-figure.
    """
    kappas = sorted(kappa_results.keys())
    linestyles = ['-', '--', ':', '-.']
    colors = [C_BLUE, C_GREEN, C_ORANGE, C_SKY][:len(kappas)]

    n = _n_runs(next(iter(kappa_results.values())))
    all_mu = np.concatenate([kappa_results[k]['mean_cascade'] for k in kappas])
    lstar = _find_lambda_star(
        kappa_results[kappas[len(kappas) // 2]]['lambda_grid'],
        kappa_results[kappas[len(kappas) // 2]]['mean_cascade'],
    )
    y_hi = float(all_mu.max()) * 1.06

    fig = plt.figure(figsize=(5.8, 4.0))
    ax = fig.add_axes([0.14, 0.28, 0.58, 0.52])
    ax_gutter = fig.add_axes([0.74, 0.28, 0.24, 0.52])
    ax_gutter.axis('off')
    _tufte_ax(ax)

    ends = []
    for kappa, col, ls in zip(kappas, colors, linestyles):
        res = kappa_results[kappa]
        lam = res['lambda_grid']
        mu = res['mean_cascade']
        ax.plot(lam, mu, color=col, linestyle=ls, linewidth=1.3,
                solid_capstyle='round', zorder=2)
        ends.append((kappa, float(mu[-1]), col, ls))

    ax.axvline(lstar, color=C_GRAY, linewidth=0.6, linestyle=':', zorder=1)
    ax.text(lstar - 0.015, 0.97, rf'$\lambda^{{*}}\approx{lstar:.2f}$',
            transform=ax.get_xaxis_transform(),
            color=C_GRAY, fontsize=7, ha='right', va='top')

    ordered = sorted(ends, key=lambda t: t[1])
    for rank, (k, v, col, ls) in enumerate(ordered):
        y_ax = float(np.clip(v / y_hi + (rank - 0.5 * (len(ordered) - 1)) * 0.02,
                             0.08, 0.92))
        ax_gutter.plot([0.0, 0.12], [y_ax, y_ax], color=col, lw=1.3,
                       linestyle=ls, transform=ax_gutter.transAxes, clip_on=False)
        ax_gutter.text(0.16, y_ax, rf'$\kappa={k:.2f}$: ${v:.3f}$',
                       transform=ax_gutter.transAxes, color=col,
                       fontsize=7.5, va='center', ha='left')

    dmu = max(e[1] for e in ends) - min(e[1] for e in ends)
    ax_gutter.text(0.0, 0.02, rf'max $|\Delta\mu|={dmu:.3f}$',
                   transform=ax_gutter.transAxes, color=C_GRAY,
                   fontsize=7, va='bottom', ha='left')

    ax.set_xlabel(r'self-funding fraction $\lambda$', fontsize=9, labelpad=6)
    ax.set_ylabel('mean cascade size\n(fraction of network)', fontsize=9, labelpad=6)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, y_hi)
    ax.spines['left'].set_bounds(0, float(all_mu.max()))
    ax.spines['bottom'].set_bounds(0, 1)

    fig.text(0.14, 0.94,
             r'Investor concentration barely moves the cliff',
             fontsize=9, color=C_INK, ha='left', va='top')
    _reading_guide(
        fig,
        f'Reading guide: each curve is a different investor-concentration '
        f'level $\\kappa$ (color + line style). The curves sit on top of each '
        f'other — the transition location does not care about $\\kappa$ here. '
        f'Right labels: cascade size at $\\lambda=1$. {n} networks per point.',
        x=0.14, width=88,
    )

    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, 'fig3_sensitivity.pdf')
    png_path = os.path.join(out_dir, 'fig3_sensitivity.png')
    for path in (pdf_path, png_path):
        fig.savefig(path, dpi=300, bbox_inches=None)
    if os.path.basename(os.path.normpath(out_dir)) == 'figures':
        fig.savefig(os.path.join(_REPO_ROOT, 'fig3_sensitivity.png'),
                    dpi=300, bbox_inches=None)
    plt.close(fig)
    return pdf_path


def plot_density_sensitivity(density_results: dict, out_dir: str = 'figures') -> str:
    """
    Figure 5: Mean cascade vs λ across network density.
    Location of λ* is invariant; magnitude at λ = 1 scales with d.
    """
    densities = sorted(density_results.keys())
    linestyles = ['-', '--', '-.', ':']
    # Okabe–Ito categorical hues + linestyle (grayscale backup).
    colors = [C_SKY, C_BLUE, C_ORANGE, C_VERM][:len(densities)]
    if len(densities) > len(colors):
        colors = (colors + [C_GREEN, C_GRAY])[:len(densities)]

    n = _n_runs(next(iter(density_results.values())))
    all_mu = np.concatenate([density_results[d]['mean_cascade'] for d in densities])
    d_ref = 2.0 if 2.0 in density_results else densities[len(densities) // 2]
    lstar = _find_lambda_star(density_results[d_ref]['lambda_grid'],
                              density_results[d_ref]['mean_cascade'])
    lonset_vals = [
        _find_lambda_onset(density_results[d]['lambda_grid'],
                           density_results[d]['mean_cascade'],
                           density_results[d]['std_cascade'], k=2.0)
        for d in densities
    ]
    lonset_lo = min(lonset_vals)
    y_hi = float(all_mu.max()) * 1.06

    # Title | panel + gutter | footer  (end values live only in the gutter)
    fig = plt.figure(figsize=(6.2, 4.0))
    ax = fig.add_axes([0.12, 0.28, 0.62, 0.54])
    ax_gutter = fig.add_axes([0.75, 0.28, 0.23, 0.54])
    ax_gutter.axis('off')
    _tufte_ax(ax)

    end_vals = []
    for d, col, ls in zip(densities, colors, linestyles):
        res = density_results[d]
        lam = res['lambda_grid']
        mu = res['mean_cascade']
        ax.plot(lam, mu, color=col, linestyle=ls, linewidth=1.35,
                solid_capstyle='round', zorder=2)
        end_vals.append((d, float(mu[-1]), col, ls))

    ax.axvspan(lonset_lo, lstar, color='#999999', alpha=0.10, linewidth=0, zorder=0)
    ax.axvline(lstar, color=C_GRAY, linewidth=0.6, linestyle=':', zorder=1)
    ax.text(lstar - 0.015, 0.97, rf'$\lambda^{{*}}\approx{lstar:.2f}$',
            transform=ax.get_xaxis_transform(),
            color=C_GRAY, fontsize=7, ha='right', va='top')

    # Direct labels in gutter, sorted by final cascade (no collision)
    ordered = sorted(end_vals, key=lambda t: t[1])
    for rank, (d, v, col, ls) in enumerate(ordered):
        y_ax = (v - 0) / y_hi if y_hi > 0 else 0.5
        # slight stagger if values are close
        y_ax = float(np.clip(y_ax + (rank - 0.5 * (len(ordered) - 1)) * 0.015,
                             0.06, 0.94))
        ax_gutter.plot([0.0, 0.10], [y_ax, y_ax], color=col, lw=1.3,
                       linestyle=ls, transform=ax_gutter.transAxes, clip_on=False)
        ax_gutter.text(0.14, y_ax, rf'$d={d:.0f}$: ${v:.2f}$',
                       transform=ax_gutter.transAxes, color=col,
                       fontsize=7.5, va='center', ha='left')

    ax.set_xlabel(r'self-funding fraction $\lambda$', fontsize=9, labelpad=6)
    ax.set_ylabel('mean cascade size\n(fraction of network)', fontsize=9, labelpad=6)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, y_hi)
    ax.spines['left'].set_bounds(0, float(all_mu.max()))
    ax.spines['bottom'].set_bounds(0, 1)

    fig.text(0.12, 0.94,
             r'Density moves how big the crash is — not where the cliff sits',
             fontsize=9, color=C_INK, ha='left', va='top')
    _reading_guide(
        fig,
        f'Reading guide: each curve is a denser bank–fund network '
        f'(color + line style = density $d$). All curves break near the same '
        f'$\\lambda^{{*}}$; only the height at $\\lambda=1$ changes '
        f'(numbers at right). Grey band: transition window. '
        f'{n} simulated networks per point.',
        x=0.12, width=92,
    )

    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, 'fig5_density_sensitivity.pdf')
    png_path = os.path.join(out_dir, 'fig5_density_sensitivity.png')
    fig.savefig(pdf_path, dpi=300, bbox_inches=None)
    fig.savefig(png_path, dpi=300, bbox_inches=None)
    if os.path.basename(os.path.normpath(out_dir)) == 'figures':
        fig.savefig(os.path.join(_REPO_ROOT, 'fig5_density_sensitivity.png'),
                    dpi=300, bbox_inches=None)
    plt.close(fig)
    return pdf_path


def plot_lppls_illustration(sweep_result: dict, out_dir: str = 'figures') -> str:
    """
    Figure 4: Synthetic LPPLS time series. Purely illustrative of the
    super-exponential-with-shivers shape described in §4.1.
    Envelope (C = 0) is drawn so the oscillations are a visible residual.
    No cascade-onset overlay: mapping λ* to a time position would imply a
    t_c prediction that the paper explicitly disclaims.
    """
    # Synthetic LPPLS: ln(p) = A + B*(tc-t)^m * (1 + C*cos(w*ln(tc-t) + phi))
    # Parameters chosen to produce a ~5x rise with visible log-periodic shivers.
    tc   = 10.5
    t    = np.linspace(0.5, 9.8, 300)
    dt   = tc - t
    A, B, m = 6.0, -0.55, 0.45
    C, w, phi = 0.04, 7.0, 1.2
    ln_p   = A + B * dt**m * (1 + C * np.cos(w * np.log(dt) + phi))
    ln_env = A + B * dt**m
    price     = np.exp(ln_p)
    price_env = np.exp(ln_env)
    # Index convention: start = 100
    scale = 100.0 / price[0]
    price     = price * scale
    price_env = price_env * scale
    tau = t / tc

    fig = plt.figure(figsize=(5.6, 3.9))
    ax = fig.add_axes([0.14, 0.24, 0.82, 0.58])
    _tufte_ax(ax)

    ax.plot(tau, price_env, color=C_GRAY, linewidth=0.95, linestyle='--',
            solid_capstyle='round', zorder=1)
    ax.plot(tau, price, color=C_BLUE, linewidth=1.35, solid_capstyle='round',
            zorder=2)

    env_i = int(0.28 * len(tau))
    ax.text(tau[env_i], price_env[env_i] + (price.max() - price.min()) * 0.06,
            r'envelope ($C=0$)', color=C_GRAY, fontsize=7,
            ha='center', va='bottom')

    resid = price - price_env
    late = slice(int(0.70 * len(tau)), None)
    shiver_idx = late.start + int(np.argmax(np.abs(resid[late])))
    ax.annotate('log-periodic\noscillation',
                xy=(tau[shiver_idx], price[shiver_idx]),
                xytext=(0.50, price.max() * 0.72),
                fontsize=7, color=C_GRAY,
                arrowprops=dict(arrowstyle='->', color=C_GRAY,
                                lw=0.7, connectionstyle='arc3,rad=-0.15'))

    ax.set_xlabel(r'$t/t_c$  (synthetic; $t_c$ is not estimated)',
                  fontsize=9, labelpad=6)
    ax.set_ylabel('index (start = 100)', fontsize=9, labelpad=6)
    ax.set_xlim(tau[0], tau[-1])
    ax.set_ylim(price.min() * 0.92, price.max() * 1.04)
    ax.set_xticks([0.2, 0.4, 0.6, 0.8])
    ax.spines['left'].set_bounds(price.min(), price.max())
    ax.spines['bottom'].set_bounds(tau[0], tau[-1])

    fig.text(0.14, 0.92,
             r'Synthetic LPPLS shape — not a fit, not a forecast',
             fontsize=9, color=C_INK, ha='left', va='top')
    fig.text(0.14, 0.865,
             r'Caveat: no empirical SRT series, no $t_c$ prediction.',
             fontsize=7, color=C_VERM, ha='left', va='top')
    _reading_guide(
        fig,
        r'Reading guide: the solid curve is a made-up price path with '
        r'accelerating growth and wiggles; the dashed curve is the same '
        r'growth without the wiggles. Horizontal axis is a fake time scale. '
        r'This figure teaches a shape, not where the real SRT market sits.',
        x=0.14, width=88,
    )

    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, 'fig4_lppls_illustration.pdf')
    png_path = os.path.join(out_dir, 'fig4_lppls_illustration.png')
    fig.savefig(pdf_path, dpi=300, bbox_inches=None)
    fig.savefig(png_path, dpi=300, bbox_inches=None)
    if os.path.basename(os.path.normpath(out_dir)) == 'figures':
        fig.savefig(os.path.join(_REPO_ROOT, 'fig4_lppls_illustration.png'),
                    dpi=300, bbox_inches=None)
    plt.close(fig)
    return pdf_path


def plot_tranche_comparison(sweep_default: dict, sweep_empirical: dict,
                            out_dir: str = 'figures') -> str:
    """
    Figure 6: Mean cascade vs λ at δ = 0.08 (paper default) vs δ = 0.15
    (Osberghaus & Schepens 2026 median junior tranche).
    Coincidence of the curves is the invariance result; the onset-window
    tightening is the v2 mechanism the figure must make visible.
    """
    lam08 = sweep_default['lambda_grid']
    mu08  = sweep_default['mean_cascade']
    sd08  = sweep_default['std_cascade']
    lam15 = sweep_empirical['lambda_grid']
    mu15  = sweep_empirical['mean_cascade']

    lon08 = _find_lambda_onset(lam08, mu08, sd08, k=2.0)
    lon15 = _find_lambda_onset(lam15, mu15, sweep_empirical['std_cascade'], k=2.0)
    lstar = _find_lambda_star(lam08, mu08)
    n = _n_runs(sweep_default)
    dmu = float(np.max(np.abs(mu08 - mu15)))
    y_top = max((mu08 + sd08).max(), mu15.max()) * 1.04

    fig = plt.figure(figsize=(5.8, 4.0))
    ax = fig.add_axes([0.14, 0.28, 0.82, 0.52])
    _tufte_ax(ax)

    ax.fill_between(lam08, np.clip(mu08 - sd08, 0, None), mu08 + sd08,
                    color=C_BLUE, alpha=0.10, linewidth=0, zorder=1)
    ax.plot(lam08, mu08, color=C_BLUE, linewidth=1.4, linestyle='-',
            solid_capstyle='round', zorder=2, label=r'$\delta=0.08$ (paper)')
    ax.plot(lam15, mu15, color=C_VERM, linewidth=1.3, linestyle='--',
            solid_capstyle='round', zorder=3, label=r'$\delta=0.15$ (empirical median)')

    ax.axvline(lon08, color=C_BLUE, linewidth=0.6, linestyle=':', zorder=1)
    ax.axvline(lon15, color=C_VERM, linewidth=0.6, linestyle=':', zorder=1)

    # Direct labels near series ends (stable whitespace left of cliff)
    ax.plot([0.05, 0.14], [y_top * 0.88, y_top * 0.88], color=C_BLUE, lw=1.3)
    ax.text(0.16, y_top * 0.88, r'$\delta=0.08$ (paper default)',
            color=C_BLUE, fontsize=7.5, va='center')
    ax.plot([0.05, 0.14], [y_top * 0.78, y_top * 0.78],
            color=C_VERM, lw=1.2, linestyle='--')
    ax.text(0.16, y_top * 0.78, r'$\delta=0.15$ (empirical median)',
            color=C_VERM, fontsize=7.5, va='center')
    ax.text(0.05, y_top * 0.66,
            rf'max $|\Delta\mu|={dmu:.3f}$'
            + '\n'
            + rf'$\mu(\lambda{{=}}1)$: ${mu08[-1]:.3f}$ vs ${mu15[-1]:.3f}$',
            color=C_GRAY, fontsize=7, va='top')

    ax.set_xlabel(r'self-funding fraction $\lambda$', fontsize=9, labelpad=6)
    ax.set_ylabel('mean cascade size\n(fraction of network)', fontsize=9, labelpad=6)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, y_top)
    ax.spines['left'].set_bounds(0, max(mu08.max(), mu15.max()))
    ax.spines['bottom'].set_bounds(0, 1)

    fig.text(0.14, 0.94,
             r'Thicker junior tranche: same cliff height, tighter onset',
             fontsize=9, color=C_INK, ha='left', va='top')
    if abs(lon15 - lstar) < 1e-9:
        onset_line = (
            rf'Onset marks: $\lambda_{{\mathrm{{onset}}}}(\delta{{=}}0.08)'
            rf'\approx{lon08:.2f}$ (blue); '
            rf'at $\delta{{=}}0.15$, onset collapses onto '
            rf'$\lambda^{{*}}\approx{lon15:.2f}$ (vermillion).'
        )
    else:
        onset_line = (
            rf'Onset marks: $\delta{{=}}0.08\rightarrow{lon08:.2f}$; '
            rf'$\delta{{=}}0.15\rightarrow{lon15:.2f}$.'
        )
    fig.text(0.14, 0.895, onset_line, fontsize=7, color='0.3', ha='left', va='top')
    _reading_guide(
        fig,
        f'Reading guide: blue is the paper default tranche thickness; '
        f'vermillion dashed is the empirical median ($\\delta=0.15$). '
        f'The curves nearly overlap (invariance). Dotted verticals mark '
        f'onset for each $\\delta$. '
        f'Band: $\\pm 1$ SD for $\\delta=0.08$. {n} networks per point.',
        x=0.14, width=90,
    )

    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, 'fig6_tranche_comparison.pdf')
    png_path = os.path.join(out_dir, 'fig6_tranche_comparison.png')
    for path in (pdf_path, png_path):
        fig.savefig(path, dpi=300, bbox_inches=None)
    if os.path.basename(os.path.normpath(out_dir)) == 'figures':
        fig.savefig(os.path.join(_REPO_ROOT, 'fig6_tranche_comparison.png'),
                    dpi=300, bbox_inches=None)
    plt.close(fig)
    return pdf_path


def plot_all(sweep_result: dict, kappa_results: dict,
             density_results: dict = None,
             tranche_result: dict = None,
             out_dir: str = 'figures') -> list:
    """Run all plot functions. Returns list of output paths."""
    plt.rcParams.update({
        'font.family':      'sans-serif',
        'font.sans-serif':  ['Helvetica Neue', 'Arial', 'DejaVu Sans'],
        'font.size':        9,
        'axes.linewidth':   0.6,
        'xtick.major.width': 0.6,
        'ytick.major.width': 0.6,
        'figure.dpi':       150,
        'savefig.dpi':      300,
        'pdf.fonttype':     42,
        'ps.fonttype':      42,
    })
    paths = [
        plot_phase_transition(sweep_result, out_dir),
        plot_cascade_distributions(sweep_result, out_dir),
        plot_sensitivity(kappa_results, out_dir),
        plot_lppls_illustration(sweep_result, out_dir),
    ]
    if density_results is not None:
        paths.append(plot_density_sensitivity(density_results, out_dir))
    if tranche_result is not None:
        paths.append(plot_tranche_comparison(sweep_result, tranche_result, out_dir))
    return paths


# ---------------------------------------------------------------------------
# SECTION 5: Proxy metrics + main()
# ---------------------------------------------------------------------------

# Current Q1 2026 readings from public sources (see paper §5a).
# These are empirical snapshots, not model output.
COCKPIT_CURRENT = {
    'bdc_dispersion': {
        'label':     'BDC price dispersion',
        'value':     'Extreme: Blue Owl -68% YTD; FSK/GSBD dividend cuts; '
                     '$20.8B redemption requests Q1',
        'source':    'NYSE prices; KBRA/Fitch; Woozle Research (Apr 2026)',
        'signal':    'RED',
        'threshold': 'Cross-sectional std dev > 15% = elevated',
    },
    'clo_spread': {
        'label':     'CLO BB minus AAA spread',
        'value':     '~470-615 bps (US BB 600-750 bps; AAA ~130 bps over SOFR)',
        'source':    'TwentyFour AM (Mar 2026); PitchBook CLO Outlook',
        'signal':    'AMBER/RED',
        'threshold': 'Gap > 400 bps = elevated mezzanine stress',
    },
    'sofr_ois': {
        'label':     'SOFR-OIS spread',
        'value':     '~10-15 bps; interbank stress not yet acute',
        'source':    'FRED SOFR series; NY Fed (Apr 2026)',
        'signal':    'GREEN',
        'threshold': '> 30 bps = emerging stress; > 50 bps = acute',
    },
    'pik_ratio': {
        'label':     'PIK ratio in BDC filings (bad PIK)',
        'value':     '6.4% of total private debt volume (KBRA/Fitch Q1 2026)',
        'source':    'KBRA; Fitch Ratings; SEC EDGAR 10-Q filings',
        'signal':    'RED',
        'threshold': '> 4% bad PIK = late-cycle stress; > 6% = critical',
    },
    'secondary_pricing': {
        'label':     'Secondary market pricing of private credit stakes',
        'value':     'Multiple platforms gating at 5% cap; Blue Owl all-time low',
        'source':    'Setter Capital; public BDC prices (Apr 2026)',
        'signal':    'RED',
        'threshold': 'Widespread gating = effective NAV discount signal',
    },
    'cds_volume': {
        'label':     'CDS index volume (CDX IG/HY)',
        'value':     '$4.5T Q1 2026, +69% YoY, all-time record. '
                     'New S&P CDX Financials (FINDX) launched Apr 13 2026.',
        'source':    'ISDA/DTCC; Seeking Alpha; Traders Magazine (Apr 2026)',
        'signal':    'RED',
        'threshold': 'Record volume = systemic hedging demand',
    },
}

SIGNAL_ORDER = {'RED': 0, 'AMBER/RED': 1, 'AMBER': 2, 'GREEN': 3}


def compute_proxy_metrics(sweep_result: dict) -> dict:
    """
    Compute simulated lead-time proxy for each cockpit metric.

    For each metric we ask: at what λ does cascade size first exceed
    a 'warning threshold' (mean + 1 SD above the λ=0 baseline)?
    This gives a simulated λ_trigger per metric — earlier trigger = better lead time.

    In the paper this is used to rank the six metrics by their theoretical
    sensitivity to circular leverage buildup.

    Returns
    -------
    dict: metric_key -> {lambda_trigger, lead_fraction, rank}
        lead_fraction = 1 - (lambda_trigger / lambda_star)
        Higher = more lead time before the cascade cliff.
    """
    lam   = sweep_result['lambda_grid']
    mu    = sweep_result['mean_cascade']
    sd    = sweep_result['std_cascade']
    lstar = _find_lambda_star(lam, mu)

    baseline = mu[0] + sd[0]   # warning threshold: above λ=0 mean+SD

    # Simulated sensitivity weights per metric — how strongly each proxy
    # correlates with λ in the model. Justified in paper §5.
    # Scale: 1.0 = perfectly tracks λ; 0.0 = no sensitivity.
    # These are model assumptions, documented as such.
    sensitivity = {
        'bdc_dispersion':   0.85,   # directly reflects fund heterogeneity
        'clo_spread':       0.75,   # mezzanine repricing tracks loss expectations
        'sofr_ois':         0.30,   # lags — only fires on interbank transmission
        'pik_ratio':        0.80,   # reference portfolio quality
        'secondary_pricing':0.90,   # market's direct assessment of fund solvency
        'cds_volume':       0.60,   # systemic anxiety, directionally noisy
    }

    # Find λ where mean cascade first exceeds baseline
    trigger_idx = next(
        (i for i, m in enumerate(mu) if m > baseline), len(lam) - 1
    )
    lambda_trigger_base = float(lam[trigger_idx])

    results = {}
    for key, sens in sensitivity.items():
        # Earlier trigger for higher-sensitivity metrics
        lt = lambda_trigger_base * (1.0 - 0.4 * (sens - 0.5))
        lt = float(np.clip(lt, lam[0], lam[-1]))
        lead = max(0.0, (lstar - lt) / lstar) if lstar > 0 else 0.0
        results[key] = {
            'lambda_trigger': round(lt, 3),
            'lead_fraction':  round(lead, 3),
            'signal_current': COCKPIT_CURRENT[key]['signal'],
        }

    # Rank by lead_fraction descending
    ranked = sorted(results.items(), key=lambda x: -x[1]['lead_fraction'])
    for rank, (key, _) in enumerate(ranked, 1):
        results[key]['rank'] = rank

    return results


def export_cockpit_csv(sweep_result: dict, out_dir: str = 'figures') -> str:
    """
    Export the cockpit table as CSV for paper supplementary material.
    Columns: rank, metric, current_value, signal, lambda_trigger, lead_fraction, source
    """
    os.makedirs(out_dir, exist_ok=True)
    metrics = compute_proxy_metrics(sweep_result)
    rows = sorted(metrics.items(), key=lambda x: x[1]['rank'])

    path = os.path.join(out_dir, 'cockpit_metrics.csv')
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['rank', 'metric', 'current_value_q1_2026',
                    'signal', 'lambda_trigger', 'lead_fraction', 'source'])
        for key, vals in rows:
            c = COCKPIT_CURRENT[key]
            w.writerow([
                vals['rank'],
                c['label'],
                c['value'],
                c['signal'],
                vals['lambda_trigger'],
                vals['lead_fraction'],
                c['source'],
            ])
    return path


def _write_publication_summary(
    sweep_result: dict,
    kappa_results: dict,
    density_results: dict,
    tranche_result: dict,
    max_abs_dmu: float,
    tranche_onset: float,
    tranche_star: float,
    *,
    seed: int,
    n_runs_sweep: int,
    n_runs_kappa: int,
    n_runs_density: int,
    shock_size: float,
    dest: str = 'results/publication_sweep_summary.json',
) -> str:
    """Persist publication-sweep scalars for the manuscript integrity gate."""
    os.makedirs(os.path.dirname(dest) or '.', exist_ok=True)
    d1 = density_results[1.0]
    d5 = density_results[5.0]
    payload = {
        "schema": "srt-publication-sweep/v1",
        "note": (
            "Summary of python srt_simulation.py. "
            "Not the n=80 claim-gate JSON. "
            "Do not bind these percents to srt_claim_verify.json."
        ),
        "seed": seed,
        "n_runs_sweep": n_runs_sweep,
        "n_runs_kappa": n_runs_kappa,
        "n_runs_density": n_runs_density,
        "shock_size": shock_size,
        "lambda_onset": _find_lambda_onset(
            sweep_result['lambda_grid'], sweep_result['mean_cascade'],
            sweep_result['std_cascade'], k=2.0,
        ),
        "lambda_star": _find_lambda_star(
            sweep_result['lambda_grid'], sweep_result['mean_cascade'],
        ),
        "lambda_star_percent": 95,
        "mean_cascade_lambda0": float(sweep_result['mean_cascade'][0]),
        "mean_cascade_lambda1": float(sweep_result['mean_cascade'][-1]),
        "density_d1_cascade_lambda1": float(d1['mean_cascade'][-1]),
        "density_d1_cascade_percent": int(round(d1['mean_cascade'][-1] * 100)),
        "density_d2_cascade_lambda1": float(density_results[2.0]['mean_cascade'][-1]),
        "density_d3_cascade_lambda1": float(density_results[3.0]['mean_cascade'][-1]),
        "density_d5_cascade_lambda1": float(d5['mean_cascade'][-1]),
        "density_d5_cascade_percent": int(round(d5['mean_cascade'][-1] * 100)),
        "tranche_delta_015_lambda_onset": float(tranche_onset),
        "tranche_delta_015_lambda_star": float(tranche_star),
        "tranche_max_abs_dmu": float(max_abs_dmu),
        "tranche_delta_015_mean_cascade_lambda1": float(
            tranche_result['mean_cascade'][-1]
        ),
    }
    # Keep the printed 95% label honest: only write it when λ* rounds to 0.95
    star = payload["lambda_star"]
    payload["lambda_star_percent"] = int(round(star * 100))
    with open(dest, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, indent=2)
        fh.write('\n')
    return dest


def main(
    n_runs_sweep:   int = 1000,
    n_runs_kappa:   int = 500,
    n_runs_density: int = 500,
    shock_size:     float = 0.05,
    out_dir:        str = 'figures',
    seed:           int = DEFAULT_SEED,
) -> None:
    """
    Full pipeline: sweep → sensitivity (kappa, density, tranche) → plots → cockpit CSV.
    Called by GitHub Actions / Zenodo reproduction script.
    """
    global RNG
    RNG = np.random.default_rng(seed)

    grid = np.linspace(0.0, 1.0, 21)

    print(f"[1/6] Lambda sweep  (n_runs={n_runs_sweep}, shock={shock_size}) ...")
    sw = sweep_lambda(lambda_grid=grid, n_runs=n_runs_sweep,
                      shock_size=shock_size)
    lstar  = _find_lambda_star(sw['lambda_grid'], sw['mean_cascade'])
    lonset = _find_lambda_onset(sw['lambda_grid'], sw['mean_cascade'],
                                sw['std_cascade'], k=2.0)
    print(f"      λ_onset ≈ {lonset:.2f}  λ*(cliff) ≈ {lstar:.2f}  "
          f"max cascade: {sw['mean_cascade'].max():.3f}")

    print(f"[2/6] Kappa sensitivity (n_runs={n_runs_kappa}) ...")
    kres = sweep_kappa_sensitivity(lambda_grid=grid, n_runs=n_runs_kappa)

    print(f"[3/6] Density sensitivity (n_runs={n_runs_density}) ...")
    dres = sweep_density_sensitivity(lambda_grid=grid, n_runs=n_runs_density)
    print("      density    λ_onset  λ*(cliff)  cascade(λ=1.0)")
    for d in sorted(dres.keys()):
        r = dres[d]
        lo = _find_lambda_onset(r['lambda_grid'], r['mean_cascade'], r['std_cascade'], k=2.0)
        ls = _find_lambda_star(r['lambda_grid'], r['mean_cascade'])
        print(f"      {d:>5.1f}      {lo:>5.2f}     {ls:>5.2f}     {r['mean_cascade'][-1]:>.3f}")

    print(f"[4/6] Tranche comparison δ=0.15 (n_runs={n_runs_sweep}) ...")
    sw15 = sweep_lambda(lambda_grid=grid, n_runs=n_runs_sweep,
                        shock_size=shock_size, tranche_thickness=0.15)
    lon15 = _find_lambda_onset(sw15['lambda_grid'], sw15['mean_cascade'],
                               sw15['std_cascade'], k=2.0)
    ls15  = _find_lambda_star(sw15['lambda_grid'], sw15['mean_cascade'])
    dmu15 = float(np.max(np.abs(sw['mean_cascade'] - sw15['mean_cascade'])))
    print(f"      δ=0.15  λ_onset ≈ {lon15:.2f}  λ* ≈ {ls15:.2f}  "
          f"max |Δμ| vs δ=0.08 = {dmu15:.3f}")

    print("[5/6] Generating figures ...")
    fig_paths = plot_all(sw, kres, dres, tranche_result=sw15, out_dir=out_dir)
    for p in fig_paths:
        print(f"      {p}")

    print("[6/6] Exporting cockpit CSV and sweep summary ...")
    metrics = compute_proxy_metrics(sw)
    csv_path = export_cockpit_csv(sw, out_dir=out_dir)
    print(f"      {csv_path}")
    summary_path = _write_publication_summary(
        sw, kres, dres, sw15, dmu15, lon15, ls15, seed=seed,
        n_runs_sweep=n_runs_sweep, n_runs_kappa=n_runs_kappa,
        n_runs_density=n_runs_density, shock_size=shock_size,
    )
    print(f"      {summary_path}")

    print("\n=== Cockpit summary (Q1 2026 readings) ===")
    ranked = sorted(metrics.items(), key=lambda x: x[1]['rank'])
    for key, vals in ranked:
        c = COCKPIT_CURRENT[key]
        sig = c['signal']
        pad = ' ' * (10 - len(sig))
        print(f"  #{vals['rank']} [{sig}]{pad} λ_trigger={vals['lambda_trigger']:.2f} "
              f"lead={vals['lead_fraction']:.2f}  {c['label']}")

    print("\nDone. Reproduce with: python srt_simulation.py")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    quick = '--quick' in sys.argv
    main(
        n_runs_sweep   = 300 if quick else 1000,
        n_runs_kappa   = 200 if quick else 500,
        n_runs_density = 200 if quick else 500,
        shock_size     = 0.05,
        out_dir        = 'figures',
    )
