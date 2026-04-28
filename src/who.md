---
title: Who commented
---

# Who commented

```js
const comments = FileAttachment("data/comments.csv").csv({typed: true});
```

<div class="note">
<strong>530 submissions deduplicated to 517 representatives.</strong> The 13 duplicate pairs are submitter revisions (e.g., Pantheon Lab redacting personal info, CTIA filing a replacement). No form-letter campaigns. Everything below uses the representative set unless noted.
</div>

## Stakeholder distribution

```js
const stakeCounts = d3.rollups(comments, v => v.length, d => d.stakeholder_type)
  .map(([stakeholder_type, n]) => ({stakeholder_type, n}))
  .sort((a, b) => d3.descending(a.n, b.n));

display(Plot.plot({
  marginLeft: 260,
  marginBottom: 40,
  width: Math.min(width, 820),
  height: 360,
  x: {label: "# representatives", grid: true},
  y: {label: null, domain: stakeCounts.map(d => d.stakeholder_type)},
  marks: [
    Plot.barX(stakeCounts, {y: "stakeholder_type", x: "n", fill: "#1f4e79", tip: true}),
    Plot.text(stakeCounts, {y: "stakeholder_type", x: "n", text: d => `${d.n} (${(d.n/517*100).toFixed(0)}%)`, dx: 6, textAnchor: "start", fontSize: 11, fill: "currentColor"}),
    Plot.ruleX([0]),
  ],
}));
```

**Individuals are the largest group (40%).** This is unusually high for a NIST-style RFI — most comparable dockets draw a majority of responses from trade associations and large firms. It makes the individual-level signal noisy: you'll see heterogeneous technical proposals rather than coordinated policy positions. Most of the 81 "Other" entries are unclassifiable small LLCs with no AI/security signal in their name; see [Methods](/methods) for how the taxonomy was built.

## Who wasn't there

Three demographic absences are worth flagging explicitly:

- **Only 2 foundation model labs:** Anthropic and OpenAI. No Google DeepMind, Meta AI, Cohere, Mistral, or xAI. Hugging Face also submitted, but is classified as an enterprise-software/dev-platform vendor here rather than a frontier lab — see [Methodology](/methods).
- **Only 1 government entity:** Australia's CSIRO. **No U.S. federal, state, or local agency submitted** — a surprising silence given the policy weight of the docket.
- **No academic legal scholars:** the Academic/Research entries are Johns Hopkins APL and research think tanks (CNAS, CSET, CNA, Heritage), not law school centers.

## Timing

```js
const withDate = comments.filter(d => d["Posted Date"]).map(d => ({
  ...d,
  posted: new Date(d["Posted Date"]),
}));
const byDay = d3.rollups(withDate, v => v.length, d => d3.timeDay(d.posted))
  .map(([date, n]) => ({date, n}))
  .sort((a, b) => d3.ascending(a.date, b.date));

display(Plot.plot({
  marginLeft: 40,
  marginBottom: 55,
  width: Math.min(width, 820),
  height: 260,
  x: {label: "Posted date", type: "time"},
  y: {label: "# submissions", grid: true},
  marks: [
    Plot.rectY(byDay, {x: "date", interval: "day", y: "n", fill: "#1f4e79", tip: true}),
    Plot.ruleY([0]),
  ],
}));
```

**502 of 530 comments were posted on 2026-03-22** — the deadline. The remaining distribution is a thin pre-deadline tail plus a handful of late-accepted filings. This is normal bureaucratic bunching, not a campaign signal.

## Geography

```js
const byCountry = d3.rollups(comments.filter(d => d.Country), v => v.length, d => d.Country)
  .map(([country, n]) => ({country, n}))
  .sort((a, b) => d3.descending(a.n, b.n)).slice(0, 12);

display(Plot.plot({
  marginLeft: 140,
  marginBottom: 40,
  width: Math.min(width, 720),
  height: 300,
  x: {label: "# representatives", grid: true},
  y: {label: null, domain: byCountry.map(d => d.country)},
  marks: [
    Plot.barX(byCountry, {y: "country", x: "n", fill: "#1f4e79", tip: true}),
    Plot.text(byCountry, {y: "country", x: "n", text: "n", dx: 6, textAnchor: "start", fontSize: 11, fill: "currentColor"}),
    Plot.ruleX([0]),
  ],
}));
```

**332 of 517 representatives left the Country field blank** — a data-quality issue caused by regulations.gov's optional submitter fields. Among the 185 who filled it in, the U.S. dominates (139), followed by a suspiciously concentrated cluster of 13 from Chiang Mai, Thailand, then a single-digit tail. Because of the blank-country issue, geographic claims should only be made about the 185 self-identified entries — not extrapolated to the full corpus.

## Heavy hitters

No organization submitted more than 2 comments. The 11 org names that appear twice are all the revision-pairs from the dedup analysis. This confirms [Phase 3](/methods): there's no orchestrated campaign in this corpus.

---

**Next:** [What the RFI asked and where commenters engaged →](/topics)
