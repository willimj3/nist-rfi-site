---
title: Cross-tab any two fields
---

# Cross-tab any two fields

```js
const comments = FileAttachment("../data/comments.csv").csv({typed: true});
```

<div class="note">
Pick any two codebook or stakeholder fields to see how positions distribute. Useful for exploring patterns the narrative pages don't cover — e.g., "how do AIStartups split on tone?" or "is there a topic-area × stance interaction?"
</div>

## Pick two fields

```js
const fields = {
  "stakeholder_type": "Stakeholder type",
  "overall_stance_on_mandatory_federal_role": "Stance on mandatory federal role",
  "stance_on_nist_as_standards_body": "NIST as standards body",
  "supports_mandatory_pre_deployment_eval": "Mandatory pre-deploy eval",
  "supports_incident_reporting_regime": "Incident reporting regime",
  "supports_liability_safe_harbor": "Liability safe harbor",
  "emphasizes_innovation_or_compliance_cost": "Flags innovation/cost",
  "tone": "Tone",
  "quality": "Quality",
  "primary_topic_area": "Primary topic area",
  "Country": "Country",
};

const rowFieldInput = Inputs.select(Object.keys(fields), {label: "Row field", value: "stakeholder_type", format: k => fields[k]});
const colFieldInput = Inputs.select(Object.keys(fields), {label: "Column field", value: "overall_stance_on_mandatory_federal_role", format: k => fields[k]});
const normalizeInput = Inputs.radio(["counts", "row %", "col %"], {label: "Show as", value: "row %"});

const rowField = Generators.input(rowFieldInput);
const colField = Generators.input(colFieldInput);
const normalize = Generators.input(normalizeInput);

display(html`<div class="filter-grid">
  <div>${rowFieldInput}</div>
  <div>${colFieldInput}</div>
  <div>${normalizeInput}</div>
</div>`);
```

```js
// Build the cross-tab
function buildXtab(data, row, col) {
  const rows = new Map();
  for (const d of data) {
    const r = d[row] || "(blank)";
    const c = d[col] || "(blank)";
    if (!rows.has(r)) rows.set(r, new Map());
    rows.get(r).set(c, (rows.get(r).get(c) || 0) + 1);
  }
  // Sort row labels by total count desc; col labels by total count desc
  const rowTotals = [...rows.entries()].map(([k, m]) => [k, [...m.values()].reduce((a, b) => a + b, 0)]).sort((a, b) => d3.descending(a[1], b[1]));
  const colTotals = new Map();
  for (const [, m] of rows) for (const [k, n] of m) colTotals.set(k, (colTotals.get(k) || 0) + n);
  const colOrder = [...colTotals.entries()].sort((a, b) => d3.descending(a[1], b[1])).map(([k]) => k);
  const rowOrder = rowTotals.map(([k]) => k);

  // Flatten into cell array for Plot
  const cells = [];
  for (const r of rowOrder) {
    const total = rowTotals.find(([k]) => k === r)[1];
    for (const c of colOrder) {
      const n = rows.get(r).get(c) || 0;
      const rowPct = total ? n / total * 100 : 0;
      const colPct = (colTotals.get(c) || 0) ? n / colTotals.get(c) * 100 : 0;
      cells.push({row: r, col: c, n, rowPct, colPct, rowTotal: total});
    }
  }
  return {cells, rowOrder, colOrder, rowTotals, colTotals: [...colTotals.entries()]};
}

const xt = buildXtab(comments, rowField, colField);
const valueKey = normalize === "counts" ? "n" : normalize === "row %" ? "rowPct" : "colPct";
const valueFormat = normalize === "counts" ? d => d : d => `${d.toFixed(0)}%`;
```

```js
display(Plot.plot({
  marginLeft: Math.min(240, 8 + d3.max(xt.rowOrder, r => String(r).length) * 7),
  marginBottom: Math.min(120, 30 + d3.max(xt.colOrder, c => String(c).length) * 5),
  width: Math.min(width, 860),
  height: Math.max(240, xt.rowOrder.length * 36),
  padding: 0.03,
  color: {
    scheme: "blues",
    label: normalize === "counts" ? "count" : "%",
    legend: true,
    domain: normalize === "counts" ? undefined : [0, 100],
  },
  x: {label: null, tickRotate: -35, domain: xt.colOrder},
  y: {label: null, domain: xt.rowOrder},
  marks: [
    Plot.cell(xt.cells, {x: "col", y: "row", fill: valueKey, tip: true}),
    Plot.text(xt.cells, {
      x: "col",
      y: "row",
      text: d => valueFormat(d[valueKey]),
      fill: d => {
        // Scale to 0-100 for consistent contrast threshold regardless of mode
        const max = normalize === "counts" ? d3.max(xt.cells, x => x.n) : 100;
        return (d[valueKey] / max) > 0.55 ? "white" : "black";
      },
      fontSize: 11,
    }),
  ],
}));
```

## Raw counts

```js
display(Inputs.table(
  xt.rowOrder.map(r => {
    const row = {[fields[rowField] || rowField]: r, "n (row total)": xt.rowTotals.find(([k]) => k === r)[1]};
    for (const c of xt.colOrder) {
      row[c] = (xt.cells.find(x => x.row === r && x.col === c) || {n: 0}).n;
    }
    return row;
  }),
  {
    layout: "auto",
    rows: 14,
  }
));
```

<div class="note small">
Small-N caveat: many cells have counts under 5. Don't over-interpret differences where the row total is small. When a group has fewer than 5 observations (e.g., AIFoundationModelLab n=2, GovernmentOrPublicSector n=1), the percentage view is unstable.
</div>

---

[← Explore all 517 comments](/explore/) · [Methodology](/methods)
