---
title: NIST AI Agent Security RFI — Public Comment Analysis
---

# How industry, labs, and the public told NIST to regulate AI agents

<div class="hero">
<div class="hero-number">22%</div>
<div class="hero-caption">The RFI asked questions across <strong>five topic areas</strong>. Four of them drew substantive engagement from a majority of the 517 organizations that responded. The fifth — <em>Additional Considerations</em>, covering research priorities, international approaches, and cross-domain insights — drew it from 22%. None of the RFI's nine priority questions fall in that section.</div>
</div>

```js
const comments = FileAttachment("data/comments.csv").csv({typed: true});
const topicPrev = FileAttachment("data/topic_area_prevalence.csv").csv({typed: true});
```

```js
// Short labels for the chart — full verbatim headings are in the cards below.
const TOPIC_SHORT = {
  "Security Threats, Risks, and Vulnerabilities Affecting AI Agent Systems": "1. Threats, risks, vulnerabilities",
  "Security Practices for AI Agent Systems": "2. Security practices",
  "Assessing the Security of AI Agent Systems": "3. Assessing security",
  "Limiting, Modifying, and Monitoring Deployment Environments": "4. Deployment environments",
  "Additional Considerations": "5. Additional considerations",
};
const topicPrevShort = topicPrev.map(d => ({...d, short_name: TOPIC_SHORT[d.area_name] || d.area_name}));

// Hero chart: topic-area engagement — the big pattern
const topicChart = Plot.plot({
  marginLeft: 220,
  marginBottom: 40,
  width: Math.min(width, 820),
  x: {label: "% of representatives (n=517)", domain: [0, 100], grid: true, tickFormat: d => `${d}%`},
  y: {label: null, domain: topicPrevShort.map(d => d.short_name)},
  color: {legend: true, domain: ["substantive", "brief"], range: ["#1f4e79", "#8db4d2"]},
  marks: [
    Plot.barX(topicPrevShort, {
      y: "short_name",
      x: "substantive_pct",
      fill: () => "substantive",
      tip: true,
    }),
    Plot.barX(topicPrevShort, {
      y: "short_name",
      x1: "substantive_pct",
      x2: "addressed_pct",
      fill: () => "brief",
      tip: true,
    }),
    Plot.text(topicPrevShort, {
      y: "short_name",
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

**Of the five topic areas, only "Additional Considerations" fails to draw majority engagement.** 82% have substantive things to say about threats and vulnerabilities (Topic 1); 85% about security practices (Topic 2). But only 22% engage substantively with Topic 5 — and 7.5% of enterprise security vendors engage with it at all. Trade Associations are the only stakeholder group that pushes Topic 5 (52% substantive). The pattern matches the RFI's own framing: the priority questions NIST highlights for bandwidth-limited respondents are concentrated in Topics 1–4.

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
    <h2>22%</h2>
    <p>substantively engage with <a href="/topics">Topic 5 (Additional Considerations)</a></p>
  </div>
  <div class="card">
    <h2>90%</h2>
    <p>support <a href="/agreement">NIST as the standards body</a> for AI agent security</p>
  </div>
</div>

## What to read

<div class="grid grid-cols-2 grid-cols-2-md">
  <div class="card">
    <h3><a href="/topics">Topic-area engagement</a></h3>
    <p>Where commenters engaged across the five topic areas the RFI asked about, broken out by stakeholder type. Topic 5 ("Additional Considerations") is the standout under-engagement.</p>
  </div>
  <div class="card">
    <h3><a href="/agreement">Points of agreement</a></h3>
    <p>The corpus is more hedged than divided: 90% support NIST leading; 51% endorse mandatory pre-deployment evaluation conditionally; only 4% outright oppose a federal role.</p>
  </div>
  <div class="card">
    <h3><a href="/stakeholders">Stakeholder patterns</a></h3>
    <p>Enterprise Software vendors lead on security practices (95%) but avoid "Additional Considerations" almost entirely (7.5%). Trade associations flag innovation cost. Individuals propose their own technical frameworks.</p>
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
