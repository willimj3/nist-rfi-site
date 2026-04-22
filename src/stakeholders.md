---
title: Stakeholder patterns
---

# Stakeholder-specific patterns

```js
const comments = FileAttachment("data/comments.csv").csv({typed: true});
const themePct = FileAttachment("data/theme_by_stakeholder_pct.csv").csv({typed: true});
```

<div class="note">
Each analytical stakeholder group (n ≥ 5) profiled on its top themes, its dominant stance, whether it flags innovation cost, and whether it endorses mandatory pre-deployment evaluation. These patterns are the main stakeholder-level signal in the corpus.
</div>

## Summary table

```js
const analytical = ["LargeTechCompany", "AIFoundationModelLab", "AIStartup",
                    "EnterpriseSoftwareOrSecurityVendor", "TradeAssociation",
                    "CivilSocietyNGO", "AcademicOrResearchInstitute",
                    "LawFirmOrConsultancy", "Individual"];

const THEME_SHORT = {
  "human_oversight": "Oversight",
  "agent_autonomy": "Autonomy",
  "identity_authentication": "Identity",
  "transparency_documentation": "Transparency",
  "pre_deployment_evaluation": "Pre-eval",
  "supply_chain": "Supply",
  "sandboxing_isolation": "Sandbox",
  "misuse_abuse": "Misuse",
  "red_teaming": "Red-team",
  "mandatory_vs_voluntary": "Mand/Vol",
  "data_provenance": "Provenance",
  "incident_reporting": "Incident",
  "liability": "Liability",
  "international_harmonization": "Harmoniz.",
  "economic_impact": "Cost",
};

const profiles = analytical.map(g => {
  const sub = comments.filter(d => d.stakeholder_type === g);
  if (sub.length < 5) return null;
  const themeCounts = {};
  for (const r of sub) {
    if (!r.top_3_themes) continue;
    for (const t of String(r.top_3_themes).split(";")) {
      const k = t.trim();
      if (k) themeCounts[k] = (themeCounts[k] || 0) + 1;
    }
  }
  const topThemes = Object.entries(themeCounts).sort((a, b) => d3.descending(a[1], b[1])).slice(0, 3);
  const costYes = sub.filter(d => d.emphasizes_innovation_or_compliance_cost === "yes").length / sub.length;
  const evalConditional = sub.filter(d => d.supports_mandatory_pre_deployment_eval === "conditional").length / sub.length;
  const stances = d3.rollups(sub, v => v.length, d => d.overall_stance_on_mandatory_federal_role)
    .map(([k, n]) => [k, n / sub.length])
    .sort((a, b) => d3.descending(a[1], b[1]));
  return {
    group: g,
    n: sub.length,
    topThemes: topThemes.map(([t, n]) => `${THEME_SHORT[t] || t} (${n})`).join(", "),
    cost_yes: (costYes * 100).toFixed(0) + "%",
    eval_conditional: (evalConditional * 100).toFixed(0) + "%",
    top_stance: `${stances[0][0]} (${(stances[0][1]*100).toFixed(0)}%)`,
  };
}).filter(x => x);

display(Inputs.table(profiles, {
  header: {
    group: "Group",
    n: "n",
    top_stance: "Top stance on federal role",
    cost_yes: "% flag cost",
    eval_conditional: "% conditional on eval",
    topThemes: "Top 3 themes",
  },
  columns: ["group", "n", "top_stance", "cost_yes", "eval_conditional", "topThemes"],
  layout: "auto",
}));
```

## Cost-flagging — the cleanest stakeholder split

```js
const costData = [];
for (const g of analytical) {
  const sub = comments.filter(d => d.stakeholder_type === g);
  if (sub.length < 5) continue;
  const yes = sub.filter(d => d.emphasizes_innovation_or_compliance_cost === "yes").length;
  costData.push({group: g, n: sub.length, pct: yes / sub.length * 100, yes});
}
costData.sort((a, b) => d3.descending(a.pct, b.pct));

display(Plot.plot({
  marginLeft: 260,
  marginBottom: 40,
  width: Math.min(width, 780),
  height: 280,
  x: {label: "% of group flagging innovation / compliance cost", domain: [0, 100], grid: true, tickFormat: d => `${d}%`},
  y: {label: null, domain: costData.map(d => d.group)},
  marks: [
    Plot.barX(costData, {y: "group", x: "pct", fill: "#1f4e79", tip: true}),
    Plot.text(costData, {y: "group", x: "pct", text: d => `${d.yes}/${d.n} (${d.pct.toFixed(0)}%)`, dx: 6, textAnchor: "start", fontSize: 11, fill: "currentColor"}),
    Plot.ruleX([0]),
    Plot.ruleX([costData.reduce((a, d) => a + d.yes, 0) / costData.reduce((a, d) => a + d.n, 0) * 100], {stroke: "red", strokeDasharray: "4 4"}),
  ],
}));
```

**Trade Associations (64%) and Law Firms/Consultancies (46%) are the groups most likely to flag innovation cost.** Large Tech is at 36%; Enterprise Security at 25%. Individuals and civil society sit below 20%. This is the single cleanest demographic split in the codebook — the chi-square test confirms it (p<0.001).

## Themes by stakeholder

```js
// theme_by_stakeholder_pct has rows = stakeholder types, columns = themes, values = % of group's top-3 mentions
const themes = Object.keys(themePct[0] || {}).filter(k => k !== "stakeholder_type");
const heat = [];
for (const row of themePct) {
  for (const theme of themes) {
    heat.push({
      group: row.stakeholder_type,
      theme: THEME_SHORT[theme] || theme,
      pct: +row[theme],
    });
  }
}

const groupOrder = themePct.map(d => d.stakeholder_type);

display(Plot.plot({
  marginLeft: 240,
  marginBottom: 80,
  width: Math.min(width, 880),
  height: 340,
  padding: 0.03,
  color: {scheme: "blues", label: "% of group's theme mentions", legend: true, domain: [0, 30]},
  x: {label: null, tickRotate: -40},
  y: {label: null, domain: groupOrder},
  marks: [
    Plot.cell(heat, {x: "theme", y: "group", fill: "pct", tip: true}),
    Plot.text(heat, {x: "theme", y: "group", text: d => d.pct > 5 ? `${d.pct.toFixed(0)}` : "", fontSize: 10, fill: d => d.pct > 15 ? "white" : "black"}),
  ],
}));
```

**What to take away:**

- **Human oversight dominates every group** — it's the corpus's common vocabulary. But look at the second- and third-most-concentrated cells.
- **Enterprise Software & Security vendors over-index on identity** — the IAM-vendor reframing effect visible throughout the corpus.
- **Trade Associations alone concentrate on supply chain and cost** — the industry-policy framing.
- **Academic / Research institutes are the only group with pre-deployment evaluation notably above average** — the push for a real evaluation regime comes from academia, not industry.
- **Individuals are the only group with a meaningful tail into sandboxing and misuse** — they're proposing specific technical architectures rather than policy frames.

---

**Next:** [Notable submissions →](/notable)
