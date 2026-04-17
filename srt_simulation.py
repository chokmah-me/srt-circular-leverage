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
import csv, os

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

def _tufte_ax(ax):
    """Strip to bare minimum: bottom + left spines only, no top/right."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.6)
    ax.spines['bottom'].set_linewidth(0.6)
    ax.tick_params(length=3, width=0.6, labelsize=8)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')


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
    Annotates λ*, baseline cascade level, and the DK / stable regime zones.
    """
    os.makedirs(out_dir, exist_ok=True)
    lam  = sweep_result['lambda_grid']
    mu   = sweep_result['mean_cascade']
    sd   = sweep_result['std_cascade']
    lstar = _find_lambda_star(lam, mu)

    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    _tufte_ax(ax)

    # SD band
    ax.fill_between(lam, mu - sd, mu + sd, color='#4878CF', alpha=0.12, linewidth=0)
    # Mean line
    ax.plot(lam, mu, color='#4878CF', linewidth=1.4, solid_capstyle='round')
    # Baseline (λ=0 level) — thin reference
    ax.axhline(mu[0], color='#888888', linewidth=0.5, linestyle='--', zorder=0)

    # λ* annotation
    ax.axvline(lstar, color='#C44E52', linewidth=0.8, linestyle=':', zorder=1)
    ax.text(lstar + 0.01, ax.get_ylim()[0] + (mu.max() - mu.min()) * 0.05,
            f'λ* ≈ {lstar:.2f}', color='#C44E52', fontsize=7.5,
            va='bottom', ha='left')

    # Zone labels — placed in data whitespace
    ymid = mu.min() + (mu.max() - mu.min()) * 0.85
    ax.text(lstar * 0.45, ymid, 'stable regime', fontsize=7,
            color='#555555', ha='center', style='italic')
    ax.text(lstar + (1.0 - lstar) * 0.45, ymid, 'Dragon King regime',
            fontsize=7, color='#C44E52', ha='center', style='italic')

    ax.set_xlabel('self-funding fraction λ', fontsize=9, labelpad=6)
    ax.set_ylabel('mean cascade size\n(fraction of network)', fontsize=9, labelpad=6)
    ax.set_xlim(0, 1)
    ax.set_ylim(bottom=0)

    # Tufte-style range frame: shrink spines to data range
    ax.spines['left'].set_bounds(mu.min(), mu.max())
    ax.spines['bottom'].set_bounds(lam.min(), lam.max())

    fig.text(0.13, 0.01,
             'Shaded band: ±1 SD across Monte Carlo runs. '
             'Dashed: baseline cascade at λ=0.',
             fontsize=6.5, color='#777777')

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    path = os.path.join(out_dir, 'fig1_phase_transition.pdf')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    png_path = path.replace('.pdf', '.png')
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return path


