---
title: Notable submissions
---

# Notable individual submissions

```js
const comments = FileAttachment("data/comments.csv").csv({typed: true});
```

<div class="note">
Ten substantive, well-identified submissions worth reading in full. Picks ensure at least one per major stakeholder type plus a dissenting voice (Google, opposed) and a substantive named individual. Every row links to the original comment on regulations.gov.
</div>

```js
// Reproduce the phase_09 selection logic so the page always matches
// what the final report says.
const pool = comments.filter(d =>
  d.quality === "substantive" &&
  d.specific_recommendations && d.specific_recommendations.length > 80
);

const mandatoryTypes = [
  "AIFoundationModelLab", "LargeTechCompany",
  "EnterpriseSoftwareOrSecurityVendor", "TradeAssociation",
  "CivilSocietyNGO", "AcademicOrResearchInstitute",
  "StandardsOrProfessionalBody", "AIStartup",
];

const notable = [];
const usedIds = new Set();

for (const t of mandatoryTypes) {
  const sub = pool
    .filter(d => d.stakeholder_type === t && d["Organization Name"] && d["Organization Name"].length > 2)
    .sort((a, b) => d3.descending((a.specific_recommendations || "").length, (b.specific_recommendations || "").length));
  if (sub.length) {
    const r = sub[0];
    notable.push(r);
    usedIds.add(r["Document ID"]);
  }
}

// Dissenting voice
const dissent = pool
  .filter(d => !usedIds.has(d["Document ID"]) &&
    (d.overall_stance_on_mandatory_federal_role === "opposed" ||
     d.supports_mandatory_pre_deployment_eval === "no"))
  .sort((a, b) => d3.descending((a.specific_recommendations || "").length, (b.specific_recommendations || "").length));
if (dissent.length) {
  notable.push(dissent[0]);
  usedIds.add(dissent[0]["Document ID"]);
}

// Substantive individual
const ind = pool
  .filter(d => !usedIds.has(d["Document ID"]) && d.stakeholder_type === "Individual")
  .sort((a, b) => d3.descending((a.specific_recommendations || "").length, (b.specific_recommendations || "").length));
if (ind.length) {
  notable.push(ind[0]);
  usedIds.add(ind[0]["Document ID"]);
}

while (notable.length < 10) {
  const more = pool
    .filter(d => !usedIds.has(d["Document ID"]) &&
      (d.stakeholder_type === "TradeAssociation" || d.stakeholder_type === "CivilSocietyNGO"))
    .sort((a, b) => d3.descending((a.specific_recommendations || "").length, (b.specific_recommendations || "").length));
  if (!more.length) break;
  notable.push(more[0]);
  usedIds.add(more[0]["Document ID"]);
}
```

```js
display(html`<div class="notable-list">
  ${notable.map(r => html`
    <article class="notable-item">
      <h3>
        <a href="${r.regulations_url}" target="_blank" rel="noopener">${r["Document ID"]}</a>
        — ${r["Organization Name"] || "(no org)"}
      </h3>
      <div class="notable-meta">
        <span class="stakeholder-tag">${r.stakeholder_type}</span>
        <span>Stance: <code>${r.overall_stance_on_mandatory_federal_role}</code></span>
        <span>NIST role: <code>${r.stance_on_nist_as_standards_body}</code></span>
        <span>Pre-deploy eval: <code>${r.supports_mandatory_pre_deployment_eval}</code></span>
      </div>
      <div class="notable-themes">
        <strong>Top themes:</strong> ${String(r.top_3_themes || "").split(";").map(t => t.trim()).filter(Boolean).map(t => html`<code>${t}</code>`)}
      </div>
      <div class="notable-asks">
        <strong>Asks of NIST:</strong> ${r.specific_recommendations}
      </div>
      ${r.evidence_excerpt ? html`<blockquote class="notable-excerpt">"${r.evidence_excerpt}"</blockquote>` : ""}
    </article>
  `)}
</div>`);
```

---

**Next:** [Methodology →](/methods)
