---
title: Methodology
---

# Methodology

## Pipeline

The analysis ran as a nine-phase script-driven pipeline. Each phase is idempotent with on-disk caching — any phase can be re-run without repeating prior work.

| Phase | What it did |
|---|---|
| 1 | Load the regulations.gov CSV export (530 rows); count attachments; report shape. |
| 2 | Download all 660 attachment files; extract text (`pdfplumber` → `pypdf` → OCR fallback). |
| 3 | TF-IDF + cosine similarity clustering (≥0.90) to detect form letters. **None found.** 530 → 517 clusters. |
| 4 | Rule-based stakeholder classification (known-entity dictionary + regex) + hand-review of 175 ambiguous orgs. |
| 5 | Descriptive statistics on submitters (distribution, country, timeline). |
| 6 | Keyword-dictionary theme counting (15 themes) + regex citation detection (12 references). |
| 7 | **Structured LLM coding** — Claude Sonnet 4.6 via forced tool use, one call per representative, 12-field codebook. Input capped at 12,000 chars per comment. Cost: ~$11. |
| 8 | Crosstabs of every codebook field vs. stakeholder type; χ² per field; k-means position-space clustering (k=6 by silhouette). |
| 9 | Final synthesis report. |
| 10 | **Post-fix:** verbatim-excerpt repair. Scans each `evidence_excerpt`; if not a substring of the source, swaps in the highest-overlap actual sentence. 105/107 paraphrased excerpts repaired. |
| 11 | **Topic-area coding** — second Sonnet 4.6 pass, 5-area engagement schema. Cost: ~$5. |

## Coding validation

- **Initial verbatim-substring rate on `evidence_excerpt`: 79%** — the remaining 21% were paraphrases despite explicit "verbatim only" instructions.
- **After Phase 10 repair pass: 99.6% (515/517).** Two rows had no high-confidence match and retain their original phrasing.
- Full audit trail in `logs/verbatim_fix_audit.csv`; pre-fix version preserved as `tables/comments_coded_original.csv`.

## Known limitations

- **Blank Country field.** 332/517 representatives left Country blank. Geographic claims should only be made about the 185 self-identified entries.
- **Small-N chi-square.** Many stakeholder × codebook cells have counts under 5. All p-values should be read as directional, not as frequentist hypothesis tests.
- **Topic-area source and scope.** The five topic areas on [topics](/topics) are the verbatim section headings of the RFI (Federal Register 2026-00206), retrieved via the Federal Register JSON API. The RFI contains 24 top-level subquestions across the five topics (5+5+4+5+5). This analysis maps each comment to topic-area engagement at the section level — it does not code engagement per subquestion. Commenters who self-reference 25 or 27 question-level items are typically counting sub-subquestion Roman numerals (e.g. 2(a)(i)-(iii)) as separate questions.
- **LLM coder quirks.** Sonnet 4.6 occasionally produced comma-separated `top_3_themes` where a list was expected, or went ≤10 chars over string-length caps. Validators in `phase_07_code_comments.py` handle both defensively.
- **"Other" category.** 81 of 517 representatives are classified as `Other` — small LLCs with no AI/security signal in their name. Hand-review of those rows in `stakeholder_judgments.csv` would refine this; for now they carry low confidence.
- **Independence.** Each comment was coded independently. Cross-comment context (e.g., "this is the third comment from an identity vendor") was deliberately withheld to avoid priming.

## Stakeholder taxonomy

| Label | Definition |
|---|---|
| `LargeTechCompany` | Major established tech firms (Microsoft, Google, Adobe, Cisco, Intel, etc.) |
| `AIFoundationModelLab` | Frontier AI labs: Anthropic, OpenAI, Hugging Face |
| `AIStartup` | Smaller or less-known AI or AI-security companies |
| `EnterpriseSoftwareOrSecurityVendor` | Non-AI-first software and cybersecurity vendors |
| `TradeAssociation` | Industry groups, chambers, alliances, councils |
| `CivilSocietyNGO` | Advocacy, public-interest, policy non-profits |
| `AcademicOrResearchInstitute` | Universities, research labs, academic-posture think tanks |
| `StandardsOrProfessionalBody` | IEEE, ISO, professional societies |
| `LawFirmOrConsultancy` | Outside counsel or consulting firms commenting on behalf of themselves |
| `GovernmentOrPublicSector` | Domestic or foreign government entities |
| `Individual` | Submitted by a named individual with no organizational affiliation |
| `Other` | None of the above (mostly small unclassifiable LLCs) |

## Codebook fields

