---
title: Explore all 517 comments
---

# Explore all 517 comments

```js
const comments = FileAttachment("../data/comments.csv").csv({typed: true});
```

<div class="note">
Every representative comment with its full coded fields. Filter by stakeholder type, stance, topic-area engagement, or search the recommendations text. Click any Document ID to jump to the original on regulations.gov.
</div>

## Filters

```js
const stakeholderOptions = ["(any)"].concat([...new Set(comments.map(d => d.stakeholder_type))].filter(Boolean).sort());
const stanceOptions = ["(any)", "supportive", "mixed", "opposed", "unclear"];
const nistOptions = ["(any)", "supportive", "neutral", "skeptical", "unclear"];
const evalOptions = ["(any)", "yes", "conditional", "no", "unclear"];
const costOptions = ["(any)", "yes", "no"];
const toneOptions = ["(any)", "technical", "policy_advocacy", "individual_opinion", "commercial_promotion", "mixed"];
const qualityOptions = ["(any)", "substantive", "light", "off_topic", "promotional"];
const primaryTopicOptions = ["(any)", "1", "2", "3", "4", "5", "none"];
```

```js
const stakeholderFilter = Inputs.select(stakeholderOptions, {label: "Stakeholder type", value: "(any)"});
const stakeholder = Generators.input(stakeholderFilter);

const stanceFilter = Inputs.select(stanceOptions, {label: "Stance on federal role", value: "(any)"});
const stance = Generators.input(stanceFilter);

const nistFilter = Inputs.select(nistOptions, {label: "NIST as standards body", value: "(any)"});
const nistStance = Generators.input(nistFilter);

const evalFilter = Inputs.select(evalOptions, {label: "Mandatory pre-deploy eval", value: "(any)"});
const evalStance = Generators.input(evalFilter);

const costFilter = Inputs.select(costOptions, {label: "Flags innovation/cost?", value: "(any)"});
const cost = Generators.input(costFilter);

const toneFilter = Inputs.select(toneOptions, {label: "Tone", value: "(any)"});
const tone = Generators.input(toneFilter);

const qualityFilter = Inputs.select(qualityOptions, {label: "Quality", value: "(any)"});
const quality = Generators.input(qualityFilter);

const primaryTopicFilter = Inputs.select(primaryTopicOptions, {
  label: "Primary topic area",
  value: "(any)",
  format: d => d === "(any)" ? d : d === "none" ? "none" : `Area ${d}`,
});
const primaryTopic = Generators.input(primaryTopicFilter);

const searchFilter = Inputs.search({placeholder: "Search recommendations / excerpt / org…"});
const search = Generators.input(searchFilter);

display(html`<div class="filter-grid">
  <div>${stakeholderFilter}</div>
  <div>${stanceFilter}</div>
  <div>${nistFilter}</div>
  <div>${evalFilter}</div>
  <div>${costFilter}</div>
  <div>${toneFilter}</div>
  <div>${qualityFilter}</div>
  <div>${primaryTopicFilter}</div>
</div>
<div>${searchFilter}</div>`);
```

```js
const filtered = comments.filter(d => {
  if (stakeholder !== "(any)" && d.stakeholder_type !== stakeholder) return false;
  if (stance !== "(any)" && d.overall_stance_on_mandatory_federal_role !== stance) return false;
  if (nistStance !== "(any)" && d.stance_on_nist_as_standards_body !== nistStance) return false;
  if (evalStance !== "(any)" && d.supports_mandatory_pre_deployment_eval !== evalStance) return false;
  if (cost !== "(any)" && d.emphasizes_innovation_or_compliance_cost !== cost) return false;
  if (tone !== "(any)" && d.tone !== tone) return false;
  if (quality !== "(any)" && d.quality !== quality) return false;
  if (primaryTopic !== "(any)" && d.primary_topic_area !== primaryTopic) return false;
  if (search) {
    const q = search.toLowerCase();
    const hay = [d["Organization Name"], d.specific_recommendations, d.evidence_excerpt, d.notable_evidence_or_examples]
      .filter(Boolean).join(" ").toLowerCase();
    if (!hay.includes(q)) return false;
  }
  return true;
});
```

