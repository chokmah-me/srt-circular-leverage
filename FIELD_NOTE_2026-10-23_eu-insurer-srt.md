# Field note — EU guardrails for unfunded insurer SRTs (2026-10-23)

Status: field evidence for §2.5 / §7. **No change to the paper, the cockpit, or any
count.** Filed on branch `v2.1` @ 58dde67. The monitoring baseline for the cockpit
watch remains frozen at 1bf9a51; the one intervening commit (58dde67) touches
AGENTS.md only.

## Sources

- Bloomberg via Asset Securitization Report, 2026-10-19: "EU officials propose
  guardrails for insurance SRT boom" (expert opinion for the European Commission,
  seen by Bloomberg; Commission declined comment).
- Council of the EU press release, 21 Oct 2026 23:17: provisional political
  agreement on the securitisation package.
- European Parliament reporting on the agreement (5% floor figure);
  law-firm summary, 22 Oct 2026 (compromise text not yet published).

## What happened

Commission officials proposed that insurers providing UNFUNDED SRT protection
qualify for the most lenient bank-capital treatment only under extra conditions:
solvency ratios held above set levels for the previous three years; at least two
protection providers per transaction; replacement provisions on rating downgrade;
supervisor assessments of bank concentration via SRTs; EIOPA and ESRB mandated to
assess concentration at insurers. Stated risks of unfunded protection:
counterparty (provider cannot pay), legal (provider disputes the credit event),
settlement/liquidity (delayed payment). AIG 2008 invoked by name. The capital
stake is a 5% vs 7% risk-weight floor on the bank's retained senior tranche.
Market context: insurers expect ~50% more SRT participation in 2026 than 2025
(IACPM survey of 14 insurers/reinsurers); recent unfunded deals at UniCredit,
BNP Paribas, BBVA.

On 21 Oct 2026 the Council and Parliament reached a provisional political
agreement on the package.

## Fact status board

- CONFIRMED: the provisional agreement; the new "resilient" category;
  materially lower capital requirements for low-risk securitisations; targeted
  STS changes enabling insurer/reinsurer participation in synthetic
  securitisation.
- PROVISIONAL: the 5% floor. Parliament reporting names it; its link to the
  resilient category is proposal architecture (June 2025 package analyses:
  5% resilient STS senior vs 7% non-resilient STS), not yet confirmed in the
  agreed text.
- OPINION-GRADE ONLY: every insurer guardrail listed above. None appears in the
  agreement's public summaries; the compromise text is unpublished; formal
  adoption by both co-legislators is still required (in force 20 days after
  Official Journal publication).

## Revised net assessment (post second opinions, 2026-10-23)

1. Numbers: nothing moves. Q3 count stays 3 RED / 1 AMBER / 1 GREEN / 1 PENDING;
   aggregate lambda ~0.26 unchanged; no rescore; no version-bump trigger.
2. Argument: the item is evidence for the paper's supervisory FRAMING (relief
   priced on whether protection actually pays; concentration as a supervisory
   concern; supervision moving past monitoring), NOT for the circular-leverage
   MECHANISM. It contains no evidence about lambda, adopts no lambda disclosure
   and no lambda limit. By enabling the non-lambda insurer channel it may dilute
   aggregate lambda over time — capital rules feed back into market structure,
   which the model (lambda exogenous) does not capture.
3. Modelling: an insurer seller node is a partial extension, not a rebuild. The
   lost-capital-relief propagation channel already covers insurer failure; only
   the credit-line channel is absent. What is missing is the seller FAILURE
   RULE: portfolio-aggregated solvency buffer, cycle-correlated, graded
   (delay / dispute / partial payment) rather than binary. Bias direction:
   correlated seller capital thins the effective buffer in bad states, so the
   channel probably biases toward MORE fragility; the tranche-thickness (delta)
   narrowing result is conditional on the credit-line channel. Ladder:
   limitations paragraph in §8 now; optional labelled uncalibrated scenario
   sweep as v2.2 prep; calibrated simulation only with anchors (Solvency II
   SFCR ratios can bound insurer headroom; SRT-specific exposure per insurer
   and the correlation loading remain unobservable).
4. Data: IF the EIOPA/ESRB mandate survives into the text AND publishes, it
   yields a partial insurer-slice kappa series (one seller class, EU aggregate)
   — useful for §5.3's retained concentration concern, not a per-bank kappa and
   not a lambda substitute. Supervisory bank-concentration assessments are not
   published data by default. The two-provider minimum is a count floor and a
   comparator to the paper's proposed 15–20% single-investor cap, not a share
   cap (a 90/10 split satisfies it).

## Pickup

Monthly field scan (Mon 2026-11-02) to check: (a) has the compromise text been
published? (b) score the five guardrail items individually against it;
(c) confirm what the 5% floor attaches to (resilient category vs asset class).
Field evidence only; no colour change.

## Review provenance

Assessment double-checked 2026-10-23 by two independent second opinions via
OpenRouter at the author's request: Claude Haiku 5.5 (SOUND WITH CAVEATS on all
three sub-answers) and Gemini 4 Argon (headline + Answer 1 SOUND WITH CAVEATS;
Answers 2 and 3 FLAWED, mostly on omissions — relief-loss channel, two-provider
comparator, incentive feedback — all adjudicated into the revised assessment
above). Total second-opinion cost $0.0206. Full record: cockpit watch state
file, goal srt-v2-1-cockpit-monitoring-and-tripwire.
