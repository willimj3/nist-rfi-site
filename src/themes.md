---
title: Major themes
---

# Major themes

```js
const comments = FileAttachment("data/comments.csv").csv({typed: true});
```

```js
// Aggregate top_3_themes into per-theme counts
const themeCounts = {};
for (const r of comments) {
  if (!r.top_3_themes) continue;
  for (const t of String(r.top_3_themes).split(";")) {
    const k = t.trim();
    if (!k) continue;
    themeCounts[k] = (themeCounts[k] || 0) + 1;
  }
}
const themeData = Object.entries(themeCounts)
  .map(([theme, n]) => ({theme, n, pct: n/517*100}))
  .sort((a, b) => d3.descending(a.n, b.n));

const themeShort = {
  "human_oversight": "Human oversight",
  "agent_autonomy": "Agent autonomy",
  "identity_authentication": "Identity & authentication",
  "transparency_documentation": "Transparency / documentation",
  "pre_deployment_evaluation": "Pre-deployment evaluation",
  "supply_chain": "Supply chain / third-party",
  "sandboxing_isolation": "Sandboxing / isolation",
  "misuse_abuse": "Misuse / abuse",
  "red_teaming": "Red teaming",
  "mandatory_vs_voluntary": "Mandatory vs voluntary",
  "data_provenance": "Data provenance / watermarking",
  "incident_reporting": "Incident reporting",
  "liability": "Liability",
  "international_harmonization": "Intl. harmonization",
  "economic_impact": "Innovation / compliance cost",
};

display(Plot.plot({
  marginLeft: 220,
  marginBottom: 40,
  width: Math.min(width, 820),
  height: 420,
  x: {label: "% of representatives with theme in top-3", domain: [0, 100], grid: true, tickFormat: d => `${d}%`},
  y: {label: null, domain: themeData.map(d => themeShort[d.theme] || d.theme)},
  marks: [
    Plot.barX(themeData, {y: d => themeShort[d.theme] || d.theme, x: "pct", fill: "#1f4e79", tip: true}),
    Plot.text(themeData, {y: d => themeShort[d.theme] || d.theme, x: "pct", text: d => `${d.pct.toFixed(0)}%`, dx: 6, textAnchor: "start", fontSize: 11, fill: "currentColor"}),
    Plot.ruleX([0]),
  ],
}));
```

**Human oversight is the overwhelming consensus theme** — 88% of representatives list it in their top-3. The RFI's framing has effectively centered the field on human-in-the-loop and human-on-the-loop designs. Four themes are mentioned by 80%+ of commenters; `incident_reporting` and `liability` sit at the bottom, each under 13% — consistent with the RFI's framing as a technical-security inquiry rather than a legal/regulatory policy docket. See [Points of agreement → A note on liability safe harbor](/agreement#a-note-on-liability-safe-harbor).

## Verbatim excerpts per theme

Quotes below are verbatim passages pulled from each commenter's own text. Validation: 99.6% of these excerpts are exact substrings of the source (see [Methods](/methods)).

```js
// Helper: find two exemplar comments per theme from diverse stakeholder types
function exemplarsFor(theme, k = 2) {
  const matches = comments.filter(d =>
    d.top_3_themes && String(d.top_3_themes).includes(theme)
    && d.quality === "substantive"
    && d.evidence_excerpt && d.evidence_excerpt.length > 80
  );
  const seen = new Set();
  const out = [];
  for (const r of matches.sort((a, b) =>
    d3.descending((a.evidence_excerpt || "").length, (b.evidence_excerpt || "").length))) {
    if (!seen.has(r.stakeholder_type)) {
      seen.add(r.stakeholder_type);
      out.push(r);
      if (out.length >= k) break;
    }
  }
  return out;
}

const topThemes = themeData.slice(0, 6).map(d => d.theme);
```

```js
function themeSection(theme) {
  const label = themeShort[theme] || theme;
  const n = themeCounts[theme];
  const exemplars = exemplarsFor(theme, 2);
  return html`<div class="theme-section">
    <h3>${label} <span class="theme-pct">${(n/517*100).toFixed(0)}% (${n} reps)</span></h3>
    ${exemplars.map(r => html`
      <blockquote>
        "${r.evidence_excerpt}"
        <footer>
          <a href="${r.regulations_url}" target="_blank" rel="noopener">${r["Document ID"]}</a>
          — ${r["Organization Name"] || "(no org)"}
          · <em>${r.stakeholder_type}</em>
        </footer>
      </blockquote>
    `)}
  </div>`;
}

display(html`<div>${topThemes.map(themeSection)}</div>`);
```

---

**Next:** [Points of agreement →](/agreement)