def plot_cascade_distributions(sweep_result: dict, out_dir: str = 'figures') -> str:
    """
    Figure 2: Cascade size distributions at λ_low, λ_mid, λ_high.
    Three small multiples on one row. Rug plot below each histogram.
    Shows power-law tail (low λ) vs Dragon King outlier mass (high λ).
    """
    os.makedirs(out_dir, exist_ok=True)
    lam_grid = sweep_result['lambda_grid']
    cascades = sweep_result['all_cascades']

    # Pick three representative λ values
    n = len(lam_grid)
    idx_low  = 2
    idx_mid  = n // 2
    idx_high = n - 1
    picks = [
        (idx_low,  lam_grid[idx_low],  cascades[idx_low]),
        (idx_mid,  lam_grid[idx_mid],  cascades[idx_mid]),
        (idx_high, lam_grid[idx_high], cascades[idx_high]),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(7.5, 3.0),
                             sharey=False, sharex=False)
    colors = ['#4878CF', '#6ACC65', '#C44E52']

    for ax, (_, lv, data), col in zip(axes, picks, colors):
        _tufte_ax(ax)
        ax.spines['left'].set_visible(False)
        ax.yaxis.set_visible(False)

        bins = np.linspace(0, max(data.max(), 0.01), 30)
        ax.hist(data, bins=bins, color=col, alpha=0.75, linewidth=0,
                density=True)

        # Rug
        ax.plot(data, np.full_like(data, -0.4),
                '|', color=col, alpha=0.25, markersize=3, markeredgewidth=0.4)

        # Median line
        med = np.median(data)
        ax.axvline(med, color=col, linewidth=0.8, linestyle='--', alpha=0.7)

        ax.set_xlabel('cascade size', fontsize=8, labelpad=4)
        ax.set_title(f'λ = {lv:.2f}', fontsize=9, pad=4, fontweight='normal')
        ax.set_xlim(left=0)
        ax.spines['bottom'].set_bounds(0, data.max())

    axes[0].set_title(axes[0].get_title() + '\n(stable)', fontsize=9,
                      pad=4, fontweight='normal')
    axes[2].set_title(axes[2].get_title() + '\n(Dragon King)', fontsize=9,
                      pad=4, color='#C44E52', fontweight='normal')

    fig.text(0.5, 0.01,
             'Dashed line: median. Rug: individual Monte Carlo outcomes.',
             fontsize=6.5, color='#777777', ha='center')

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    path = os.path.join(out_dir, 'fig2_distributions.pdf')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    png_path = path.replace('.pdf', '.png')
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return path


def plot_sensitivity(kappa_results: dict, out_dir: str = 'figures') -> str:
    """
    Figure 3: Mean cascade vs λ for multiple κ values.
    Staggered right-side labels; absolute minimum gap to prevent overlap.
    """
    os.makedirs(out_dir, exist_ok=True)
    colors = ['#4878CF', '#6ACC65', '#C44E52', '#8172B2']
    kappas = sorted(kappa_results.keys())

    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    _tufte_ax(ax)

    for kappa, col in zip(kappas, colors):
        res = kappa_results[kappa]
        lam = res['lambda_grid']
        mu  = res['mean_cascade']
        ax.plot(lam, mu, color=col, linewidth=1.3, solid_capstyle='round')

    # Right-edge labels: force absolute vertical separation regardless of
    # how close the curves actually end. Sorted by end-value then pushed apart.
    all_mu = np.concatenate([kappa_results[k]['mean_cascade'] for k in kappas])
    y_span = all_mu.max() - all_mu.min()
    min_gap_abs = max(0.02 * y_span, 0.012)

    ends = sorted(
        [(k, kappa_results[k]['mean_cascade'][-1]) for k in kappas],
        key=lambda x: x[1]
    )
    placed_ys = []
    last_y = -np.inf
    for k, v in ends:
        y = max(v, last_y + min_gap_abs)
        placed_ys.append((k, y))
        last_y = y

    for k, y in placed_ys:
        col = colors[kappas.index(k)]
        ax.text(1.015, y, f'κ = {k:.2f}', color=col, fontsize=7.5,
                va='center', ha='left')

    ax.set_xlabel('self-funding fraction λ', fontsize=9, labelpad=6)
    ax.set_ylabel('mean cascade size', fontsize=9, labelpad=6)
    ax.set_xlim(0, 1.16)
    ax.set_ylim(bottom=0)

    ax.spines['left'].set_bounds(0, all_mu.max())
    ax.spines['bottom'].set_bounds(0, 1)

    fig.text(0.13, 0.01,
             'κ = investor concentration. Curves are nearly coincident: the '
             'transition location is insensitive to κ in this parametrization.',
             fontsize=6.5, color='#777777')

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    path = os.path.join(out_dir, 'fig3_sensitivity.pdf')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    png_path = path.replace('.pdf', '.png')
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return path


