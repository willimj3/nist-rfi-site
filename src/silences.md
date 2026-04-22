---
title: The silences
---

# The silences: liability safe harbor and incident reporting

```js
const comments = FileAttachment("data/comments.csv").csv({typed: true});
```

<div class="note">
Two fields in the codebook reveal what the corpus <em>doesn't</em> discuss more than what its stakeholder positions are. These are the fields most directly connected to the legal and regulatory architecture of AI agent risk. If industry were lobbying hardest for safe harbor, or civil society were pushing for mandatory disclosure, the signal would show up here. It doesn't.
</div>

## Incident reporting

```js
const incNonSilent = comments.filter(d => d.supports_incident_reporting_regime && d.supports_incident_reporting_regime !== "unclear");
const incCounts = d3.rollups(incNonSilent, v => v.length, d => d.supports_incident_reporting_regime)
  .map(([k, n]) => ({position: k, n}));

display(Plot.plot({
  marginLeft: 120,
  marginBottom: 40,
  width: Math.min(width, 520),
  height: 140,
  x: {label: "# representatives (of 517)", grid: true},
  y: {label: null, domain: ["yes", "conditional", "no"]},
  marks: [
    Plot.barX(incCounts, {y: "position", x: "n", fill: "#1f4e79", tip: true}),
    Plot.text(incCounts, {y: "position", x: "n", text: d => d.n, dx: 6, textAnchor: "start", fontSize: 11, fill: "currentColor"}),
    Plot.ruleX([0]),
  ],
}));
```

**85% (437 of 517) do not address an incident-reporting regime at all.** Of the 80 who do: 32 `yes`, 47 `conditional`, 1 `no`. Engagement rates by stakeholder type (share of each group that says something non-silent):

```js
const incByGroup = d3.rollups(
  comments,
  v => ({
    non_silent: v.filter(d => d.supports_incident_reporting_regime && d.supports_incident_reporting_regime !== "unclear").length,
    total: v.length,
  }),
  d => d.stakeholder_type
).map(([g, x]) => ({group: g, pct: x.non_silent / x.total * 100, n: x.non_silent, total: x.total}))
 .filter(d => d.total >= 5)
 .sort((a, b) => d3.descending(a.pct, b.pct));

display(Plot.plot({
  marginLeft: 260,
  marginBottom: 40,
  width: Math.min(width, 780),
  height: 280,
  x: {label: "% of group that engages with incident reporting", domain: [0, 30], grid: true, tickFormat: d => `${d}%`},
  y: {label: null, domain: incByGroup.map(d => d.group)},
  marks: [
    Plot.barX(incByGroup, {y: "group", x: "pct", fill: "#1f4e79", tip: true}),
    Plot.text(incByGroup, {y: "group", x: "pct", text: d => `${d.n}/${d.total} (${d.pct.toFixed(0)}%)`, dx: 6, textAnchor: "start", fontSize: 11, fill: "currentColor"}),
    Plot.ruleX([0]),
  ],
}));
```

CivilSocietyNGO is the most engaged group on incident reporting (26% of the group takes a position), but even there the absolute count is small. The 80 voices in favor of *any* incident-reporting regime come from every stakeholder group in proportion to the group's size — there's no single constituency pushing the question.

## Liability safe harbor

```js
const liab = comments.filter(d => d.supports_liability_safe_harbor && d.supports_liability_safe_harbor !== "unclear");
const liabAll = liab.map(d => ({
  id: d["Document ID"],
  org: d["Organization Name"] || "(no org)",
  type: d.stakeholder_type,
  position: d.supports_liability_safe_harbor,
  url: d.regulations_url,
}));
```

```js
display(html`<div class="liability-summary">
  <div class="liability-stat"><span class="big">97%</span> of representatives do not address liability at all.</div>
  <div class="liability-stat"><span class="big">18</span> did. ${liab.filter(d => d.supports_liability_safe_harbor === "yes").length} call for a safe harbor. ${liab.filter(d => d.supports_liability_safe_harbor === "no").length} argue against one.</div>
</div>`);
```

### Every commenter who addressed liability

```js
display(Inputs.table(liabAll, {
  columns: ["id", "org", "type", "position"],
  header: {
    id: "Document ID",
    org: "Organization",
    type: "Stakeholder type",
    position: "Position on safe harbor",
  },
  format: {
    id: (d) => html`<a href="https://www.regulations.gov/comment/${d}" target="_blank">${d}</a>`,
    position: (d) => d === "yes"
      ? html`<span style="color:#2d7a2d;font-weight:600">supports</span>`
      : html`<span style="color:#a03030;font-weight:600">opposes</span>`,
  },
  width: {id: 200, position: 160},
  layout: "auto",
}));
```

**The striking pattern:** among the 18 commenters who engaged with liability, the majority argue *against* safe harbor — and the strongest opposition is not from civil society but from individuals and small security vendors. Industry isn't asking for the protection; independent commenters are arguing against giving it.

## Why this matters

Industry might be expected to lobby hardest for liability safe harbor. It's a familiar ask in every prior tech regulatory debate — Section 230, DMCA, autonomous vehicles, the SAFE Harbor framework of 2000, the patent safe harbors of the Hatch-Waxman Act. Its near-total absence from this RFI is striking. Three plausible explanations, none tested here:

1. **Premature.** Industry may judge that arguing for safe harbor would concede too much about agent liability being a real problem worth addressing.
2. **Wrong venue.** NIST is a standards body, not Congress. Commenters may be saving liability arguments for a different docket or a future legislative ask.
3. **The question was framed narrowly.** The RFI asked about *technical security considerations*, not legal architecture. Legal framing may have been implicitly discouraged.

Whichever is right, a future analysis of legislative comments on AI agent liability — as opposed to this NIST docket — should treat the liability silence here as a baseline rather than as consensus.

---

**Next:** [Stakeholder patterns →](/stakeholders)
