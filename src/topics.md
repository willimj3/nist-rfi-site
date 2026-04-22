---
title: Topic-area engagement
---

# What the RFI asked — and where commenters engaged

```js
const prev = FileAttachment("data/topic_area_prevalence.csv").csv({typed: true});
const cov = FileAttachment("data/topic_area_coverage_by_stakeholder.csv").csv({typed: true});
const comments = FileAttachment("data/comments.csv").csv({typed: true});
```

<div class="note">
The RFI groups its questions into <strong>five topic areas</strong>, referenced throughout the corpus as Section 1(a) through 5(e). Each representative was coded for engagement depth per area: <code>substantive</code>, <code>brief</code>, or <code>not_addressed</code>. See <a href="/methods">Methods</a> for the coding schema.
</div>

## Overall engagement

```js
display(Plot.plot({
  marginLeft: 260,
  marginBottom: 40,
  width: Math.min(width, 820),
  height: 300,
  x: {label: "% of representatives (n=517)", domain: [0, 100], grid: true, tickFormat: d => `${d}%`},
  y: {label: null, domain: prev.map(d => d.area_name)},
  color: {legend: true, domain: ["substantive", "brief"], range: ["#1f4e79", "#8db4d2"]},
  marks: [
    Plot.barX(prev, {y: "area_name", x: "substantive_pct", fill: () => "substantive", tip: true}),
    Plot.barX(prev, {y: "area_name", x: d => d.addressed_pct - d.substantive_pct, x1: "substantive_pct", x2: "addressed_pct", fill: () => "brief", tip: true}),
    Plot.text(prev, {y: "area_name", x: "addressed_pct", text: d => `${d.addressed_pct.toFixed(0)}%`, dx: 6, textAnchor: "start", fontSize: 11, fill: "currentColor"}),
    Plot.ruleX([0]),
  ],
}));
```

**Area 3 — pre-deployment evaluation & testing — is the RFI's most-neglected area.** Only 30% of representatives engage substantively; 39% say nothing at all. Compare with Area 1 (83% substantive) and Area 4 (79%). Commenters are comfortable describing the *problem* (agent architecture, threats, runtime defenses) but reluctant to prescribe a *regime* for evaluating agents before they ship. This is the same silence visible in the codebook — 85% of representatives are `conditional` or `unclear` on mandatory pre-deployment evaluation.

## Engagement by stakeholder type

```js
const groups = cov.map(d => d.stakeholder_type);
const areas = ["area_1_substantive_pct","area_2_substantive_pct","area_3_substantive_pct","area_4_substantive_pct","area_5_substantive_pct"];
const areaLabels = {
  "area_1_substantive_pct": "1. Architecture & threat",
  "area_2_substantive_pct": "2. Identity & auth",
  "area_3_substantive_pct": "3. Pre-deploy eval",
  "area_4_substantive_pct": "4. Runtime & incident",
  "area_5_substantive_pct": "5. Governance & supply",
};
const heatmapData = [];
for (const row of cov) {
  for (const col of areas) {
    heatmapData.push({
      group: row.stakeholder_type,
      area: areaLabels[col],
      pct: +row[col],
    });
  }
}

display(Plot.plot({
  marginLeft: 240,
  marginBottom: 80,
  width: Math.min(width, 780),
  height: 360,
  padding: 0.03,
  color: {scheme: "blues", label: "% substantive", legend: true, domain: [0, 100]},
  x: {label: null, tickRotate: -30},
  y: {label: null, domain: groups},
  marks: [
    Plot.cell(heatmapData, {x: "area", y: "group", fill: "pct", tip: true}),
    Plot.text(heatmapData, {x: "area", y: "group", text: d => `${d.pct.toFixed(0)}%`, fontSize: 11, fill: d => d.pct > 55 ? "white" : "black"}),
  ],
}));
```

### What to notice

- **Enterprise Software & Security vendors over-index on Area 2 (identity)** — the IAM-vendor reframing effect. They're comfortable with Area 1 and Area 4, engage moderately on Area 5, and notably avoid Area 3 (25% substantive).
- **Trade Associations are the anomaly** — they're the only group with Area 5 (governance) as their top substantive engagement (76%), matching their lobbying posture.
- **Academic & Research institutes are the push for Area 3.** They're the only group with an Area-3 substantive rate (60%) notably above the corpus average. If mandatory pre-deployment evaluation gets picked up in the final NIST guidance, watch these submissions.
- **Law firms & consultancies** are the least engaged on Area 3 (8%) and Area 5 (46%) — the inverse of what you might expect if you thought legal-sector commenters would carry the policy/evaluation argument.
- **AIFoundationModelLab (n=3, excluded from the heatmap — below the n≥5 threshold for aggregation)** is revealing at the individual level. OpenAI engages substantively on all five areas; Anthropic marks Area 3 as `not_addressed` in its submission; Hugging Face is substantive on Area 1 only.

## What the topic areas are

<div class="grid grid-cols-1">
  <div class="card"><strong>Area 1 — Agent architecture & threat model.</strong> How agents should be characterized; novel risks from agentic behavior (tool use, long-horizon planning, multi-agent coordination); threat taxonomies; what distinguishes agent security from traditional software security.</div>
  <div class="card"><strong>Area 2 — Identity, authentication & delegation.</strong> How agents should be authenticated/authorized; machine identity; delegation of authority from humans to agents; access control; zero-trust frameworks applied to agents.</div>
  <div class="card"><strong>Area 3 — Pre-deployment evaluation & testing.</strong> Evaluations, red-teaming, adversarial testing, audits, benchmarks, assessments conducted <em>before</em> deployment. Risk tiers and what tests fit each tier.</div>
  <div class="card"><strong>Area 4 — Runtime controls, monitoring, incident handling.</strong> Controls active <em>during</em> agent operation: sandboxing, tool-use isolation, human-in-the-loop gating, continuous monitoring, logging, incident detection/reporting, fail-closed architectures.</div>
  <div class="card"><strong>Area 5 — Governance, supply chain & ecosystem.</strong> Governance frameworks; voluntary vs mandatory regimes; supply chain controls; international harmonization; interoperable standards; provenance; NIST's role vs other bodies.</div>
</div>

<div class="note small">
The RFI's literal question text was not retrievable via automated fetch — <code>regulations.gov</code> blocks non-browser user-agents on the document page, and <code>federalregister.gov</code> requires human verification. The five topic areas above were inferred from the structural patterns visible across commenters (the section-numbering convention used by <a href="https://www.regulations.gov/comment/NIST-2025-0035-0282">NIST-2025-0035-0282</a>, the Q-numbering in <a href="https://www.regulations.gov/comment/NIST-2025-0035-0416">NIST-2025-0035-0416</a>, and the thematic consensus across all 517 responses).
</div>

---

**Next:** [Major themes →](/themes)