| Field | Values | Purpose |
|---|---|---|
| `overall_stance_on_mandatory_federal_role` | supportive / opposed / mixed / unclear | Does the commenter support a mandatory federal role (vs. voluntary/industry-led) in AI agent security? |
| `stance_on_nist_as_standards_body` | supportive / skeptical / neutral / unclear | Does the commenter want NIST specifically to lead this work? |
| `supports_mandatory_pre_deployment_eval` | yes / no / conditional / unclear | Pre-deployment evaluation regime. |
| `supports_incident_reporting_regime` | yes / no / conditional / unclear | Mandatory incident disclosure. |
| `supports_liability_safe_harbor` | yes / no / unclear | Liability protection for good-faith actors. |
| `emphasizes_innovation_or_compliance_cost` | yes / no | Does the comment flag innovation harm or compliance burden? |
| `top_3_themes` | list from 15-theme dictionary | Dominant themes per comment. |
| `specific_recommendations` | free text ≤500 chars | Concrete asks of NIST. |
| `notable_evidence_or_examples` | free text ≤300 chars | Cited incidents, studies, datasets, products. |
| `tone` | technical / policy_advocacy / individual_opinion / commercial_promotion / mixed | |
| `quality` | substantive / light / off_topic / promotional | Coder judgment of analytical depth. |
| `evidence_excerpt` | ≤300-char verbatim quote | Passage supporting the stance tag. |

## Topic-area engagement schema

For each of the 5 topic areas defined on [topics](/topics), each comment was coded `substantive`, `brief`, or `not_addressed`, plus a `primary_topic_area` field (which area is most central) and a short excerpt per non-silent area.

## Data

All coded tables are downloadable as CSV. Links are resolved at build time to the hashed asset URLs.

```js
const datasets = [
  ["comments.csv", "master join: 517 rows, every codebook field + topic-area fields + stakeholder type. Link back to regulations.gov included."],
  ["comments_coded.csv", "Phase 7 output (12-field codebook)."],
  ["comments_topic_areas.csv", "Phase 11 output (5-area engagement)."],
  ["comments_with_stakeholder.csv", "all 530 submissions + stakeholder + cluster info."],
  ["theme_by_stakeholder_pct.csv", "theme × stakeholder aggregate."],
  ["topic_area_coverage_by_stakeholder.csv", "topic × stakeholder aggregate."],
  ["topic_area_prevalence.csv", "overall engagement per area."],
  ["chisquare_summary.csv", "χ² per codebook field vs. stakeholder_type."],
  ["agreement_summary.csv", "consensus/division summary."],
  ["citation_flags.csv", "12 standards/EO citation flags per comment."],
];

const hrefs = {
  "comments.csv": await FileAttachment("data/comments.csv").href,
  "comments_coded.csv": await FileAttachment("data/comments_coded.csv").href,
  "comments_topic_areas.csv": await FileAttachment("data/comments_topic_areas.csv").href,
  "comments_with_stakeholder.csv": await FileAttachment("data/comments_with_stakeholder.csv").href,
  "theme_by_stakeholder_pct.csv": await FileAttachment("data/theme_by_stakeholder_pct.csv").href,
  "topic_area_coverage_by_stakeholder.csv": await FileAttachment("data/topic_area_coverage_by_stakeholder.csv").href,
  "topic_area_prevalence.csv": await FileAttachment("data/topic_area_prevalence.csv").href,
  "chisquare_summary.csv": await FileAttachment("data/chisquare_summary.csv").href,
  "agreement_summary.csv": await FileAttachment("data/agreement_summary.csv").href,
  "citation_flags.csv": await FileAttachment("data/citation_flags.csv").href,
};

display(html`<ul class="download-list">${datasets.map(([name, desc]) =>
  html`<li><a href="${hrefs[name]}" download="${name}">${name}</a> — ${desc}</li>`
)}</ul>`);
```

Data is offered under a <a href="https://creativecommons.org/licenses/by/4.0/">CC-BY 4.0 license</a> — use it, cite it.

## Citation

<div class="citation-block">
Williams, M. (2026). <em>Public Comments to NIST RFI on Security Considerations for Artificial Intelligence Agents: A Content Analysis of Docket NIST-2025-0035.</em> Vanderbilt University MLS Program, AI in Law Practice.
</div>

Source data: NIST docket [NIST-2025-0035](https://www.regulations.gov/docket/NIST-2025-0035) on regulations.gov. 530 public comments, posted 2026-03-15 through 2026-04-07. All comments retrieved 2026-04-20.

---

**Next:** [How this was built →](/how-built)
