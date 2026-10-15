"""Metric 2: BDC price dispersion, computed two ways, with a calm baseline.

A: cross-sectional std of quarterly total returns (robustness check;
   no base-date dependence).
B: median daily cross-sectional std of prices normalized to each quarter's
   first close (v2.1 scored measure, re-based per quarter).

Status rule (judgment-based, like the other cockpit weights), vs the
2023-2024 median:
   RED   if value > 2.0x
   AMBER if value > 1.25x
   GREEN otherwise
The in-progress quarter is dropped (QE labels are quarter-end).
Run: pip install yfinance pandas   then: python bdc_dispersion.py
"""
import pandas as pd
import yfinance as yf

PANEL = ["ARCC", "OBDC", "FSK", "GSBD", "GBDC", "BXSL", "MAIN", "HTGC",
         "TSLX", "OCSL", "PSEC", "MFIC", "CSWC", "NMFC", "CGBD"]  # fixed panel

px = yf.download(PANEL, start="2022-12-31", end="2026-10-14",
                 auto_adjust=True, progress=False)["Close"].dropna(how="all")

# A: quarterly return dispersion
qret = px.resample("QE").last().pct_change().iloc[1:]
A = qret.std(axis=1)

# B: per-quarter re-based normalized price dispersion, median of daily values
def b_quarter(g):
    norm = g / g.iloc[0]
    return norm.std(axis=1).median()
B = px.groupby(pd.Grouper(freq="QE")).apply(b_quarter)

out = pd.DataFrame({"A_ret_std": A, "B_norm_px_med": B}).dropna(how="all")
out = out[out.index > "2023-01-01"]  # drop the 1-day stub quarter
last_px = px.index.max()
out = out[out.index <= last_px]  # drop in-progress quarter (QE = quarter-end)
BASE_YEARS = [2023, 2024]  # pre-stress; 2025 already had Q2-Q3 stress
base = out[out.index.year.isin(BASE_YEARS)].median()
print("2025 median for comparison:\n",
      out[out.index.year == 2025][["A_ret_std", "B_norm_px_med"]].median().round(4).to_string(), "\n")

def status(v, b):
    return "RED" if v > 2 * b else "AMBER" if v > 1.25 * b else "GREEN"

for col in ["A_ret_std", "B_norm_px_med"]:
    out[col + "_status"] = [status(v, base[col]) for v in out[col]]

print("2023-2024 baseline medians:\n", base.round(4).to_string(), "\n")
print(out.round(4).to_string())
out.round(6).to_csv("results/metric2_bdc_dispersion.csv")
