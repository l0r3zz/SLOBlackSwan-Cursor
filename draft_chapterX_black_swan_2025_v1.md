# Cursor Multi-Agent Authoring Workflow Guide

## Scenario
**Query:** Research recent black swan incidents in 2025.

---

### Step 1: Research Phase

- **Launch Cursor 2.0, select Research Agent.**
- *Prompt:*
  Research recent black swan incidents in 2025 in tech infrastructure. Summarize why each event was unpredictable, its impact, and include sources/citations. Output markdown in template, save as outputs/research/research_black_swan_2025.md.

- **Checkpoint:**  
  Review `research_black_swan_2025.md` for at least 3 events, source links/citations in place.

---

### Step 2: Drafting

- **Switch to Writing Agent.**
- *Prompt:*
  Draft a section for Chapter X using the research file as input. Begin with an overview, then summarize each event in detail, end with SRE implications.
  Save as outputs/drafts/draft_chapterX_black_swan_2025_v1.md.

- **Checkpoint:**  
  Confirm `draft_chapterX_black_swan_2025_v1.md` is structured, readable, and relevant.

---

### Step 3: Critique

- **Switch to Critique Agent.**
- *Prompt:*
  Review draft for clarity, completeness, and actionable insights per book/cursor rules. Output strengths, issues, suggestions as markdown critique to outputs/critiques/critique_chapterX_black_swan_2025.md.

- **Checkpoint:**  
  Critique file includes well-defined feedback. Note improvements for next iteration.

---

### Step 4: Technical Validation

- **Switch to Technical Validator Agent.**
- *Prompt:*
  Validate all technical claims, highlight gaps or outdated info, note missing citations. Save as outputs/critiques/validation_chapterX_black_swan_2025.md.

- **Checkpoint:**  
  Validation report lists all flagged issues, technical confirmations, or needed corrections.

---

### Step 5: Organize & Stage

- **Run:**
  python scripts/organize_outputs.py --chapter X

  Outputs move to staging/ready-for-scrivener/Chapter_X, manifest generated.

- **(Optional) Convert Markdown to RTF:**
  python scripts/convert_to_rtf.py --input staging/ready-for-scrivener/Chapter_X

- **Review all files in the staging folder for completeness and naming.**

---

### Step 6: Import to Scrivener

- **Batch review, drag and drop all staged files into Scrivener Binder for Chapter X.**
- Assign appropriate subfolders (drafts, research, critique, validation).
- Verify formatting, structure, and citations post-import.

---

### Step 7: QA and Version Control

- Confirm import accuracy by reading in Scrivener.
- Tag git with import milestone for rollback/versioning.

---

### Iteration & Improvement

- If feedback requires edits, repeat Writing → Critique → Validation → Organize steps, using incremented version filenames.
- Document changes for future chapters or queries.

---

## Best Practices

- Save outputs by agent, type, and version for audit/history.
- Do all reviews and checkpoints before final import into Scrivener.
- Use git for both workspace and script versioning.
- Adjust prompts/templates as the book’s style evolves.

---

## Troubleshooting

- Agent errors: check API keys, quotas, prompt formatting.
- Missing files: rerun agent with new filename, audit manifest.
- Import errors: verify file compatibility, run conversion utility.

---

**End of Workflow Guide**

