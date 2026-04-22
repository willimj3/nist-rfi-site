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
// Short chart labels — full verbatim headings are in the cards further down.
const TOPIC_SHORT = {
  "Security Threats, Risks, and Vulnerabilities Affecting AI Agent Systems": "1. Threats, risks, vulnerabilities",
  "Security Practices for AI Agent Systems": "2. Security practices",
  "Assessing the Security of AI Agent Systems": "3. Assessing security",
  "Limiting, Modifying, and Monitoring Deployment Environments": "4. Deployment environments",
  "Additional Considerations": "5. Additional considerations",
};
const prevShort = prev.map(d => ({...d, short_name: TOPIC_SHORT[d.area_name] || d.area_name}));

display(Plot.plot({
  marginLeft: 220,
  marginBottom: 40,
  width: Math.min(width, 820),
  height: 300,
  x: {label: "% of representatives (n=517)", domain: [0, 100], grid: true, tickFormat: d => `${d}%`},
  y: {label: null, domain: prevShort.map(d => d.short_name)},
  color: {legend: true, domain: ["substantive", "brief"], range: ["#1f4e79", "#8db4d2"]},
  marks: [
    Plot.barX(prevShort, {y: "short_name", x: "substantive_pct", fill: () => "substantive", tip: true}),
    Plot.barX(prevShort, {y: "short_name", x1: "substantive_pct", x2: "addressed_pct", fill: () => "brief", tip: true}),
    Plot.text(prevShort, {y: "short_name", x: "addressed_pct", text: d => `${d.addressed_pct.toFixed(0)}%`, dx: 6, textAnchor: "start", fontSize: 11, fill: "currentColor"}),
    Plot.ruleX([0]),
  ],
}));
```

**Topic 5 — Additional Considerations — is the RFI's most-neglected section.** Only 22% of representatives engage substantively; 16% don't address it at all. Compare with Topic 2 (85% substantive) and Topic 1 (82%). The RFI itself implicitly weights this section lowest: none of the nine "priority questions" NIST names for bandwidth-limited respondents fall in Topic 5. Commenters are comfortable describing threats (Topic 1), prescribing controls (Topic 2), and discussing deployment constraints (Topic 4), but mostly skip the catch-all section on research priorities, international approaches, and cross-domain insights.

## Engagement by stakeholder type

```js
const groups = cov.map(d => d.stakeholder_type);
const areas = ["area_1_substantive_pct","area_2_substantive_pct","area_3_substantive_pct","area_4_substantive_pct","area_5_substantive_pct"];
const areaLabels = {
  "area_1_substantive_pct": "1. Threats",
  "area_2_substantive_pct": "2. Practices",
  "area_3_substantive_pct": "3. Assessing",
  "area_4_substantive_pct": "4. Deployment envs",
  "area_5_substantive_pct": "5. Additional",
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

- **Enterprise Software & Security vendors dominate Topic 2 (95%) and disappear on Topic 5 (7.5%)** — a 12-fold gap. This group is the clearest example of "happy to talk about technical controls, uninterested in international or cross-domain framing."
- **Trade Associations are the only group engaging Topic 5 at scale** (52% substantive, more than double any other group). Topic 5 covers government-ecosystem collaboration and policy priorities — which is what trade associations are built to address.
- **Academic & Research institutes lead on Topic 3 (Assessing)** at 60% — the highest group rate on the most methodology-heavy section. If NIST picks up specific assessment or evaluation regimes from this RFI, watch academic submissions.
- **Civil society has the weakest engagement on Topic 2 (65%)** — the lowest of any analytical group on an otherwise-near-universal section. Their emphasis is elsewhere (Topic 1, Topic 3).
- **Law Firms & Consultancies concentrate on Topic 4 (Deployment Environments) at 77%** — the second-highest rate among all groups. This is where the legal-community submissions land: constraints on agent action, counterparty risk, rollback mechanisms.
- **AIFoundationModelLab (n=3, excluded from the heatmap — below the n≥5 threshold for aggregation)** is revealing at the individual level. OpenAI engages substantively on all five topics; Hugging Face is substantive on Topics 1, 2, and 4; Anthropic is substantive only on Topic 1. Even the frontier labs don't uniformly address every topic area.

## The five topic areas (verbatim from the RFI)

<div class="grid grid-cols-1">
  <div class="card"><strong>Topic 1 — Security Threats, Risks, and Vulnerabilities Affecting AI Agent Systems.</strong> Unique threats affecting AI agents (distinct from traditional software). How risks vary by model capability, scaffolding, tool use, deployment method, hosting. Whether threats are creating adoption barriers. How threats have evolved and will evolve. Multi-agent-specific threats. <em>5 subquestions.</em></div>
  <div class="card"><strong>Topic 2 — Security Practices for AI Agent Systems.</strong> Technical controls, processes, and practices that could improve agent security — model-level controls, agent system-level controls, and human oversight controls. How practices vary with context, must change as capabilities evolve. Methods for patching and updating. Relevant cybersecurity frameworks and barriers to adopting them. <em>5 subquestions.</em></div>
  <div class="card"><strong>Topic 3 — Assessing the Security of AI Agent Systems.</strong> Methods to anticipate, identify, assess threats during development and to detect incidents after deployment. Alignment with traditional information-security including supply chain. Per-system assessments. Upstream-to-downstream documentation flow. Mandatory-disclosure risks. User-facing documentation for secure deployment. <em>4 subquestions.</em></div>
  <div class="card"><strong>Topic 4 — Limiting, Modifying, and Monitoring Deployment Environments.</strong> Constraining agent deployment environments. Modifying virtual/physical environments; rollback and undo mechanisms. Managing risks of counterparty interactions (with humans, digital resources, mechanical/IoT systems, authentication/OS access vectors, and other agents). Monitoring deployment environments and legal/privacy challenges. Open-internet traffic tracking. <em>5 subquestions.</em></div>
  <div class="card"><strong>Topic 5 — Additional Considerations.</strong> Methods and resources to aid rapid adoption of agent-security practices. Where government-ecosystem collaboration is most urgent. Priority research directions. How other countries address these challenges. Practices and empirical insights from fields outside AI and cybersecurity. <em>5 subquestions.</em></div>
</div>

<div class="note small">
<strong>Priority questions.</strong> The RFI explicitly names nine questions to prioritize for bandwidth-limited respondents: <code>1(a), 1(d), 2(a), 2(e), 3(a), 3(b), 4(a), 4(b), 4(d)</code>. Every topic area except Topic 5 has priority questions — which tells us something about how NIST itself weights the sections.
</div>

<div class="note small">
Topic-area headings are verbatim from the RFI (<a href="https://www.federalregister.gov/documents/2026/01/08/2026-00206/">Federal Register 2026-00206</a>). The RFI contains 24 top-level subquestions (5+5+4+5+5 across the five topics). This analysis codes engagement at the topic-area level, not per subquestion. The analysis was initially run on inferred definitions (the <code>regulations.gov</code> document page blocks non-browser fetches); once the real RFI was retrieved via the Federal Register JSON API, the coding was re-run and this page reflects the corrected numbers.
</div>

---

**Next:** [Major themes →](/themes)