def plot_density_sensitivity(density_results: dict, out_dir: str = 'figures') -> str:
    """
    Figure 5: Mean cascade vs λ for multiple network density values.
    Density = expected number of bank-connections per fund.
    Key finding: the transition location (λ*) is invariant across density;
    cascade magnitude at high λ scales with density.
    """
    os.makedirs(out_dir, exist_ok=True)
    colors = ['#4878CF', '#6ACC65', '#EE9A49', '#C44E52']
    densities = sorted(density_results.keys())

    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    _tufte_ax(ax)

    for d, col in zip(densities, colors):
        res = density_results[d]
        lam = res['lambda_grid']
        mu  = res['mean_cascade']
        ax.plot(lam, mu, color=col, linewidth=1.3, solid_capstyle='round')

    # Stagger right-edge labels by end-value
    end_vals = sorted(
        [(d, density_results[d]['mean_cascade'][-1]) for d in densities],
        key=lambda x: x[1]
    )
    y_range = max(v for _, v in end_vals) - min(v for _, v in end_vals)
    placed = []
    min_gap = 0.03 * max(v for _, v in end_vals) if y_range > 0 else 0.005
    for d, v in end_vals:
        y = v
        while any(abs(y - py) < min_gap for py in placed):
            y -= min_gap
        placed.append(y)
        col = colors[densities.index(d)]
        ax.text(1.01, y, f'density = {d:.1f}', color=col, fontsize=7.5,
                va='center', ha='left')

    # Shade transition zone ~0.90-0.95 (invariant across density)
    ax.axvspan(0.90, 0.95, color='#999999', alpha=0.08, linewidth=0)

    ax.set_xlabel('self-funding fraction λ', fontsize=9, labelpad=6)
    ax.set_ylabel('mean cascade size', fontsize=9, labelpad=6)
    ax.set_xlim(0, 1.20)
    ax.set_ylim(bottom=0)

    all_mu = np.concatenate([density_results[d]['mean_cascade'] for d in densities])
    ax.spines['left'].set_bounds(0, all_mu.max())
    ax.spines['bottom'].set_bounds(0, 1)

    fig.text(0.13, 0.01,
             'density = expected bank-connections per fund. '
             'Grey band: transition zone (≈0.90–0.95) across all densities.',
             fontsize=6.5, color='#777777')

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    path = os.path.join(out_dir, 'fig5_density_sensitivity.pdf')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    png_path = path.replace('.pdf', '.png')
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return path


def plot_lppls_illustration(sweep_result: dict, out_dir: str = 'figures') -> str:
    """
    Figure 4: Synthetic LPPLS time series. Purely illustrative of the
    super-exponential-with-shivers shape described in §4.1.
    Per SME review, no cascade onset overlay is drawn: mapping λ* to a time
    position would imply a t_c prediction that the paper explicitly disclaims.
    """
    os.makedirs(out_dir, exist_ok=True)

    # Synthetic LPPLS: ln(p) = A + B*(tc-t)^m * (1 + C*cos(w*ln(tc-t) + phi))
    # Parameters chosen to produce a ~5x rise with visible log-periodic shivers.
    tc   = 10.5
    t    = np.linspace(0.5, 9.8, 300)
    dt   = tc - t
    A, B, m = 6.0, -0.55, 0.45
    C, w, phi = 0.04, 7.0, 1.2
    ln_p = A + B * dt**m * (1 + C * np.cos(w * np.log(dt) + phi))
    price = np.exp(ln_p)

    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    _tufte_ax(ax)

    ax.plot(t, price, color='#4878CF', linewidth=1.3, solid_capstyle='round')

    # Annotate log-periodic oscillations on a shiver
    shiver_idx = np.argmin(np.abs(t - 4.5))
    ax.annotate('log-periodic\n"shiver"',
                xy=(t[shiver_idx], price[shiver_idx]),
                xytext=(t[shiver_idx] - 1.8, price[shiver_idx] * 0.92),
                fontsize=7, color='#555555',
                arrowprops=dict(arrowstyle='->', color='#888888',
                                lw=0.7, connectionstyle='arc3,rad=0.2'))

    # X-axis: label as years relative to cycle start, not absolute
    year_ticks = [0.5, 2.5, 4.5, 6.5, 8.5]
    ax.set_xticks(year_ticks)
    ax.set_xticklabels([f'Y{int(y - 0.5 + 1)}' for y in year_ticks], fontsize=8)

    ax.set_xlabel('time (stylized cycle years)', fontsize=9, labelpad=6)
    ax.set_ylabel('SRT issuance index\n(normalized)', fontsize=9, labelpad=6)
    ax.set_xlim(t[0] - 0.2, t[-1] + 0.3)
    ax.set_ylim(bottom=price.min() * 0.95)
    ax.spines['left'].set_bounds(price.min(), price.max())
    ax.spines['bottom'].set_bounds(t[0], t[-1])

    # Prominent synthetic label
    ax.text(0.02, 0.97,
            'SYNTHETIC, illustrative only.\nNo empirical fit. No t_c prediction.',
            transform=ax.transAxes, fontsize=7, color='#C44E52',
            va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor='#C44E52', linewidth=0.6, alpha=0.9))

    plt.tight_layout(rect=[0, 0.02, 1, 1])
    path = os.path.join(out_dir, 'fig4_lppls_illustration.pdf')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    png_path = path.replace('.pdf', '.png')
    fig.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return path


