"""Figure 7: Metric 2 BDC price-dispersion sparkline (paper v2.1).

Reads results/metric2_bdc_dispersion.csv (measure B). Does not run the
simulation or fetch market data. Series is cut at Q3 2026, matching Table 2.

Run: python plot_metric2_sparkline.py
"""
from __future__ import annotations

import csv
import os
from datetime import date

import matplotlib.pyplot as plt

from srt_simulation import (
    C_BLUE,
    C_GRAY,
    C_GREEN,
    C_INK,
    C_ORANGE,
    C_VERM,
    _REPO_ROOT,
    _reading_guide,
    _tufte_ax,
)

CSV_NAME = os.path.join('results', 'metric2_bdc_dispersion.csv')
STEM = 'fig7_metric2_dispersion'
CUTOFF = date(2026, 9, 30)  # last complete quarter in Table 2
BASE_YEARS = (2023, 2024)

STATUS_MARKER = {
    'GREEN': ('o', C_GREEN),
    'AMBER': ('^', C_ORANGE),
    'RED': ('s', C_VERM),
}

# Quarters the Metric 2 paragraph names. Labels use the paper's rounding.
# (text, ha, va, dx, dy) — keep every glyph inside the axes.
CALLOUTS = {
    date(2023, 3, 31): ('Q1 2023', 'left', 'top', 7, -5),
    date(2024, 12, 31): ('Q4 2024', 'center', 'bottom', 0, 8),
    date(2026, 3, 31): ('Q1 2026  0.074', 'right', 'bottom', -8, 8),
    date(2026, 9, 30): ('0.049', 'center', 'bottom', 0, 8),
}


def _load_series(path: str):
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        for rec in csv.DictReader(f):
            y, m, d = (int(p) for p in rec['Date'][:10].split('-'))
            q = date(y, m, d)
            if q > CUTOFF:
                continue
            val = rec.get('B_norm_px_med', '').strip()
            if not val:
                continue
            rows.append(
                (q, float(val), rec['B_norm_px_med_status'].strip())
            )
    if len(rows) < 8:
        raise SystemExit(f'need a full 2023-24 baseline; got {len(rows)} rows from {path}')
    return rows


def _baseline(rows) -> float:
    base = [v for q, v, _ in rows if q.year in BASE_YEARS]
    base.sort()
    n = len(base)
    if n < 2:
        raise SystemExit('2023-24 baseline missing')
    if n % 2:
        return base[n // 2]
    return 0.5 * (base[n // 2 - 1] + base[n // 2])


def plot_metric2(csv_path: str, out_dir: str) -> str:
    rows = _load_series(csv_path)
    median = _baseline(rows)
    amber = 1.25 * median
    red = 2.0 * median
    xs = list(range(len(rows)))
    ys = [v for _, v, _ in rows]

    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Helvetica Neue', 'Arial', 'DejaVu Sans'],
        'font.size': 9,
        'axes.linewidth': 0.6,
        'xtick.major.width': 0.6,
        'ytick.major.width': 0.6,
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'pdf.fonttype': 42,
        'ps.fonttype': 42,
    })

    fig = plt.figure(figsize=(7.2, 3.55))
    # Bands: title | plot | footer. Right gutter for threshold labels.
    ax = fig.add_axes([0.10, 0.30, 0.72, 0.56])
    _tufte_ax(ax)

    ax.axhspan(amber, red, color=C_ORANGE, alpha=0.08, linewidth=0, zorder=0)
    ax.axhspan(red, 0.082, color=C_VERM, alpha=0.07, linewidth=0, zorder=0)

    ax.axhline(median, color=C_GRAY, linewidth=0.8, linestyle=':', zorder=1)
    ax.axhline(amber, color=C_ORANGE, linewidth=0.8, linestyle='--', zorder=1)
    ax.axhline(red, color=C_VERM, linewidth=0.8, linestyle='--', zorder=1)

    ax.plot(xs, ys, color=C_BLUE, linewidth=1.15, solid_capstyle='round',
            zorder=2)

    for i, (q, v, status) in enumerate(rows):
        mk, col = STATUS_MARKER[status]
        ax.plot(i, v, marker=mk, color=col, markersize=6.0,
                markeredgecolor='white', markeredgewidth=0.5, zorder=3)
        if q in CALLOUTS:
            text, ha, va, dx, dy = CALLOUTS[q]
            ax.annotate(
                text,
                xy=(i, v),
                xytext=(dx, dy),
                textcoords='offset points',
                fontsize=7,
                color=col,
                ha=ha,
                va=va,
                clip_on=True,
            )

    y0, y1 = min(ys), max(ys)
    ax.set_ylim(0.022, 0.082)
    ax.set_xlim(-0.45, len(rows) - 0.15)
    ax.spines['bottom'].set_bounds(0, len(rows) - 1)
    ax.spines['left'].set_bounds(0.022, 0.082)

    year_ticks, year_labels = [], []
    for i, (q, _, _) in enumerate(rows):
        if q.month == 3:
            year_ticks.append(i)
            year_labels.append(str(q.year))
    # Last complete quarter is Q3 2026, not a year-start tick.
    year_ticks.append(len(rows) - 1)
    year_labels.append('Q3')
    ax.set_xticks(year_ticks)
    ax.set_xticklabels(year_labels)
    ax.set_ylabel('quarter-rebased dispersion', fontsize=8, labelpad=6)
    ax.tick_params(labelsize=8)

    # Threshold labels in the right gutter (outside the data spine).
    trans = ax.get_yaxis_transform()
    for y, lab, col in (
        (median, 'median', C_GRAY),
        (amber, r'$1.25\times$ amber', C_ORANGE),
        (red, r'$2.0\times$ red', C_VERM),
    ):
        ax.text(
            1.02, y, lab, transform=trans, fontsize=7, color=col,
            ha='left', va='center', clip_on=False,
        )

    fig.text(
        0.10, 0.96,
        'Only Q1 2026 crossed red; Q3 2026 is amber, still above the 2023-24 median',
        fontsize=9, color=C_INK, ha='left', va='top',
    )
    _reading_guide(
        fig,
        'Reading guide: each marker is one quarter of BDC price dispersion '
        "(15-name panel, prices rebased to that quarter's first close; the "
        'reading is the median of daily cross-sectional standard deviations). '
        'Circles green, triangles amber, squares red. Grey dotted line: 2023-24 '
        'median (0.037 in the text). Orange band: amber zone. Vermillion band: '
        'red zone. Series ends Q3 2026.',
        width=108,
    )

    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, f'{STEM}.pdf')
    png_path = os.path.join(out_dir, f'{STEM}.png')
    for path in (pdf_path, png_path):
        fig.savefig(path, dpi=300, bbox_inches=None)
    if os.path.basename(os.path.normpath(out_dir)) == 'figures':
        fig.savefig(os.path.join(_REPO_ROOT, f'{STEM}.png'),
                    dpi=300, bbox_inches=None)
    plt.close(fig)
    return pdf_path


def main() -> None:
    csv_path = os.path.join(_REPO_ROOT, CSV_NAME)
    out_dir = os.path.join(_REPO_ROOT, 'figures')
    path = plot_metric2(csv_path, out_dir)
    print(path)


if __name__ == '__main__':
    main()
