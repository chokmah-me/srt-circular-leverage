# Patch list: dyb-2026k v2 → v2.1 (Q3 2026 refresh)

Target: `dyb-2026k-circular-nw-risk-v2.md` (repo master). Scope: empirical sections only. No simulation re-run; λ*, λ_onset, density and δ results are untouched.

Rev 2 (14 Oct 2026, evening): folds in the Kimi review after source checks. Changes from rev 1: Metric 4 back to RED (it is a gap metric; BB widened while AAA tightened), Cliffwater "first gate" corrected, redemption trend reframed as "past peak, queues persist", Volta and data-centre SRT material added to §2.5.

Rev 3 (14 Oct 2026, 21:35): Metric 2 computed with `bdc_dispersion.py` (measure B primary, 2023-2024 baseline, rule fixed before the final run). Q3 = AMBER. Q2 restated from RED to AMBER under the pinned rule.

Rev 4 (15 Oct 2026): decision D2 = (a). Metric 5 gets a pinned level rule against a 2023-2024 ISDA baseline, set before ISDA's Q3 data exists. Q3 cell = PENDING; Q2 restated from RED to AMBER under the rule.

Rev 5 (15 Oct 2026): align leftover seams with the paper. Metric 5 red line is $5.7T (2.0 × verified median $2.85T), not the patch's $5.8T from 2.0 × $2.9T rounded. Drop “updated at least monthly” from §6 (Metrics 1–5 are quarterly scores). Metric 6 30/50 bp lines stay in companion code as a tripwire, not the Q3 rule.

**Headline count (Q3 2026): 3 RED / 1 AMBER / 1 GREEN / 1 PENDING.** Metric 2 (BDC dispersion) reads amber; Metric 5 (index CDS) awaits ISDA's Q3 review, due mid-November.

Legend: `OLD` = exact anchor in v2. `NEW` = replacement. `[VERIFY]` = upgrade to a primary source before shipping.

---

## P1. Version line (header)

OLD: `v2: 17 August 2026 (v1: 17 April 2026)`
NEW: `v2.1: [date] 2026 (v2: 17 August 2026; v1: 17 April 2026)`

## P2. Abstract, cockpit sentence

OLD: `As of Q2/Q3 2026, five of six show stress signals, up from four in Q1. SOFR-OIS remains green, consistent with its predicted role as a lagging indicator.`
NEW: `As of Q3 2026, three of six read red, one amber and one green; the CDS index reading awaits ISDA's Q3 data. BDC price dispersion eased from its Q1 extreme, and index CDS activity fell back after a record Q1. SOFR-OIS remains green, consistent with its predicted role as a lagging indicator. v2.1 pins numeric status rules for the dispersion and CDS metrics, which restate both Q2 readings from red to amber.`

## P3. Practitioner summary

OLD: `As of Q2/Q3 2026, five of six are flashing red, up from four in Q1. The CLO BB-AAA spread has moved from amber to red. A new CDS index (FINDX) now provides real-time pricing of private credit sector credit risk.`
NEW: `As of Q3 2026, three of six read red, one amber, one green, and one awaits data. Redemption requests at the largest funds are past their peak, but gates still bind and queues persist. Banks have started tightening leverage lines to private credit funds and limiting how much AI-linked debt they will underwrite. A new CDS index (FINDX) exists but has traded thinly so far.`

Also in the general-public and decision-maker summaries: replace `Five of six warning signs are now showing stress` and `five currently showing stress as of Q2/Q3 2026` with the Q3 count (three red, one amber, one green, one pending).

## P4. New §2.5 (insert after §2.4, before §3)