```js
display(html`<p class="result-count"><strong>${filtered.length}</strong> of ${comments.length} comments match.</p>`);

display(Inputs.table(filtered, {
  columns: [
    "Document ID",
    "Organization Name",
    "stakeholder_type",
    "overall_stance_on_mandatory_federal_role",
    "supports_mandatory_pre_deployment_eval",
    "emphasizes_innovation_or_compliance_cost",
    "primary_topic_area",
    "top_3_themes",
    "tone",
    "quality",
  ],
  header: {
    "Document ID": "Doc ID",
    "Organization Name": "Organization",
    "stakeholder_type": "Type",
    "overall_stance_on_mandatory_federal_role": "Stance",
    "supports_mandatory_pre_deployment_eval": "Mand. eval",
    "emphasizes_innovation_or_compliance_cost": "Cost?",
    "primary_topic_area": "Primary area",
    "top_3_themes": "Top themes",
    "tone": "Tone",
    "quality": "Quality",
  },
  format: {
    "Document ID": (d) => html`<a href="https://www.regulations.gov/comment/${d}" target="_blank" rel="noopener" style="font-family: var(--monospace); font-size: 0.85em;">${d}</a>`,
    "Organization Name": (d) => d || "(no org)",
    "top_3_themes": (d) => html`<span style="font-family: var(--monospace); font-size: 0.8em;">${String(d || "").split(";").slice(0, 3).join(", ")}</span>`,
    "primary_topic_area": (d) => d === "none" || !d ? "—" : `Area ${d}`,
  },
  width: {
    "Document ID": 180,
    "Organization Name": 190,
    "stakeholder_type": 170,
    "top_3_themes": 220,
  },
  rows: 20,
  sort: "stakeholder_type",
  layout: "auto",
}));
```

### Drill down into a selected comment

Click any row above to see its full codebook + both coded excerpts.

```js
const selected = view(Inputs.table(filtered, {
  columns: ["Document ID", "Organization Name", "stakeholder_type"],
  header: {"Document ID": "Doc ID", "Organization Name": "Organization", "stakeholder_type": "Type"},
  required: false,
  multiple: false,
  rows: 8,
  width: {"Document ID": 200, "Organization Name": 260},
}));
```

```js
display(selected
  ? html`<div class="detail-card">
      <h3><a href="${selected.regulations_url}" target="_blank" rel="noopener">${selected["Document ID"]}</a> — ${selected["Organization Name"] || "(no org)"}</h3>
      <div class="detail-grid">
        <div><strong>Stakeholder type:</strong> ${selected.stakeholder_type}</div>
        <div><strong>Country:</strong> ${selected.Country || "—"}</div>
        <div><strong>Cluster size:</strong> ${selected.cluster_size}</div>
        <div><strong>Stance (fed role):</strong> <code>${selected.overall_stance_on_mandatory_federal_role}</code></div>
        <div><strong>NIST:</strong> <code>${selected.stance_on_nist_as_standards_body}</code></div>
        <div><strong>Pre-deploy eval:</strong> <code>${selected.supports_mandatory_pre_deployment_eval}</code></div>
        <div><strong>Incident reporting:</strong> <code>${selected.supports_incident_reporting_regime}</code></div>
        <div><strong>Safe harbor:</strong> <code>${selected.supports_liability_safe_harbor}</code></div>
        <div><strong>Flags cost?</strong> <code>${selected.emphasizes_innovation_or_compliance_cost}</code></div>
        <div><strong>Tone:</strong> <code>${selected.tone}</code></div>
        <div><strong>Quality:</strong> <code>${selected.quality}</code></div>
        <div><strong>Primary topic:</strong> <code>${selected.primary_topic_area === "none" ? "—" : `Area ${selected.primary_topic_area}`}</code></div>
      </div>
      <div class="detail-section">
        <strong>Top themes:</strong> ${String(selected.top_3_themes || "").split(";").map(t => t.trim()).filter(Boolean).map(t => html`<code>${t}</code> `)}
      </div>
      <div class="detail-section">
        <strong>Asks of NIST:</strong> ${selected.specific_recommendations || "—"}
      </div>
      <div class="detail-section">
        <strong>Notable evidence:</strong> ${selected.notable_evidence_or_examples || "—"}
      </div>
      ${selected.evidence_excerpt ? html`<blockquote class="detail-excerpt">"${selected.evidence_excerpt}"</blockquote>` : ""}
      <div class="detail-section">
        <strong>Topic-area engagement:</strong>
        <ul class="area-list">
          ${[1,2,3,4,5].map(i => html`<li>Area ${i}: <code>${selected[`area_${i}_engagement`]}</code>${selected[`area_${i}_excerpt`] ? html` — <em>"${selected[`area_${i}_excerpt`]}"</em>` : ""}</li>`)}
        </ul>
      </div>
    </div>`
  : html`<p class="detail-hint">Select a row above to see full detail.</p>`);
```

---

**Next:** [Cross-tab any two fields →](/explore/crosstab)
