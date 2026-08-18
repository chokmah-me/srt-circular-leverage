# Zenodo map — Circular Leverage in Bank-NBFI SRT Networks

Paper and software are **separate concepts**. Do not merge the PDF and the code zip.

| Role | Record | DOI | Notes |
|------|--------|-----|--------|
| Paper **concept** (always latest) | 19632277 | [10.5281/zenodo.19632277](https://doi.org/10.5281/zenodo.19632277) | Live cite for “the paper” |
| Paper **v1** (17 Apr 2026) | 19632278 | [10.5281/zenodo.19632278](https://doi.org/10.5281/zenodo.19632278) | Superseded pin; keep PDF; add Errata notes |
| Paper **v2** (18 Aug 2026) | 21995468 | [10.5281/zenodo.21995468](https://doi.org/10.5281/zenodo.21995468) | Current version of 19632278 |
| Software **concept** | 19651936 | [10.5281/zenodo.19651936](https://doi.org/10.5281/zenodo.19651936) | |
| Software **v1.1** | 19651937 | [10.5281/zenodo.19651937](https://doi.org/10.5281/zenodo.19651937) | Related as `isSupplementedBy` |

GitHub: https://github.com/chokmah-me/srt-circular-leverage

---

## Mint checklist (human)

1. Open https://zenodo.org/records/19632278 → **New version**.
2. Paste **Description**, **Version notes**, **Additional notes**, and **Method** from below.
3. Version: `2.0`. Publication date: `2026-08-18`. Resource type: Preprint. License: CC-BY-4.0. Language: English.
4. Related identifiers: copy the list below.
5. Upload: `dyb-2026k-circular-nw-risk-v2.pdf` (primary), `fig1`–`fig6` PNGs, optional `cockpit_metrics.csv`. Do **not** make the v1 PDF the main file.
6. Publish. Send the new version DOI back so `FIXME`s here and in `CITATION.cff` can be filled.
7. Re-open **v1** (19632278) → Edit → paste **v1 Errata** into Additional notes. Do not replace the v1 PDF.

---

## Description (v2 — paste into Zenodo)

<p>Synthetic Risk Transfers (SRTs) let banks shed credit risk to non-bank financial intermediaries (NBFIs) while keeping the underlying loans on their balance sheets. A structural vulnerability arises when the same banks extend credit lines to the funds that buy their SRT protection, creating a circular leverage loop in which the capital relief is partly self-funded. We formalize this loop as a single parameter, λ, the fraction of total SRT protection weight financed by the originating bank or its affiliates.</p>

<p>Using a directed network model of bank–NBFI SRT relationships, we simulate contagion cascades across 1,000 random network realizations for each λ value. The simulation shows a two-stage phase transition: cascade size first departs from its baseline at λ<sub>onset</sub> ≈ 0.85–0.95, then jumps sharply at λ* ≈ 0.95, where Dragon King events emerge from the loop itself. The transition <em>location</em> is invariant across network density, investor concentration, shock size, and tranche thickness; density controls cascade <em>magnitude</em> at high λ (0.18 to 0.61 in the tested range). A v2 re-run at the empirically observed median junior-tranche thickness δ = 0.15 (Osberghaus and Schepens, 2026) leaves λ* at 0.95; the warning window between onset and cliff narrows.</p>

<p>Since v1 (April 2026), transaction-level ECB AnaCredit evidence shows banks are 57–66% more likely to sell SRTs to investors they also finance, with roughly 26% of SRT funding attributable to bank credit if the pre-deal debt rise is assigned to the SRT (Osberghaus and Schepens, 2026). The FSB (May 2026) reports about $220 billion of official bank credit lines to private credit funds (commercial estimates $270–500 billion). The BIS (March 2026) discusses the same loop as “circles of risk” (ESRB 2025) and characterizes the documented scale as modest given scarce data.</p>

<p>Six public proxy metrics are ranked by sensitivity-weighted ordinal position relative to λ*. As of Q2/Q3 2026, five of six show stress; SOFR–OIS remains green, consistent with its role as a lagging indicator. One number, λ, would let supervisors place banks on the phase diagram. It is already known to each originating bank and is not reported.</p>

<p>This version includes the v2 paper PDF, six figures, and a cockpit CSV. Simulation code is a separate MIT-licensed deposit (10.5281/zenodo.19651937) and <a href="https://github.com/chokmah-me/srt-circular-leverage">github.com/chokmah-me/srt-circular-leverage</a>.</p>

---

## Version notes (v2 — paste)

<p><strong>v2 (17 August 2026)</strong> relative to v1 (17 April 2026):</p>
<ul>
<li>Connects the simulated circular-leverage channel to Osberghaus and Schepens (2026), ECB Working Paper 3210 (AnaCredit): interconnectedness 57–66%, indicative self-funding ~26%, median junior tranche 15%, monitoring reduction 12–25% (35%/70% when the entire firm exposure is transferred).</li>
<li>Adds Figure 6: full 1,000-run sweep at δ = 0.15 versus the paper default δ = 0.08. λ* = 0.95 in both; max |Δμ| within sampling noise; λ<sub>onset</sub> tightens onto λ* at the thicker tranche.</li>
<li>Updates the six-metric cockpit through Q2/Q3 2026 (five of six red; CLO BB–AAA moved from amber/red to red).</li>
<li>Restyles Figures 1–5 for print (shared scales, labeled thresholds, n on-figure).</li>
<li>Corrects v1 citation errors (see Errata on 10.5281/zenodo.19632278): BIS wording, Wosnitza and Sornette (2015) in place of a garbled 2015 cite, IMF not BIS for the 75% top-10 investor figure, Osberghaus monitoring and stock-date wording.</li>
</ul>

---

## Additional notes (v2 — paste)

<p>Concept DOI (always the latest paper version): <a href="https://doi.org/10.5281/zenodo.19632277">10.5281/zenodo.19632277</a>. Pin this record’s version DOI once minted to cite v2 exactly.</p>
<p>Code and figures can be reproduced with <code>python srt_simulation.py</code> (publication Monte Carlo) or <code>python verify_srt_claims.py</code> (thin claim gate, seed 42, n=80). The thin gate does not underwrite the 1,000-run tranche comparison.</p>

---

## Method / AI utilization (v2 — paste)

<p><strong>AI Utilization Statement</strong></p>
<p>v1 was prepared with assistance from Claude Sonnet (Anthropic), Gemini 3.1 (Google), and Kimi 2.5 Thinking (Moonshot), orchestrated through Novakit Utilities v3. AI tools contributed to drafting, critique, code, figure generation, and sensitivity analyses under the author's direction. Final draft inspections used Opus 4.7.</p>
<p>v2 citation checks, figure restyle, manuscript-integrity scan, and release metadata were prepared with assistance from Grok (xAI) under the author's direction. Official-report wording (BIS, BCBS, FSB, Osberghaus and Schepens) was checked against the source PDFs/HTML; remaining errors are the author's.</p>
<p>The research question, parameterization, empirical interpretations, policy recommendations, and all numerical results executed from the simulation code are the author's own.</p>

---

## Related identifiers (v2)

| Identifier | Relation | Type |
|------------|----------|------|
| 10.5281/zenodo.19632278 | isNewVersionOf | DOI (paper v1) |
| 10.5281/zenodo.19632277 | isVersionOf | DOI (paper concept) |
| 10.5281/zenodo.19651937 | isSupplementedBy | DOI (software) |
| https://github.com/chokmah-me/srt-circular-leverage | isSupplementedBy | URL |
| https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp3210~e2dc529b33.en.pdf | cites | URL (Osberghaus &amp; Schepens 2026) |
| 10.5089/9798229027748.001 | cites | DOI (IMF WP/25/200) |
| https://www.bis.org/publ/qtrpdf/r_qt2603c.htm | cites | URL (BIS QR Mar 2026) |
| https://www.bis.org/bcbs/publ/d607.htm | cites | URL (BCBS d607) |
| https://www.fsb.org/uploads/P060526.pdf | cites | URL (FSB May 2026) |

Keywords: synthetic risk transfer; circular leverage; network contagion; phase transition; Dragon King; LPPLS; private credit; systemic risk; NBFI; Basel III; Pillar 3; synthetic securitisation; AnaCredit

---

## v1 Errata (paste onto record 19632278 only)

<p><strong>Errata (18 August 2026).</strong> This file is the 17 April 2026 v1 PDF and is unchanged. The current version is the concept DOI <a href="https://doi.org/10.5281/zenodo.19632277">10.5281/zenodo.19632277</a> (v2, 17 August 2026).</p>
<p>Known issues in v1:</p>
<ol>
<li>The sentence attributing the phrase “circular leverage,” a “non-trivial fraction” of loops, and lack of intent to BIS (2026) is wrong. The BIS Quarterly Review uses “circles of risk” (ESRB 2025), calls the documented scale modest, and does not quantify a fraction or discuss unintentional same-bank circles. The BCBS (2026) report says SRT-financing data are scarce.</li>
<li>“Sandomenico et al. 2015” is a garbled citation. The paper is Wosnitza, J.H., and D. Sornette (2015), <em>Eur. Phys. J. B</em> 88:97, <a href="https://doi.org/10.1140/epjb/e2015-50019-9">10.1140/epjb/e2015-50019-9</a>.</li>
<li>“North American issuance grew 400%” is not in the BIS Quarterly Review.</li>
<li>Osberghaus and Schepens monitoring reduction should read 12–25% on average (not 12–28%). European outstanding SRT stock should read 300 billion euros at end-2024 (not “over 300 billion by mid-2024”).</li>
<li>The finding that the top 10 investors hold over 75% of outstanding SRT exposure is IMF (2025), WP/25/200, not BIS (2026).</li>
</ol>
