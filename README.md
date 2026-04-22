# NIST AI Agent Security RFI — Public Comment Analysis

A content-analysis site for every public comment submitted to NIST's 2026 Request for Information on Security Considerations for Artificial Intelligence Agents (docket [NIST-2025-0035](https://www.regulations.gov/docket/NIST-2025-0035)).

- **Live site:** https://nist-rfi-site.vercel.app
- **Source data:** 530 public comments + 660 attachment files, retrieved from regulations.gov 2026-04-20.
- **Analysis:** 517 deduplicated representatives, each read by Claude Sonnet 4.6 and coded against a 12-field codebook + a 5-area topic-engagement schema. 99.6% of evidence excerpts are verbatim substrings of the source (see `/methods` on the live site).

## Stack

- [Observable Framework](https://observablehq.com/framework/) — static site generator
- Data loaders in Python (`src/data/*.csv.py`)
- Charts via Observable Plot (no custom D3)
- Deployed on Vercel

## Local development

```bash
npm install
npx observable preview        # dev server on http://localhost:3000
npx observable build          # static output in dist/
```

## Data

Every row in `src/data/comments.csv` is a coded representative comment with stakeholder classification, 12-field codebook, topic-area engagement, and the original `regulations.gov` URL. Licensed [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) — use it, cite it.

## Citation

Williams, M. (2026). _Public Comments to NIST RFI on Security Considerations for Artificial Intelligence Agents: A Content Analysis of Docket NIST-2025-0035._ Vanderbilt University MLS Program, AI in Law Practice.

## How it was built

The analysis and this site were built end-to-end using [Claude Code](https://claude.com/claude-code) over the course of an evening, working from a ~40KB natural-language instructions document. The site's `/how-built` page documents the workflow, the real failures encountered, and the checkpoint pattern that made the full pipeline shippable. This project was originally presented as a demo for a Coding Agents workshop.

Contact: [mark.j.williams@vanderbilt.edu](mailto:mark.j.williams@vanderbilt.edu)
