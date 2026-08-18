# Osberghaus & Schepens (2026) passage check

Source: ECB Working Paper No. 3210 PDF
`https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp3210~e2dc529b33.en.pdf`
PDF metadata DOI `10.2866/9337769` (Handle exists; not in Crossref — not placed as a `10.` token in the draft so `--online` will not false-fail it).

Checked against `dyb-2026k-circular-nw-risk-v2.md` after 2026-08-18 residual pass.

| v2 claim | Source locus | Verdict |
|----------|--------------|---------|
| Banks 57–66% more likely to sell SRTs to investors they also finance | p. 7; Table 10 col. 5 = 57%, col. 6 = 66% | **match** |
| ~26% of SRT funding may trace back to bank credit | p. 7: “on average, 26% of the funding for SRT investments comes from bank credit”; §3.3.1 same, *if the entire pre-deal debt increase is attributed to the SRT* | **match**, with the paper’s “may” hedging the attribution assumption |
| Median junior tranche thickness 15% | p. 12: “the thickness of the junior tranche of the median SRT is 15%” | **match** |
| Monitoring drop 12–25% average | p. 7: “12–25% on average”; Table 9: 12–13% (PD-update dummy), ~26% (SD of PD, caption) | **match** after residual edit (was 12–28%, which blended the SD figure into “frequency”) |
| Entire-exposure drop 35% / 70% | Table 9 col. 3 = 35% (frequency); col. 6 = 70% (SD) | **match** |
| Stock 60bn (2018) → 300bn | Non-technical summary: “from 60 billion euros in 2018 to 300 billion euros at the end of 2024” | **match** after residual edit (was “over 300 … by mid-2024”) |
| 35 banks with >10% of corporate book transferred | p. ~14: “Of the 35 banks that transferred at least 10%” | **match** |
| Transfer probability up to 70% at the SME-factor threshold | p. 6: “increases the likelihood of synthetically transferring a loan by up to 70%” | **match** |
| Asymmetric monitoring (less likely to record deterioration, no change on improvements) | not found in WP 3210 | **removed** from v2 |
| “First academic / transaction-level study” | authors: “first comprehensive study of SRTs”; SUERF brief repeats “first academic study” | **support WARN** (authors’ own claim; not independently verified) |

## BIS (2026) and FSB (2026) — residual pass 2026-08-18

| v2 claim | Source | Verdict |
|----------|--------|---------|
| Almost €800bn outstanding, fivefold since 2016 | BIS QR Mar 2026: “Issuance has increased fivefold since 2016, providing protection to loan portfolios of almost €800 billion as of end-2024.” | **match** (wording tightened from “roughly €800”) |
| North American issuance +400% 2016–2024 | Not in BIS QR. BIS only: NA issuance “has seen an increase… more recently.” | **removed** the 400% figure |
| Top 10 investors hold >75% | IMF WP/25/200, not BIS 2026. BIS: pre-Covid specialised funds were ~¾ of *annual* investment; UK top-10 *sellers* ~60%; top-10 *issuers* 64%. | **re-attributed** to IMF (2025) |
| FSB $1.5–2.0T private credit | FSB May 2026: “between $1.5 trillion and $2 trillion (as at the end of 2024)” | **match** |
| FSB ≥$220bn bank lines; commercial >$500bn | FSB: member data ~$220bn drawn+undrawn; commercial $270–$500bn | **match** after wording tweak |
| FSB uses “circles of risks” | Phrase is BIS QR citing ESRB (2025) “circles of risk” | **re-attributed** to BIS/ESRB |

Not checked: cockpit press snapshots.

§2.3 BIS/BCBS sentence (2026-08-18): the old claim that BIS found “circular leverage” in a “non-trivial fraction” of transactions “without any party intending it” was removed. Replacement matches BIS QR (six risk-transfer chains; “circles of risk” via ESRB; scale “modest”; information gaps) and BCBS d607 (scarce SRT-financing data; supervisors early).
