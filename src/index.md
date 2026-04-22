---
title: NIST AI Agent Security RFI — Public Comment Analysis
---

# How industry, labs, and the public told NIST to regulate AI agents

<div class="hero">
<div class="hero-number">499</div>
<div class="hero-caption">Of 517 organizations and individuals that responded to NIST's RFI on AI agent security, <strong>499 said nothing</strong> about whether good-faith developers should get a liability safe harbor. 18 addressed it. 14 of those 18 <em>opposed</em> the idea.</div>
</div>

```js
const comments = FileAttachment("data/comments.csv").csv({typed: true});
const topicPrev = FileAttachment("data/topic_area_prevalence.csv").csv({typed: true});
```

```js
// Hero chart: topic-area engagement — the big pattern
const topicChart = Plot.plot({
  marginLeft: 230,
  marginBottom: 40,
  width: Math.min(width, 800),
  x: {label: "% of representatives (n=517)", domain: [0, 100], grid: true, tickFormat: d => `${d}%`},
  y: {label: null, domain: topicPrev.map(d => d.area_name)},
  color: {legend: true, domain: ["substantive", "brief"], range: ["#1f4e79", "#8db4d2"]},
  marks: [
    Plot.barX(topicPrev, {
      y: "area_name",
      x: "substantive_pct",
      fill: () => "substantive",
      tip: true,
    }),
    Plot.barX(topicPrev, {
      y: "area_name",
      x: d => d.addressed_pct - d.substantive_pct,
      x1: "substantive_pct",
      x2: "addressed_pct",
      fill: () => "brief",
      tip: true,
    }),
    Plot.text(topicPrev, {
      y: "area_name",
      x: "addressed_pct",
      text: d => `${d.addressed_pct.toFixed(0)}% addressed`,
      dx: 6,
      textAnchor: "start",
      fontSize: 11,
      fill: "currentColor",
    }),
    Plot.ruleX([0]),
  ],
});
display(topicChart);
```

**Of the five topic areas the RFI asked about, pre-deployment evaluation is the only one that most commenters can't bring themselves to prescribe a regime for.** 83% have substantive things to say about agent architecture and threats; 79% about runtime defenses. Only 30% engage substantively with evaluation, and nearly 40% don't address it at all. That silence is what this site is about.

---

## At a glance

<div class="grid grid-cols-4">
  <div class="card">
    <h2>530</h2>
    <p>public comments submitted to docket <a href="https://www.regulations.gov/docket/NIST-2025-0035">NIST-2025-0035</a></p>
  </div>
  <div class="card">
    <h2>517</h2>
    <p>deduplicated representatives (no form-letter campaigns detected)</p>
  </div>
  <div class="card">
    <h2>30%</h2>
    <p>substantively engage with <a href="/topics">pre-deployment evaluation</a></p>
  </div>
  <div class="card">
    <h2>97%</h2>
    <p>say nothing about <a href="/silences">liability safe harbor</a></p>
  </div>
</div>

## What to read

<div class="grid grid-cols-2 grid-cols-2-md">
  <div class="card">
    <h3><a href="/silences">The silences</a></h3>
    <p>Liability and incident reporting are the fields where the absence of commentary is the finding. Industry isn't lobbying for safe harbor. Almost nobody is pushing for a disclosure regime.</p>
  </div>
  <div class="card">
    <h3><a href="/topics">Topic-area engagement</a></h3>
    <p>Of the five areas NIST asked about, Area 3 (pre-deployment evaluation) gets the least substantive response — and the push for it comes from academia and civil society, not industry.</p>
  </div>
  <div class="card">
    <h3><a href="/stakeholders">Stakeholder patterns</a></h3>
    <p>Enterprise Software vendors reframe the RFI as an identity-and-access problem. Trade associations flag innovation cost. Individuals propose their own technical frameworks.</p>
  </div>
  <div class="card">
    <h3><a href="/notable">Notable submissions</a></h3>
    <p>Ten comments worth reading in full — a deliberate mix of frontier labs, trade associations, academic research centers, and named individuals.</p>
  </div>
</div>

---

<div class="small note">
<strong>About this project.</strong> A content analysis of every public comment submitted to NIST's 2026 Request for Information on Security Considerations for Artificial Intelligence Agents. Built using the regulations.gov CSV export plus 660 downloaded attachments; each comment was read by Claude Sonnet 4.6 and coded against a 12-field codebook plus a 5-area topic-engagement schema. Validation: 99.6% of evidence excerpts are verbatim substrings of the source (see <a href="/methods">Methodology</a>). Code + CSVs are publicly available.
</div>
