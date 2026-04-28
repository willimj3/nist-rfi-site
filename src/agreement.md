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

## What few address

| Field | Dominant value | Share | Note |
|---|---|---:|---|
| Mandatory incident-reporting regime? | **unclear** | 85% | The RFI's Topic 3(a)(i) does ask about post-deployment incident detection, but few comments push for a *mandatory disclosure regime* on top of it. |
| Liability safe harbor? | **unclear** | 97% | The RFI is a technical-security inquiry — it doesn't ask about legal liability. See note below. |

## What everyone hedges on

| Field | Top value | Share | Second value | Share |
|---|---|---:|---|---:|
| Mandatory pre-deployment evaluation? | **conditional** | 51% | **unclear** | 36% |
| Overall stance on mandatory federal role? | **mixed** | 56% | **supportive** | 21% |

**The split is over scope, not principle.** 77% of commenters are supportive-or-mixed on a mandatory federal role. Only 4% are outright opposed. 51% endorse mandatory pre-deployment evaluation *conditionally* (risk-tiered, scope-limited); only 1.4% outright oppose it. This is a corpus of hedged support, not two camps divided across a fault line.

## Where the real splits are

```js
const chi = await FileAttachment("data/chisquare_summary.csv").csv({typed: true});
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

## A note on liability safe harbor

The codebook included a `supports_liability_safe_harbor` field — a holdover from an early draft of the analysis spec that anticipated a typical regulatory-policy docket where industry would predictably push for safe-harbor protection (the pattern in Section 230, autonomous-vehicles, DMCA debates).

The RFI is not that kind of docket. CAISI/NIST framed it as a technical-security inquiry — agent threat models, security practices, deployment-environment controls. Legal liability is not one of the topics, so it is unsurprising that 97% of commenters do not address it.

That said, **18 commenters did volunteer a position** — 14 against a safe harbor, 4 in favor. The 14 against come predominantly from independent commenters and small security vendors; industry trade associations were largely silent. Two readings of this:

- *Strict reading.* Nothing here. Most commenters didn't address safe harbor because the RFI didn't invite them to.
- *Looser reading.* In adjacent dockets industry typically volunteers safe-harbor arguments anyway. Its near-absence here, combined with grassroots opposition from individual commenters who *did* volunteer a position, is at least worth flagging for any future legislative analysis on AI agent liability.

The data is in the [explore tab](/explore/) for anyone who wants to filter on the field.

---

**Next:** [Stakeholder patterns →](/stakeholders)