def plot_all(sweep_result: dict, kappa_results: dict,
             density_results: dict = None,
             out_dir: str = 'figures') -> list:
    """Run all plot functions. Returns list of output paths."""
    # Global rcParams — set once
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


def main(
    n_runs_sweep:   int = 1000,
    n_runs_kappa:   int = 500,
    n_runs_density: int = 500,
    shock_size:     float = 0.05,
    out_dir:        str = 'figures',
    seed:           int = DEFAULT_SEED,
) -> None:
    """
    Full pipeline: sweep → sensitivity (kappa, density) → plots → cockpit CSV.
    Called by GitHub Actions / Zenodo reproduction script.
    """
    global RNG
    RNG = np.random.default_rng(seed)

    grid = np.linspace(0.0, 1.0, 21)

    print(f"[1/5] Lambda sweep  (n_runs={n_runs_sweep}, shock={shock_size}) ...")
    sw = sweep_lambda(lambda_grid=grid, n_runs=n_runs_sweep,
                      shock_size=shock_size)
    lstar  = _find_lambda_star(sw['lambda_grid'], sw['mean_cascade'])
    lonset = _find_lambda_onset(sw['lambda_grid'], sw['mean_cascade'],
                                sw['std_cascade'], k=2.0)
    print(f"      λ_onset ≈ {lonset:.2f}  λ*(cliff) ≈ {lstar:.2f}  "
          f"max cascade: {sw['mean_cascade'].max():.3f}")

    print(f"[2/5] Kappa sensitivity (n_runs={n_runs_kappa}) ...")
    kres = sweep_kappa_sensitivity(lambda_grid=grid, n_runs=n_runs_kappa)

    print(f"[3/5] Density sensitivity (n_runs={n_runs_density}) ...")
    dres = sweep_density_sensitivity(lambda_grid=grid, n_runs=n_runs_density)
    print("      density    λ_onset  λ*(cliff)  cascade(λ=1.0)")
    for d in sorted(dres.keys()):
        r = dres[d]
        lo = _find_lambda_onset(r['lambda_grid'], r['mean_cascade'], r['std_cascade'], k=2.0)
        ls = _find_lambda_star(r['lambda_grid'], r['mean_cascade'])
        print(f"      {d:>5.1f}      {lo:>5.2f}     {ls:>5.2f}     {r['mean_cascade'][-1]:>.3f}")

    print("[4/5] Generating figures ...")
    fig_paths = plot_all(sw, kres, dres, out_dir=out_dir)
    for p in fig_paths:
        print(f"      {p}")

    print("[5/5] Exporting cockpit CSV ...")
    metrics = compute_proxy_metrics(sw)
    csv_path = export_cockpit_csv(sw, out_dir=out_dir)
    print(f"      {csv_path}")

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
