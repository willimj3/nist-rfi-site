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
- **The RFI's literal question text was not retrievable via automated fetch.** `regulations.gov` blocks non-browser user-agents on the document page (the same block that was diagnosed and worked around for attachment downloads — but the workaround didn't extend to the document page itself); `federalregister.gov` requires human verification. The five topic areas on [topics](/topics) were inferred from the structural patterns used by the most-structured commenters (e.g. [0282](https://www.regulations.gov/comment/NIST-2025-0035-0282), [0416](https://www.regulations.gov/comment/NIST-2025-0035-0416)) and thematic consensus across all 517 responses.
- **Topic areas are coarser than "24 questions."** Several commenters explicitly reference 24, 25, or 27 question-level items. This analysis maps to the 5 topic areas, not per-question engagement.
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

All coded tables are downloadable as CSV:

<ul class="download-list">
<li><a href="/data/comments.csv" download>comments.csv</a> — master join: 517 rows, every codebook field + topic-area fields + stakeholder type. Link back to regulations.gov included.</li>
<li><a href="/data/comments_coded.csv" download>comments_coded.csv</a> — Phase 7 output (12-field codebook).</li>
<li><a href="/data/comments_topic_areas.csv" download>comments_topic_areas.csv</a> — Phase 11 output (5-area engagement).</li>
<li><a href="/data/comments_with_stakeholder.csv" download>comments_with_stakeholder.csv</a> — all 530 submissions + stakeholder + cluster info.</li>
<li><a href="/data/theme_by_stakeholder_pct.csv" download>theme_by_stakeholder_pct.csv</a> — theme × stakeholder aggregate.</li>
<li><a href="/data/topic_area_coverage_by_stakeholder.csv" download>topic_area_coverage_by_stakeholder.csv</a> — topic × stakeholder aggregate.</li>
<li><a href="/data/topic_area_prevalence.csv" download>topic_area_prevalence.csv</a> — overall engagement per area.</li>
<li><a href="/data/chisquare_summary.csv" download>chisquare_summary.csv</a> — χ² per codebook field vs. stakeholder_type.</li>
<li><a href="/data/agreement_summary.csv" download>agreement_summary.csv</a> — consensus/division summary.</li>
<li><a href="/data/citation_flags.csv" download>citation_flags.csv</a> — 12 standards/EO citation flags per comment.</li>
</ul>

Data is offered under a <a href="https://creativecommons.org/licenses/by/4.0/">CC-BY 4.0 license</a> — use it, cite it.

## Citation

<div class="citation-block">
Williams, M. (2026). <em>Public Comments to NIST RFI on Security Considerations for Artificial Intelligence Agents: A Content Analysis of Docket NIST-2025-0035.</em> Vanderbilt University MLS Program, AI in Law Practice.
</div>

Source data: NIST docket [NIST-2025-0035](https://www.regulations.gov/docket/NIST-2025-0035) on regulations.gov. 530 public comments, posted 2026-03-15 through 2026-04-07. All comments retrieved 2026-04-20.

---

**Next:** [How this was built →](/how-built)