```
### 2.5 Field evidence since v2 (new in v2.1)

Four developments between August and October 2026 bear on the loop.

**The call channel is live.** Banks have begun tightening back-leverage terms for private credit funds: higher cost, tighter covenants, and reported pauses on new lines (Troutman Pepper Locke, July 2026; Bloomberg, 12 March 2026). In our model this is the step where a distressed bank calls credit lines to funds. The trigger here was loan-value cuts tied to AI disruption, not SRT losses, so this shows the channel operates. It does not show that λ is high.

**Banks are also refusing to warehouse new AI risk.** In October 2026, JPMorgan and Goldman Sachs underwrote only $1.3 billion of a $5 billion loan package for Volta Infrastructure, an AI cloud company, leaving the $3.7 billion GPU-backed tranche to clear on a best-efforts basis at yields near 11% (Bloomberg, 12 October 2026). Apollo reportedly anchored the deal with a $1.5 billion order (Semafor, 13 October 2026). This is a second contraction mechanism, distinct from calling existing lines: banks pass the riskiest AI debt directly to non-bank lenders at origination. Whether those lenders fund the position with bank credit is exactly the quantity λ measures, and it is not disclosed.

**Redemption runs are past peak but queue rather than clear.** Q3 2026 requests eased at several flagship semi-liquid funds, yet gates kept binding (§6, Metric 1). A study of 136 tender-offer filings for ten non-traded BDCs finds requests rose from 1.2% to 6.9% of shares outstanding, with caps binding at seven of ten funds, and that gates defer redemption demand rather than remove it [Research Square, 2026; VERIFY authors]. A fund that cannot shed liabilities depends more on bank lines if its SRT positions draw.

**SRT is moving into concentrated pools, sometimes bought by insiders.** Banks with large AI data-centre exposure have approached investors about SRT structures that move the riskiest tranches off balance sheet while keeping a retained slice (Financial Times, May 2026 [VERIFY: cite FT directly]). TD Bank structured a data-centre SRT with a forward-flow feature that lets the reference pool grow over time (Bloomberg, 22 April 2026), and Deutsche Bank is working on one tied to about €2 billion of project finance debt including data centres (Bloomberg, 7 September 2026). Market participants report that data-centre SRTs price at 7% to 9%, tighter than the 8% to 12% range for broader infrastructure SRTs, and that the typical buyer already holds equity in the underlying assets (Octus, 2026). A protection seller that also owns the reference asset is a wrong-way exposure of the same family as λ: its ability to pay falls exactly when the protected loans fail.
```

## P5. Table 2: add a Q3 column

```
| Rank | Metric | Q1 2026 | Q2 2026 | Q3 2026 | $λ_{trigger}$ (ordinal) | Source |
|------|--------|---------|---------|---------|---------------------|--------|
| 1 | Secondary market pricing / BDC NAV discount | RED | RED | RED | ~0.6 | Setter Capital; BDC prices; tender filings |
| 2 | BDC stock price dispersion | RED | AMBER* | AMBER | ~0.6 | Daily closes; `bdc_dispersion.py` |
| 3 | PIK ratio in BDC 10-Q filings | RED | RED | RED | ~0.6 | SEC EDGAR; Boston Fed |
| 4 | CLO BB minus AAA spread | AMBER/RED | RED | RED | ~0.6 | Valuation Research; SIFMA |
| 5 | CDS index volume / CDX Financials (FINDX) | RED | AMBER* | PENDING | ~0.7 | ISDA SwapsInfo; IFR |
| 6 | SOFR-OIS spread | GREEN | GREEN | GREEN | ~0.8 | FRED; NY Fed |
```

P5b. Caption: replace `Updated in v2 from Q1 to Q2/Q3 2026. Five of six metrics now show red, up from four in v1. Metric 4 (CLO spreads) moved from amber/red to red.` with `Updated in v2.1 to Q3 2026. Metric 2 reads amber; Metric 5 is pending ISDA's Q3 review (mid-November). *Q2 readings for Metrics 2 and 5 are restated from red (v2, judged by eye) to amber under the numeric rules pinned in v2.1; both Q1 readings are red under either method.`

P5c. §6 intro, replace `Each metric is free, updated at least monthly, and connected to either λ or κ via the model.` with `Each metric is free and connected to either λ or κ via the model. Metrics 1–5 are scored quarterly (Metric 5 waits on ISDA's SwapsInfo review); Metric 6 is a daily funding print.`

Note: the v2 column header "Q2/Q3 2026" becomes "Q2 2026", since v2 data ran through July/August.

## P6. Metric 1, append

`Q3 2026 requests eased at several flagship funds but stayed far above caps. Cliffwater's $31 billion interval fund, gated since Q1 (7% paid against about 14% requested), capped Q3 at 5% against about 16% requested, close to Q2's 17% (Private Equity Wire, September 2026). Blue Owl's technology-focused OTIC drew requests near 39% against a 5% cap [VERIFY: tender filing]. Blue Owl halted redemptions from OBDC II entirely earlier in 2026 and began selling assets [VERIFY: date and filing], the terminal state of a queue that does not clear. The UK FCA proposed 90-day notice periods for illiquid retail funds (CP26/35, 8 October 2026). We keep the metric red: the flow of new requests is past peak; the stock of unmet requests is not.`

