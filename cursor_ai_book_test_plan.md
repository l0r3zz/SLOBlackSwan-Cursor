# Cursor Multi-Agent Book Workflow
# Unit & Integration Test Plan

## Overview

This plan covers Testing for a multi-agent authoring process in Cursor 2.0, Python workflow automation, and Scrivener import.

---

## Unit Test Cases

**Research Agent**
- Accepts varied queries (edge cases, typos).
- Produces citations in markdown.
- Handles API failures and empty results gracefully.
- Conforms to research template.

**Writing Agent**
- Processes outline and research inputs.
- Keeps markdown structure.
- Handles context window limits (large research).
- Stores outputs with correct file naming.

**Critique Agent**
- Reads drafts in various markdown formats.
- Outputs reviews with strengths/issues/suggestions.
- Identifies incomplete or ambiguous drafts.
- Handles missing source files cleanly.

**Technical Validation Agent**
- Verifies factual claims, citations, code blocks.
- Outputs validation as markdown bullets.
- Handles missing, outdated, or ambiguous content.

**Python Helper Scripts**
- Moves/organizes drafts, research, critique by chapter.
- Generates accurate manifest files.
- Converts `md` to `rtf` correctly for all cases.
- Handles missing files, folder conflicts, permission errors.

---

## Integration Test Cases

**Multi-Agent Workflow**
- Research → Draft → Critique → Validation flows in parallel.
- Outputs correctly routed/named by agent and section.
- No data is lost or overwritten.

**Automation Layer**
- Helper script collects .md files in correct staging folders.
- All markdowns convert to .rtf as needed.
- Manifest matches all imported files.

**Human-in-the-Loop QA**
- Reviewer can batch-compare agent outputs.
- Reviewer can rename/exclude/add frontmatter before import.
- Drag/drop import into Scrivener works for the batch.

**Edge Case/Failure Scenarios**
- Simulate agent API failure/malformed output.
- Malformed markdown flagged, does not disrupt workflow.
- Large queries split or batch processed without errors.

**End-to-End**
- Start from query, finish with files imported and verified in Scrivener.

---

## Regression/Upgrade Testing

- After upgrade to Cursor, agent APIs, Python libraries—rerun above on test workspace before migrating to production manuscript.

---

## Test Artifacts

- Test agent output files
- Script logs, error reports
- Manifest and final import listing

---

## Review/Sign-Off

- Reviewer to confirm all key steps
- Any failures or missed cases logged and addressed before regular use
