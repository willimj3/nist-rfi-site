---
title: How this was built
---

# How this was built

This site and the analysis behind it were built end-to-end using Claude Code as the coding agent, working from a ~40KB natural-language instructions document ([`nist_rfi_analysis_instructions.md`](https://www.regulations.gov)). The instructions specified nine analysis phases with human checkpoints; Claude Code wrote the scripts, diagnosed the failures, and shipped the result. Total elapsed human time was roughly an evening; total API spend across the project was ~$16.

## The workflow

1. **Author instructions once.** A carefully-written analysis spec — phases, checkpoints, codebook, guidelines — becomes the contract between the user and the agent.
2. **Let the agent scaffold.** Each phase became a standalone, idempotent Python script under `outputs/scripts/` — `phase_01_orientation.py`, `phase_02_download_and_extract.py`, and so on. Idempotency matters: Phase 2's 660-file download was re-run after the first attempt 403'd on every request, because the agent's local cache made the retry free.
3. **Checkpoint at every phase.** The workflow never ran end-to-end unattended. Each phase produced a markdown summary that fit on one screen, and the user explicitly approved (or redirected) before the next phase began. This is how the "paraphrased excerpts" problem in Phase 7 got caught and fixed in Phase 10.
4. **Let the agent fix its own mistakes.** The `regulations.gov` 403 block, the rate-limit 429 burst on Sonnet, the comma-vs-semicolon theme list parsing, the 99.6%→100% verbatim rate — each of these was a real failure that the agent diagnosed and resolved without human code-editing.

## Claude Code features the project exercised

- **Plan mode** for decomposing nine phases into scripts.
- **Background shell jobs** for long downloads and LLM coding runs, with completion notifications routed back into the conversation.
- **Subagents** for parallel research (e.g., fetching Observable Framework docs while writing the site structure).
- **MCP servers** — the Vercel MCP was available for one-step deploy, though v1 of this site is still local.
- **The `claude-api` skill** for the LLM coding passes (Phase 7, Phase 11) — the skill surfaces current Sonnet syntax, prompt-caching patterns, and tool-use schemas that are too fast-moving to memorize.
- **Task tracking** for this final site build — each page was a tracked task, checked off as complete.

## Things that didn't work on the first try

Writing these down because they're the interesting part:

- **Phase 2 attachments downloaded in 60 seconds — all 403.** The fast completion should have looked suspicious; it did, only after the agent reported the status. regulations.gov's CDN rejects non-browser `User-Agent` strings. Fix: browser-like UA + `From:` header with the author's email (the HTTP-polite way to advertise yourself).
- **Phase 7 coding: 93% of the first run errored.** Two causes: 6 parallel workers hit the per-account concurrent-request tier cap, and Sonnet occasionally produced evidence excerpts 10 characters over the 300-char schema limit. Fix: 2 workers + pre-trim before validation.
- **Phase 7 verbatim rate: 79%.** Sonnet paraphrased even when told not to. Fix was a post-processing pass (Phase 10) that swaps each paraphrased excerpt with the highest token-Jaccard-overlap actual sentence from the source. 79% → 99.6%.
- **Phase 11: 15 consecutive rate-limit errors mid-run.** The SDK's default retry policy isn't aggressive enough at the 2-worker throughput ceiling for this tier. Fix was trivial (re-run with cache), but the pattern should be surfaced: if you see a contiguous block of errors in a Sonnet batch, it's almost certainly a rate-limit burst, not a content issue.
- **Observable Framework complaining about `export`.** A missing `"type": "module"` in `package.json` — a five-minute distraction, but the kind of thing that derails workshops.
- **Inferred topic-area definitions were wrong.** The first Phase 11 run used topic definitions I had *inferred* from the corpus because `regulations.gov` blocks non-browser fetches on the RFI document page. When a human reader pointed out the mismatch, the actual RFI text was retrieved via the Federal Register JSON API (`/api/v1/documents/2026-00206.json` returns `raw_text_url`, which serves the full text with a browser UA). The coding pass was re-run against the verbatim headings, producing a materially different result — Topic 5 ("Additional Considerations") is the least-engaged section, not Topic 3 as initially reported. **This is the failure mode that most matters for agentic research**: when a data source is inaccessible, an agent will confidently fill the gap with inference, and the inference can be convincing enough that downstream analysis feels right. The fix is human review of any inferred definition, and a second pass once the ground truth is recovered.

## Reproducibility

The full pipeline is available at (repo link TBD). To reproduce:

```bash
# Prerequisites: Python 3.11+, Node 18+, Homebrew (for pdftoppm/tesseract),
# ANTHROPIC_API_KEY environment variable.

pip install -r requirements.txt
python3 outputs/scripts/phase_01_orientation.py
# ... continue through phase_11.
# Each phase is idempotent; caches make re-runs cheap.

# Build this site:
cd site
npm install
npx observable preview
```

## Why Observable Framework for the site

- **Markdown + inline JavaScript.** Every page is a `.md` file with `.js` chart cells. No separate templating layer.
- **Static by default.** `observable build` produces plain HTML/CSS/JS. Deploys to Vercel, Netlify, GitHub Pages, or any static host.
- **Data loaders.** A `.csv.py` file becomes a CSV at build time — the data layer is code.
- **Built-in Plot.** Observable Plot handles the chart syntax without a heavy D3 setup.
- **Academic typography out of the box.** No design work needed for credible research-publication look.

## What this demonstrates about coding agents

Three things:

1. **The bottleneck is writing a good spec, not implementing it.** The 40KB instructions file was the real intellectual work. Once that was right, building took an evening.
2. **Checkpointing is the safety layer that makes autonomy safe.** Every phase produced a human-readable summary before the agent moved on. The paraphrased-excerpt issue would have shipped unnoticed without that checkpoint.
3. **Failures are diagnostic, not terminal.** Each time a phase failed, the agent was able to read the error output, propose a hypothesis, test it, and ship the fix. That loop — not any single feature — is what makes coding agents viable for real research work.

---

**Built by Mark Williams, Professor of the Practice, Vanderbilt Law School.** Questions? [mark.j.williams@vanderbilt.edu](mailto:mark.j.williams@vanderbilt.edu).