## P6b. Metric 2, pin the definition and report

After `What it measures: the cross-sectional standard deviation of publicly traded Business Development Company stock prices.` insert:

`v2.1 pins the computation. For each quarter, prices of a fixed 15-name panel (ARCC, OBDC, FSK, GSBD, GBDC, BXSL, MAIN, HTGC, TSLX, OCSL, PSEC, MFIC, CSWC, NMFC, CGBD) are divided by their first close of the quarter, the cross-sectional standard deviation is taken each day, and the quarter's reading is the median of those daily values. Re-basing each quarter removes the drift that comes from normalizing to a single start date. Status is set against the 2023-2024 median (0.037): red above 2.0 times, amber above 1.25 times. The thresholds are judgment calls, like the sensitivity weights. As a robustness check, the dispersion of quarterly total returns gives the same direction but never reaches red.`

Replace `This metric is computable in ten lines of Python from Yahoo Finance.` with `The script is in the repository (bdc_dispersion.py) and writes results/metric2_bdc_dispersion.csv.`

Append: `Readings: Q1 2026 0.074 (2.0 times baseline, red); Q2 0.047 (amber); Q3 0.049 (1.35 times, amber). Dispersion is off its Q1 extreme but has not returned to baseline. The metric is noisy: it read amber in Q1 2023 and Q4 2024 without a matching credit event, and only Q1 2026 crossed the red line in four years of data.`

## P7. Metric 3, append

`Two Q3 readings point in different directions. The BDC median non-accrual ratio reached 2.8% in Q2 2026, the highest since 2017 [VERIFY: primary]. PIK provisions in new loans fell about 46% as lenders tightened terms (WSJ, August 2026 [VERIFY]). The stock of PIK in existing books remains high; the flow is easing. We keep the metric red on the stock.`

## P8. Metric 4, replace `This metric has moved from AMBER/RED to RED since v1.` with

`In Q3 2026, broadly syndicated loan spreads retraced part of the March widening and mezzanine CLO spreads compressed. The BB tranche was the exception: it kept widening modestly while AAA tightened by about 2bp (Valuation Research Corp., Q3 2026). Because the metric is the BB-AAA gap, it widened again in Q3. The reading stays red, though the broader CLO market is calmer than in Q1.`

## P9. Metric 5, correct the FINDX framing

OLD: `FINDX provides something this paper lacked in v1: a real-time, standardized, publicly traded price for private credit sector credit risk. Its creation was, per Woozle Research, "pulled into existence by a market under acute stress."`
NEW: `FINDX gives a standardized price for financial-sector credit risk with some private credit content, but it has traded thinly. It recorded about $1.5 billion of notional in its first four weeks, against $600 billion on CDX IG over the same span, and its spread fell from 109bp at launch to 98bp; dealers described it as a poor proxy for private credit stress (IFR, May 2026). Market-wide index CDS activity also cooled after Q1: traded notional rose 39.8% year on year in Q1 2026 to $7.4 trillion but fell 2.6% in Q2 to $5.1 trillion (ISDA SwapsInfo, May and August 2026). Single-venue figures run hotter (Tradeweb credit derivatives ADV rose 19.6% in Q2 while the market fell), so we do not use them as a market proxy. Under the rule pinned below (P9c), Q1 reads red and Q2 amber; Q3 is pending.`

P9b. Metric 5, replace the v2 Q1 source. OLD: `Q1 2026 CDS index volume reached $4.5 trillion, up 69% year-over-year, the highest on record (Kobeissi Letter, April 2026).` NEW: `Index credit derivatives traded notional reached $7.4 trillion in Q1 2026, up 39.8% year on year, led by CDX IG (ISDA SwapsInfo, May 2026).` Drop the Kobeissi reference; it does not match ISDA's figures and is a social-media source.

## P9c. Metric 5, pin the rule (set before ISDA Q3 data is published)

Insert after the P9 text:

