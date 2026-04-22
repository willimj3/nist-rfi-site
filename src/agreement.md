---
title: Points of agreement
---

# Points of agreement

<div class="note">
There are no sharply-divided substantive fields in this corpus. What looks like "division" on a typical regulatory docket — pro-regulation vs anti-regulation, mandatory vs voluntary — is, in this RFI, mostly hedging vs silence.
</div>

## What everyone agrees on

| Field | Consensus value | Share | Note |
|---|---|---:|---|
| Should NIST lead this work? | **supportive** | 90% | Only 2 of 517 reps are skeptical. Universal across stakeholder types. |
| Coding quality | **substantive** | 91% | The corpus is serious. Off-topic / promotional / light comments are <10% combined. |
| Does the comment flag innovation cost? | **no** | 76% | A minority concern overall — but the 24% who do are heavily concentrated in industry. |

## What nobody addresses

| Field | Dominant value | Share | Note |
|---|---|---:|---|
| Mandatory incident-reporting regime? | **unclear** | 85% | Silent, not consensual. See [the silences](/silences). |
| Liability safe harbor? | **unclear** | 97% | Same. Only 18 reps engaged; 14 of them *opposed* safe harbor. |

## What everyone hedges on

| Field | Top value | Share | Second value | Share |
|---|---|---:|---|---:|
| Mandatory pre-deployment evaluation? | **conditional** | 51% | **unclear** | 36% |
| Overall stance on mandatory federal role? | **mixed** | 56% | **supportive** | 21% |

**The cleavage is over scope, not principle.** 77% of commenters are supportive-or-mixed on a mandatory federal role. Only 4% are outright opposed. 51% endorse mandatory pre-deployment evaluation *conditionally* (risk-tiered, scope-limited); only 1.4% outright oppose it. This is a corpus of hedged support, not two camps divided across a fault line.

## Where the real splits are

```js
const chi = FileAttachment("data/chisquare_summary.csv").csv({typed: true});
const relevant = chi.filter(d => d.field !== "supports_liability_safe_harbor" && d.field !== "supports_incident_reporting_regime");
display(Plot.plot({
  marginLeft: 280,
  marginBottom: 40,
  width: Math.min(width, 780),
  height: 220,
  x: {label: "χ² statistic (higher = larger stakeholder split)", grid: true},
  y: {label: null, domain: relevant.sort((a,b) => d3.descending(+a.chi2, +b.chi2)).map(d => d.field)},
  marks: [
    Plot.barX(relevant, {y: "field", x: d => +d.chi2, fill: d => (+d.p_value) < 0.001 ? "#1f4e79" : "#cbd5e1", tip: true}),
    Plot.text(relevant, {y: "field", x: d => +d.chi2, text: d => (+d.p_value) < 0.001 ? `χ²=${(+d.chi2).toFixed(1)}, p<0.001` : `χ²=${(+d.chi2).toFixed(1)}, p=${(+d.p_value).toFixed(2)}`, dx: 6, textAnchor: "start", fontSize: 10, fill: "currentColor"}),
    Plot.ruleX([0]),
  ],
}));
```

Four codebook fields show statistically meaningful stakeholder-level splits (χ² p<0.001):

- **`emphasizes_innovation_or_compliance_cost`** — industry flags cost; individuals and academia don't. See the [stakeholder-pattern heatmap](/stakeholders).
- **`tone`** — industry skews `technical`; individuals skew `individual_opinion` or `mixed`.
- **`overall_stance_on_mandatory_federal_role`** — distribution varies by group, though no group is unified enough to be called "opposed."
- **`supports_mandatory_pre_deployment_eval`** — `conditional` dominates everywhere, but outright `yes` concentrates in individuals and the 3-lab AIFoundationModelLab bucket.

Two fields show **no significant stakeholder difference**: `stance_on_nist_as_standards_body` (everyone is supportive) and `supports_incident_reporting_regime` (everyone is equally silent).

<div class="note small">
Small-N caveat: several stakeholder × codebook cells have counts under 5. Treat p-values as directional, not as hypothesis tests in the frequentist sense.
</div>

---

**Next:** [The silences →](/silences)