`v2.1 pins the reading. The quarterly value is ISDA SwapsInfo index credit derivatives traded notional (US-reported). Status compares that level to the 2023-2024 median quarter, about $2.85 trillion: red above 2.0 times ($5.7 trillion), amber above 1.25 times ($3.6 trillion). A level rule avoids the base effect in year-on-year growth; Q2 2025 contained the April 2025 tariff shock. Readings: Q1 2026 $7.4 trillion (2.6 times, red); Q2 2026 $5.1 trillion (1.8 times, amber). The index market has grown since 2024 (every 2025 quarter sits near 1.8 times baseline), so this rule leans toward amber in calm periods. FINDX trading is reported as context, not scored.`

Baseline (VERIFY_LOG_v2.1.md, contemporaneous quarterly PDFs): 2023 $3.7, 2.2, 2.7, 2.5; 2024 $2.9, 2.8, 3.8, 3.5. Median $2.85T. Red line is 2.0 × 2.85 = $5.7T (not 2.0 × $2.9T rounded = $5.8T). Amber 1.25 × 2.85 = $3.56T, printed $3.6T. Q1 $7.4T and Q2 $5.1T do not sit on that seam.

## P10. Metric 6, replace `The current spread of approximately 10-15 basis points is within normal bounds.` with

`In early October 2026, SOFR printed at or a few basis points below IORB (3.87% to 3.90%), with the 99th percentile about 5bp above IORB. This holds after the Federal Reserve raised rates on 16 September 2026. Funding markets show no stress. The companion code flags a SOFR–IORB or SOFR–OIS gap above 30 basis points sustained, or 50 basis points once, as a tripwire; those lines are not the Q3 status rule.`

## P11. "The SOFR-OIS result", last two sentences

OLD: `As of Q2/Q3 2026, all five upstream metrics are showing stress. SOFR-OIS is not. This four-month tracking record since v1 provides partial out-of-sample support for the cockpit's ordering: the upstream metrics worsened while the downstream metric stayed flat, consistent with the model's predicted firing sequence.`
NEW: `Through Q2 2026, all five upstream metrics showed stress while SOFR-OIS stayed flat. In Q3, three upstream metrics stayed red, one eased to amber, one awaits data, and SOFR-OIS stayed green through a rate hike. Six months of readings since v1 are consistent with the predicted firing sequence, but they do not separate two stories: an ordinary credit cycle peaking around Q2, or a pause before further stress. The ordering has not been contradicted; it has not been confirmed either.`

## P12. §8, new limitation (insert after "Monitoring degradation..." paragraph)

`**Reference pools are assumed granular.** The model draws the initial shock across a diversified loan pool. SRTs on AI data-centre debt reference a few large, correlated exposures with single-tenant and construction risk, and some are bought by investors who hold equity in the same assets (§2.5). Market participants note that even a 30% data-centre share can erode a thin first-loss tranche (Octus, 2026). In such pools the shock s is lumpy rather than smooth, and tranche thickness δ offers less protection than its nominal size suggests. A v3 extension could draw s from a concentrated, heavy-tailed distribution for a subset of pools, and add a second wrong-way flag for protection sellers that own the reference asset.`

## P13. §9 Conclusion

- OLD: `are, as of Q2/Q3 2026, showing five red and one green.` NEW: `read, as of Q3 2026, three red, one amber and one green, with the CDS index reading pending.`
- OLD: `Since v1, the cockpit's predicted firing sequence has tracked: upstream metrics worsened while the downstream metric stayed flat.` NEW: `Since v1, the downstream metric has stayed flat while upstream metrics worsened, then partly eased.`
- OLD: `The four months since v1` NEW: `The six months since v1`
- After `They have not yet required disclosure, which is not.` add: `Meanwhile banks have begun cutting the leverage lines that close the loop, are passing new AI debt to non-bank lenders at origination, and are transferring data-centre risk through SRTs into pools the model treats as diversified.`

## P14. §7.4 Basel, minor

OLD: `Finalization is expected in late 2026, with implementation in 2027.`
NEW: `The comment period closed on 18 June 2026; as of October 2026 no final rule has been issued.` [VERIFY at ship date]

## P15. References, add

- Bloomberg. (2026, April 22). *TD Bank mulls hedging data center debt with rare SRT deal*. https://www.bloomberg.com/news/articles/2026-04-22/td-bank-mulls-hedging-data-center-debt-with-rare-srt-deal
- Bloomberg. (2026, September 7). *Deutsche Bank hedges data center risk in SRT on €2 billion book*.
- Bloomberg. (2026, October 12). *JPMorgan, Goldman curb exposure on $5 billion Volta AI loan*. https://www.bloomberg.com/news/articles/2026-10-12/jpmorgan-goldman-curb-exposure-on-5-billion-volta-ai-loan-sale
- Financial Times. (2026, May). Banks seek to offload data centre risk. [VERIFY: exact title, URL]
- Financial Conduct Authority. (2026, October 8). *CP26/35*. [VERIFY: URL]
- ISDA. (2026, May 12). *SwapsInfo First Quarter of 2026 Review*. https://www.isda.org/2026/05/12/swapsinfo-first-quarter-of-2026-review/
- ISDA. (2026, August 11). *SwapsInfo First Half of 2026 and the Second Quarter of 2026 Review*. https://www.isda.org/2026/08/11/swapsinfo-first-half-of-2026-and-the-second-quarter-of-2026-review/
- IFR. (2026, May). *CDS traders aren't worried about private credit*. https://www.ifre.com/topic-codes/2434154/cds-traders-arent-worried-about-private-credit
- Octus. (2026). *Investors warn data center SRTs function as asset gathering*. https://octus.com/?p=43623
- Octus. (2026). *SRT Weekly Wrap: High issuance volume meets new reality of risk repricing*. https://octus.com/?p=41215
- Private Equity Wire. (2026, September). Cliffwater Corporate Lending Fund caps Q3 redemptions at 5%. [VERIFY: URL]
- [Authors]. (2026). *Do redemption gates discipline or destabilize? Evidence from the 2026 run on semi-liquid private credit funds*. Research Square. https://www.researchsquare.com/article/rs-10704359/v1
- Semafor. (2026, October 13). *Volta's $5 billion debt deal is a pulse check on the AI-financing boom*. https://www.semafor.com/article/10/13/2026/voltas-5-billion-debt-deal-is-a-pulse-check-on-the-ai-financing-boom
- Troutman Pepper Locke. (2026, July). *Banks are pulling back: What private credit funds need to know now*. https://www.troutman.com/insights/banks-are-pulling-back-what-private-credit-funds-need-to-know-now/
- Valuation Research Corp. (2026). *Structured Products Market Trends: Q3 2026 CLO and ABS Update*. https://www.valuationresearch.com/insights/structured-products-market-trends-q3-2026/

---

## Not used (failed or incomplete verification)

- **Moody's downgrade of major US banks, 28 Sept 2026.** Aggregators only; no Moody's rating action found by either reviewer. Leave out.
- **Blue Owl software-exposure lawsuit (Kimi: OBDC II, case 7:26-cv-03468).** The SEC filing found states the 11.1% vs 20-30% software allegation against **OBDC**, not OBDC II, and the case number was not confirmed. Leave out of v2.1 unless both are checked on PACER/EDGAR.
- **Morgan Stanley 8% software-default projection** (Kimi). No source given; not checked. Leave out.
- **TD SRT "closed" with Blackstone as buyer** (Kimi). Octus implies a TD/Blackstone transaction but does not state the close; P4 says "structured", not "closed".

## Open items before ship

1. Metric 2: done (AMBER). Commit `bdc_dispersion.py` and `results/metric2_bdc_dispersion.csv`; keep both out of `verify_srt_claims.py` (live data, not seeded).
2. Metric 5: PENDING. Apply P9c when ISDA's Q3 SwapsInfo review lands (expect mid-November). Q3 above $5.7T = red, above $3.6T = amber, else green. Decide now whether v2.1 ships before that (with PENDING) or waits.
3. Clear every `[VERIFY]`.
4. Cockpit CSV: the readings are hard-coded in `srt_simulation.py` (`COCKPIT_CURRENT`), so a hand-edited CSV is overwritten on the next run. Apply `cockpit_q3_2026.diff` (`git apply cockpit_q3_2026.diff`), then regenerate. It also drops the old Metric 2 code threshold ("std dev > 15%"), which contradicted P6b. README: fix "Q1 snapshot" and the 5/1 count.
5. CHANGELOG entry; Zenodo v2.1 mint per ZENODO.md.
